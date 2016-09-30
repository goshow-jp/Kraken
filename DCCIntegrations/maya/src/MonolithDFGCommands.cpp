#include "Foundation.h"
#include "MonolithDFGCommands.h"


MSyntax MonolithDFGReloadJSONCommand::newSyntax()
{
  MSyntax syntax;
  syntax.addFlag("-m", "-mayaNode", MSyntax::kString);
  syntax.enableQuery(false);
  syntax.enableEdit(false);
  return syntax;
}

MStatus MonolithDFGReloadJSONCommand::doIt(const MArgList &args)
{
  MStatus status;
  MArgParser argParser( syntax(), args, &status );
  CHECK_MSTATUS_AND_RETURN_IT(status);

  try
  {
    if ( !argParser.isFlagSet("mayaNode") )
    {
      throw ArgException( MS::kFailure, "-m (-mayaNode) not provided." );
    }

    MString mayaNodeName = argParser.flagArgumentString("mayaNode", 0);

    FabricDFGBaseInterface * interf = FabricDFGBaseInterface::getInstanceByName( mayaNodeName.asChar() );
    if ( !interf )
    {
      throw ArgException( MS::kNotFound, "Maya node '" + mayaNodeName + "' not found." );
    }

    interf->reloadFromReferencedFilePath();
  }
  catch ( ArgException e )
  {
    logError( e.getDesc() );
    status = e.getStatus();
  }
  catch ( FabricCore::Exception e )
  {
    logError( e.getDesc_cstr() );
    status = MS::kFailure;
  }
  
  return status;
}
