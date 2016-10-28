"""Kraken - traverser module.

Classes:
Traverser - Base Traverser.

"""

from kraken.core.objects.scene_item import SceneItem
from kraken.core.objects.object_3d import Object3D
from kraken.core.objects.components.component import Component
from kraken.core.objects.attributes.attribute_group import AttributeGroup
from kraken.core.objects.constraints.constraint import Constraint
from kraken.core.objects.operators.operator import Operator
from kraken.core.maths import Xfo


class Traverser(object):
    """Kraken base traverser for any scene item.

    The traverser iterates through all root items and determines the
    dependencies between objects, building an ordered list as it goes. This
    order is then used by the builder to ensure that objects are created and
    evaluated in the correct order. Offset's will then be reliable.

    """

    def __init__(self, name='Traverser'):
        self._rootItems = []
        self.reset()

    # ==================
    # Property Methods
    # ==================
    @property
    def rootItems(self):
        """Gets the root items of this Traverser.

        Returns:
            list: The root items of this Traverser.

        """

        return self._xfo

    def addRootItem(self, item):
        """Adds a new root object to this Traverser

        Args:
            item (SceneItem): The SceneItem to add as a root item.

        Returns:
            bool: True if successful.

        """

        for rootItem in self._rootItems:
            if rootItem.getId() == item.getId():
                return False

        self._rootItems.append(item)

        return True

    def addRootItems(self, items):
        """Adds a bunch of root items to this Traverser

        Args:
            items (SceneItem[]): The SceneItems to add as root items.

        Returns:
            bool: True if successful.

        """

        for item in items:
            self.addRootItem(item)

        return True

    @property
    def items(self):
        """Gets the traversed items of this Traverser.

        Returns:
            list: The traversed items of this Traverser.

        """

        return self._items

    def getItemsOfType(self, typeNames):
        """Gets only the traversed items of a given type.

        Args:
            typeName (str): The name of the type to look for.

        Returns:
            list: The items in the total items list matching the given type.

        """

        if not isinstance(typeNames, list):
            typeNames = [typeNames]

        result = []
        for item in self._items:
            if item.isOfAnyType(typeNames):
                result.append(item)

        return result

    # =============
    # Traverse Methods
    # =============
    def reset(self):
        """Resets all internal structures of this Traverser."""

        self._visited = {}
        self._items = []

    def traverse(self, itemCallback=None, discoverCallback=None,
                 discoveredItemsFirst=True, toOptimize=False):
        """Visits all objects within this Traverser based on the root items.

        Args:
            itemCallback (func): A callback function to be invoked for each
                item visited.
            discoverCallback (func): A callback to return an array of children
                for each item.

        """

        self.reset()

        if discoverCallback is None:
            discoverCallback = self.discoverBySource

        for item in self._rootItems:
            self.__visitItem(item,
                             itemCallback,
                             discoverCallback,
                             discoveredItemsFirst)

        if toOptimize:
            connections, srcIndice, dstIndice = self.optimizeOperatorInput()
            self.optimizeConstraints(connections, srcIndice, dstIndice)

            for conn in connections:
                if conn["refCount"] != "never" and conn["refCount"] < 1:
                    try:
                        print "remove: ", conn["cns"].getBuildName()
                        self.items.remove(conn["cns"])
                    except ValueError:
                        pass

        return self.items

    def __collectVisitedItem(self, item, itemCallback):
        """Doc String.

        Args:
            item (Type): information.
            itemCallback (Type): information.

        """

        if itemCallback is not None:
            itemCallback(item=item, traverser=self)

        self._items.append(item)

    def __visitItem(self, item, itemCallback, discoverCallback, discoveredItemsFirst):
        """Doc String.

        Args:
            item (Type): information.
            itemCallback (Type): information.
            discoverCallback (Type): information.
            discoveredItemsFirst (Type): information.

        Returns:
            Type: information.

        """

        if self._visited.get(item.getId(), False):
            return False

        self._visited[item.getId()] = True

        if hasattr(item, 'getParent') and item.getParent():
            # If this is an attribute and we have not traversed its parent AttributeGroup then skip this
            # and visit the parent so we get this attribute and all others from there (for the sake of attr order)
            if item.isTypeOf("Attribute") and not self._visited.get(item.getParent().getId(), False):
                self._visited[item.getId()] = False
                self.__visitItem(item.getParent(),
                                 itemCallback,
                                 discoverCallback,
                                 discoveredItemsFirst)
                return False

            self.__visitItem(item.getParent(),
                             itemCallback,
                             discoverCallback,
                             discoveredItemsFirst)

        sourcedByConstraintOrOperator = False
        if discoveredItemsFirst:
            for source in item.getSources():
                if isinstance(source, (Constraint, Operator)):
                    sourcedByConstraintOrOperator = True
                    break

        if not discoveredItemsFirst or sourcedByConstraintOrOperator:
            self.__collectVisitedItem(item, itemCallback)

        if discoverCallback:
            if isinstance(item, AttributeGroup):
                discoveredItems = self.discoverChildren(item)
            else:
                discoveredItems = discoverCallback(item)

            if discoveredItems:
                for discoveredItem in discoveredItems:
                    self.__visitItem(discoveredItem,
                                     itemCallback,
                                     discoverCallback,
                                     discoveredItemsFirst)

        if discoveredItemsFirst and not sourcedByConstraintOrOperator:
            self.__collectVisitedItem(item, itemCallback)

        return True

    def discoverChildren(self, item):
        """Doc String.

        Args:
            item (Type): information.

        Returns:
            Type: information.

        """

        result = []

        if isinstance(item, Component):
            subItems = item.getItems().values()
            for subItem in subItems:
                if isinstance(subItem, AttributeGroup):
                    continue
                result.append(subItem)

        elif isinstance(item, Object3D):
            for i in xrange(item.getNumAttributeGroups()):
                result.append(item.getAttributeGroupByIndex(i))
            result += item.getChildren()

        if isinstance(item, AttributeGroup):
            for i in xrange(item.getNumAttributes()):
                result.append(item.getAttributeByIndex(i))

        return result

    def discoverBySource(self, item):
        """Doc String.

        Args:
            item (Type): information.

        Returns:
            Type: information.

        """

        result = []

        for source in item.getSources():

            if isinstance(source, Operator):
                for outputName in source.getOutputNames():
                    operatorOutputs = source.getOutput(outputName)
                    if not isinstance(operatorOutputs, list):
                        operatorOutputs = [operatorOutputs]
                    for operatorOutput in operatorOutputs:
                        if not isinstance(operatorOutput, SceneItem):
                            continue
                        result.append(operatorOutput)

            result.append(source)

        return result

    # ================
    # Optimaze Methods
    # ================
    def optimizeOperatorInput(self, cnsConnections=None, srcIndice=None, dstIndice=None):
        """Optimize self.items on operator inputs.

            Shortcut redudant constraint that can be passed through.

        """

        constraints = self.getItemsOfType('Constraint')
        operators = self.getItemsOfType('KLOperator')
        operators.extend(self.getItemsOfType('CanvasOperator'))

        if cnsConnections is None and srcIndice is None and dstIndice is None:
            cnsConnections, srcIndice, dstIndice = self._gatherConstraintConnections(constraints)
        opeOutputIndice = self._gatherOperatorConnections(operators)

        def getNewSrc(ope, portItem):

            if not self.isItemComponentIO(portItem):
                return portItem

            if portItem in dstIndice:
                anscestor = self._searchConstraintConnectionAscendant([dstIndice[portItem]], dstIndice, includeOffset=False)
                markConstraintAsNeverRemove(anscestor[0]['src'])
                return anscestor[0]['src']
            elif portItem in opeOutputIndice:
                # TODO:
                markConstraintAsNeverRemove(portItem)
                return portItem
            else:
                markConstraintAsNeverRemove(portItem)
                return portItem

        cacheMarkConstraintAsNeverRemove = []

        def markConstraintAsNeverRemove(src):
            if src in cacheMarkConstraintAsNeverRemove:
                return

            if src not in dstIndice:
                return

            start = dstIndice[src]
            needed = self._searchConstraintConnectionAscendant([start], dstIndice, includeOffset=True)

            for c in needed:
                c["refCount"] = "never"

            cacheMarkConstraintAsNeverRemove.append(src)

        for ope in operators:
            for portName, portItem in ope.inputs.iteritems():
                if type(portItem) == list:  # array port
                    news = [getNewSrc(ope, ele) for ele in portItem]
                else:
                    news = getNewSrc(ope, portItem)

                ope.inputs[portName] = news

        return cnsConnections, srcIndice, dstIndice

    def getOperatorsCanBeDirectConnect(self):
        """Retruns operator inforamions that can be direct connect with another operator.

        Returns:
            list[dict]: operator inforamtion that input can be direct connect with its src operator.
                    information contain as dict.

        """

        operators = self.getItemsOfType('KLOperator')
        operators.extend(self.getItemsOfType('CanvasOperator'))
        opeOutputIndice = self._gatherOperatorConnections(operators)
        result = []

        def _append(ope, portItem, portName, index):
            if not self.isItemComponentIO(portItem):
                return

            if portItem in opeOutputIndice:
                conn = opeOutputIndice[portItem]
                result.append(
                    {
                        'srcOperator': conn['ope'],
                        'dstOperator': ope,
                        'srcPortName': conn['name'],
                        'dstPortName': portName,
                        'srcIndex': conn['index'],
                        'dstIndex': index
                    }
                )

        for ope in operators:
            for portName, portItem in ope.inputs.iteritems():
                if type(portItem) == list:  # array port
                    for i, ele in enumerate(portItem):
                        _append(ope, ele, portName, i)
                else:
                    _append(ope, portItem, portName, -1)

        return result

    def optimizeConstraints(self, connections=None, srcIndice=None, dstIndice=None):
        """Optimize self.items on Constraints.

            Remove redudant constraint that can be passed through with another item.

        """

        constraints = self.getItemsOfType('Constraint')

        if connections is None and srcIndice is None and dstIndice is None:
            connections, srcIndice, dstIndice = self._gatherConstraintConnections(constraints)

        for conn in connections:

            new = self._searchConstraintConnectionAscendant([conn], dstIndice)
            new = self._searchConstraintConnectionDescendant(new, srcIndice)

            # connection does not terminal
            if new[-1] != conn:
                continue

            # not changed
            if len(new) == 1:
                continue
            elif len(new) < 1:
                # print "something wrong"
                continue

            newSrcConn = new[0]
            newDstConn = conn

            if newSrcConn["src"] not in newDstConn["cns"].getConstrainers():
                newDstConn["cns"].setConstrainer(newSrcConn["src"])
                canPassed = self._getMaintainOffsetInConnections(new)
                newDstConn["cns"].setMaintainOffset(canPassed)
                newDstConn["refCount"] = "never"
            # else:
            #     print "already in constrainers"

        return connections, srcIndice, dstIndice

    def _gatherOperatorConnections(self, operators):
        """Gather connection informations of given operators.

        Args:
            operators (SceneItem[]): The SceneItems that searched in for connection.

        Returns:
            dict: connection informations indexed by src item.

        """

        connections = {}

        def _append(ope, name, item, index):
            x = {
                'name': name,
                'dst': item,
                'index': index,
                'ope': ope
            }
            connections[item] = x

        for ope in operators:

            for outputName in ope.getOutputNames():
                operatorOutputs = ope.getOutput(outputName)

                if not isinstance(operatorOutputs, list):
                    if isinstance(operatorOutputs, SceneItem):
                        _append(ope, outputName, operatorOutputs, -1)

                else:
                    for i, operatorOutput in enumerate(operatorOutputs):
                        if not isinstance(operatorOutput, SceneItem):
                            continue

                        _append(ope, outputName, operatorOutput, i)

        return connections

    def _gatherConstraintConnections(self, constraints):
        """Gather connection inforamiotns of given constraints.

        Args:
            constraints (SceneItem[]): The SceneItems that searched in for connection.

        Returns:
            (list(dict), dict, dict):
                connections: connection informations
                bySrc: dict indexed by connection's src
                byDst: dict indexed by connection's dst

        """

        connections = []
        bySrc = {}
        byDst = {}

        for cns in constraints:

            if not self.isConstrainPartOfComponentIO(cns):
                continue

            dst = cns.getConstrainee()
            for src in cns.getConstrainers():
                x = {
                    'src': src,
                    'dst': dst,
                    'cns': cns,
                    'betweenComponentIO': self.isConstrainPartOfComponentIO(cns),
                    'refCount': 1
                }
                connections.append(x)

                bySrc[src] = x  # maybe duped key
                byDst[dst] = x

        return connections, bySrc, byDst

    def _searchConstraintConnectionAscendant(self, connections, dstIndice, includeOffset=True):
        """Search and return constraint connections for ascendant while constarint can be passed through.

        Args:
            connections (dict[]): connection information obtained by _gatherConstraintConnections
            dstIndice (dict): connection information indexed by src item obtained by _gatherConstraintConnections

        Returns:
            dict[]: connections stack as list. parent constraint as top, kid constarint as bottom.

        """

        conn = connections[0]
        src = conn["src"]

        if src in dstIndice:
            grandConn = dstIndice[src]

            if self.isConnectionCanPassedThrough(grandConn, includeOffset):
                conn["refCount"] = (conn["refCount"] - 1) if (conn["refCount"] != "never") else "never"
                connections.insert(0, grandConn)
                return self._searchConstraintConnectionAscendant(connections, dstIndice, includeOffset)

            else:
                return connections

        else:
            return connections

    def _searchConstraintConnectionDescendant(self, connections, srcIndice, includeOffset=True):
        """Search and return constraint connections for descendant while constarint can be passed through.

        Args:
            connections (dict[]): connection information obtained by _gatherConstraintConnections
            srcIndice (dict): connection information indexed by src item obtained by _gatherConstraintConnections

        Returns:
            dict[]: connections stack as list. parent constraint as top, kid constarint as bottom.

        """

        if type(connections) != list:
            connections = [connections]

        conn = connections[-1]
        dst = conn["dst"]

        if dst in srcIndice:
            grandConn = srcIndice[dst]

            if self.isConnectionCanPassedThrough(grandConn, includeOffset):
                conn["refCount"] = (conn["refCount"] - 1) if (conn["refCount"] != "never") else "never"
                connections.append(grandConn)
                return self._searchConstraintConnectionDescendant(connections, srcIndice)

            else:
                return connections

        else:
            return connections

    def _getMaintainOffsetInConnections(self, connections):
        """Doc String.

        Args:
            item (Type): information.

        Returns:
            Type: information.

        """

        for conn in connections:
            if not self.isConstraintCanPassedThrough(conn["cns"]):
                return True
        else:
            return False

    def isItemComponentIO(self, kSceneItem):
        """Doc String.

        Args:
            item (Type): information.

        Returns:
            Type: information.

        """

        return (
            (kSceneItem.getTypeName() == 'ComponentInput')
            or
            (kSceneItem.getTypeName() == 'ComponentOutput')
        )

    def isConstrainBetweenComponentIO(self, kConstraint):
        """Doc String.

        Args:
            item (Type): information.

        Returns:
            Type: information.

        """

        constrainee = kConstraint.getConstrainee()
        constrainer = kConstraint.getConstrainers()[0]

        return (
            (self.isItemComponentIO(constrainee) and self.isItemComponentIO(constrainer))
        )

    def isConstrainPartOfComponentIO(self, kConstraint):
        """Doc String.

        Args:
            item (Type): information.

        Returns:
            Type: information.

        """

        constrainee = kConstraint.getConstrainee()
        constrainers = kConstraint.getConstrainers()

        for c in constrainers:
            if c.getTypeName() in ['ComponentOutput', 'ComponentInput']:
                return True

        return constrainee.getTypeName() in ['ComponentOutput', 'ComponentInput']

    def isSrcOrDstPartOfComponentIO(self, src, dst):
        """Doc String.

        Args:
            item (Type): information.

        Returns:
            Type: information.

        """

        return ((src.getTypeName() in ['ComponentInput', 'ComponentOutput']) or
                (dst.getTypeName() in ['ComponentInput', 'ComponentOutput']))

    def isConstraintCanPassedThrough(self, kConstraint):
        """Doc String.

        Args:
            item (Type): information.

        Returns:
            Type: information.

        """

        if not kConstraint:
            return False

        if kConstraint.getMaintainOffset():
            if kConstraint.computeOffset() == Xfo():
                return True

            return False

        return True

    def isConnectionCanPassedThrough(self, connection, includeOffset=True):
        """Doc String.

        Args:
            item (Type): information.

        Returns:
            Type: information.

        """

        if not includeOffset:
            cns = connection["cns"]
            if not self.isConstraintCanPassedThrough(cns):
                return False

        if not connection['betweenComponentIO']:
            return False

        return True
