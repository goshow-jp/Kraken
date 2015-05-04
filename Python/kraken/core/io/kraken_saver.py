"""KrakenSaver - objects.kraken_saver module.

Classes:
KrakenSaver - Helper class for saving Kraken rigs to JSON representations .

"""

from kraken.core.maths.math_object import MathObject


class KrakenSaver(object):
    """Kraken base object type for any 3D object."""

    def __init__(self):
        super(KrakenSaver, self).__init__()


    def encodeValue(self, value):
        """Doc String.

        Arguments:
        value -- MathObject, the math object to be saved.

        Return:
        True if successful.

        """

        if isinstance(value, MathObject):
            return value.encodeValue()
        else:
            return value
