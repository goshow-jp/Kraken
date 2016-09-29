//
// Copyright (C) 
// 
// File: pluginMain.cpp
//
// Author: Maya Plug-in Wizard 2.0
//
#include "Foundation.h"

#include "Test2Node.h"
#include "test3.h"

#include <maya/MFnPlugin.h>
#include <maya/MGlobal.h>
#include <maya/MFnPlugin.h>
#include <maya/MSceneMessage.h>
#include <maya/MDGMessage.h>
#include <maya/MAnimMessage.h>
#include <maya/MUiMessage.h>
#include <maya/MEventMessage.h>
#include <maya/MQtUtil.h>
#include <maya/MCommandResult.h>
#include <maya/MViewport2Renderer.h>
#include <maya/MFileIO.h>


#include <FabricSplice.h>
#include "FabricSpliceMayaNode.h"
#include "FabricSpliceMayaDeformer.h"
#include "FabricSpliceCommand.h"
#include "FabricSpliceEditorCmd.h"
#include "FabricSpliceMayaData.h"
#include "FabricSpliceToolContext.h"
#include "FabricDFGWidgetCommand.h"
#include "FabricDFGWidget.h"
#include "FabricDFGCanvasNode.h"
#include "FabricDFGCanvasDeformer.h"
#include "FabricDFGCommands.h"
#include "FabricSpliceHelpers.h"
#include "FabricUpgradeAttrCommand.h"


#ifdef _MSC_VER
  #define MAYA_EXPORT extern "C" __declspec(dllexport) MStatus _cdecl
#else
  #define MAYA_EXPORT extern "C" MStatus
#endif

MCallbackId gOnSceneNewCallbackId;
MCallbackId gOnSceneLoadCallbackId;
MCallbackId gOnSceneSaveCallbackId;
MCallbackId gOnMayaExitCallbackId;
MCallbackId gOnBeforeImportCallbackId;
MCallbackId gOnSceneImportCallbackId;
MCallbackId gOnSceneExportCallbackId;
MCallbackId gOnSceneCreateReferenceCallbackId;
MCallbackId gOnSceneImportReferenceCallbackId;
MCallbackId gOnSceneLoadReferenceCallbackId;
MCallbackId gOnNodeAddedCallbackId;
MCallbackId gOnNodeRemovedCallbackId;
MCallbackId gOnNodeAddedDFGCallbackId;
MCallbackId gOnNodeRemovedDFGCallbackId;
MCallbackId gOnAnimCurveEditedCallbackId;
MCallbackId gOnBeforeSceneOpenCallbackId;
MCallbackId gOnModelPanelSetFocusCallbackId;

void onSceneSave(void *userData){

  MStatus status = MS::kSuccess;
  mayaSetLastLoadedScene(MFileIO::beforeSaveFilename(&status));
  if(mayaGetLastLoadedScene().length() == 0) // this happens during copy & paste
    return;

  std::vector<FabricSpliceBaseInterface*> instances = FabricSpliceBaseInterface::getInstances();

  for(uint32_t i = 0; i < instances.size(); ++i){
    FabricSpliceBaseInterface *node = instances[i];
    node->storePersistenceData(mayaGetLastLoadedScene(), &status);
  }

  FabricDFGBaseInterface::allStorePersistenceData(mayaGetLastLoadedScene(), &status);
}

void onSceneNew(void *userData){
  FabricSpliceEditorWidget::postClearAll();
  // FabricSpliceRenderCallback::sDrawContext.invalidate(); 

  MString cmd = "source \"FabricDFGUI.mel\"; deleteDFGWidget();";
  MGlobal::executeCommandOnIdle(cmd, false);
  FabricDFGWidget::Destroy();
 
  char const *no_client_persistence = ::getenv( "FABRIC_DISABLE_CLIENT_PERSISTENCE" );
  if (!!no_client_persistence && !!no_client_persistence[0])
  {
    // [FE-5944] old behavior: destroy the client.
    FabricSplice::DestroyClient();
  }
  else
  {
    // [FE-5508]
    // rather than destroying the client via
    // FabricSplice::DestroyClient() we only
    // remove all singleton objects.
    const FabricCore::Client * client = NULL;
    FECS_DGGraph_getClient(&client);
    if (client)
    {
      FabricCore::RTVal handleVal = FabricSplice::constructObjectRTVal("SingletonHandle");
      handleVal.callMethod("", "removeAllObjects", 0, NULL);
    }
  }
}

void onSceneLoad(void *userData){
  FabricSpliceEditorWidget::postClearAll();
  // FabricSpliceRenderCallback::sDrawContext.invalidate(); 

  if(getenv("FABRIC_SPLICE_PROFILING") != NULL)
    FabricSplice::Logging::enableTimers();

  MStatus status = MS::kSuccess;
  mayaSetLastLoadedScene(MFileIO::currentFile());

  std::vector<FabricSpliceBaseInterface*> instances = FabricSpliceBaseInterface::getInstances();

  // each node will only restore once, so it's safe for import too
  FabricSplice::Logging::AutoTimer persistenceTimer("Maya::onSceneLoad");
  for(uint32_t i = 0; i < instances.size(); ++i){
    FabricSpliceBaseInterface *node = instances[i];
    node->restoreFromPersistenceData(mayaGetLastLoadedScene(), &status); 
    if( status != MS::kSuccess)
      return;
  }
  FabricSpliceEditorWidget::postClearAll();

  FabricDFGBaseInterface::allRestoreFromPersistenceData(mayaGetLastLoadedScene(), &status);

  if(getenv("FABRIC_SPLICE_PROFILING") != NULL)
  {
    for(unsigned int i=0;i<FabricSplice::Logging::getNbTimers();i++)
    {
      std::string name = FabricSplice::Logging::getTimerName(i);
      FabricSplice::Logging::logTimer(name.c_str());
      FabricSplice::Logging::resetTimer(name.c_str());
    }
  }

  // [FE-6612] invalidate all DFG nodes.
  for (unsigned int i=0;i<FabricDFGBaseInterface::getNumInstances();i++)
    FabricDFGBaseInterface::getInstanceByIndex(i)->invalidateNode();
}

void onBeforeImport(void *userData){
  // [FE-6247]
  // before importing anything we mark all current base interfaces
  // as "restored from pers. data", so that they get skipped when
  // FabricDFGBaseInterface::allRestoreFromPersistenceData() is invoked
  // in the above onSceneLoad() function.
  FabricDFGBaseInterface::setAllRestoredFromPersistenceData(true);
}

bool gSceneIsDestroying = false;
void onMayaExiting(void *userData){
  gSceneIsDestroying = true;
  std::vector<FabricSpliceBaseInterface*> instances = FabricSpliceBaseInterface::getInstances();

  for(uint32_t i = 0; i < instances.size(); ++i){
    FabricSpliceBaseInterface *node = instances[i];
    node->resetInternalData();
  }

  FabricDFGBaseInterface::allResetInternalData();

  FabricDFGWidget::Destroy();

  FabricSplice::DestroyClient(true);
}

bool isDestroyingScene()
{
  return gSceneIsDestroying;
}



MAYA_EXPORT initializePlugin( MObject obj )
{ 

  char const *disable_evalContext = ::getenv( "FABRIC_MAYA_DISABLE_EVALCONTEXT" );
  FabricDFGBaseInterface::s_use_evalContext = !(!!disable_evalContext && !!disable_evalContext[0]);
  if (!FabricDFGBaseInterface::s_use_evalContext)
  {
    MGlobal::displayInfo("[Fabric for Maya]: evalContext has been disabled via the environment variable FABRIC_MAYA_DISABLE_EVALCONTEXT.");
  }

  MStatus   status;
  MFnPlugin plugin( obj, "Monolith", "2016", "Any");

  /*
  if (MGlobal::mayaState() == MGlobal::kInteractive)
  {
    FabricSpliceRenderCallback::plug();
  }
  */

  gOnSceneSaveCallbackId            = MSceneMessage::addCallback(MSceneMessage::kBeforeSave, onSceneSave);
  gOnSceneLoadCallbackId            = MSceneMessage::addCallback(MSceneMessage::kAfterOpen, onSceneLoad);
  gOnBeforeSceneOpenCallbackId      = MSceneMessage::addCallback(MSceneMessage::kBeforeOpen, onSceneNew);
  gOnSceneNewCallbackId             = MSceneMessage::addCallback(MSceneMessage::kBeforeNew, onSceneNew);
  gOnMayaExitCallbackId             = MSceneMessage::addCallback(MSceneMessage::kMayaExiting, onMayaExiting);
  gOnSceneExportCallbackId          = MSceneMessage::addCallback(MSceneMessage::kBeforeExport, onSceneSave);
  gOnBeforeImportCallbackId         = MSceneMessage::addCallback(MSceneMessage::kBeforeImport, onBeforeImport);
  gOnSceneImportCallbackId          = MSceneMessage::addCallback(MSceneMessage::kAfterImport, onSceneLoad);
  gOnSceneCreateReferenceCallbackId = MSceneMessage::addCallback(MSceneMessage::kAfterCreateReference, onSceneLoad);
  gOnSceneImportReferenceCallbackId = MSceneMessage::addCallback(MSceneMessage::kAfterImportReference, onSceneLoad);
  gOnSceneLoadReferenceCallbackId   = MSceneMessage::addCallback(MSceneMessage::kAfterLoadReference, onSceneLoad);
 
  plugin.registerNode("Test2", Test2::id, Test2::creator, Test2::initialize );
  plugin.registerNode("test3", test3::id, test3::creator, test3::initialize );


  FabricSplice::Initialize();
  FabricSplice::Logging::setLogFunc(mayaLogFunc);
  FabricSplice::Logging::setLogErrorFunc(mayaLogErrorFunc);
  FabricSplice::Logging::setKLReportFunc(mayaKLReportFunc);
  FabricSplice::Logging::setKLStatusFunc(mayaKLStatusFunc);
  FabricSplice::Logging::setCompilerErrorFunc(mayaCompilerErrorFunc);

  if (MGlobal::mayaState() == MGlobal::kInteractive){
    FabricSplice::SetLicenseType(FabricCore::ClientLicenseType_Interactive);
  } else {
    FabricSplice::SetLicenseType(FabricCore::ClientLicenseType_Compute);
  }


  return status;
}

MAYA_EXPORT uninitializePlugin( MObject obj)
//
//  Description:
//    this method is called when the plug-in is unloaded from Maya. It 
//    deregisters all of the services that it was providing.
//
//  Arguments:
//    obj - a handle to the plug-in object (use MFnPlugin to access it)
//
{
  MStatus   status;
  MFnPlugin plugin( obj );

  plugin.deregisterNode(Test2::id);
  plugin.deregisterNode(test3::id);


  FabricSplice::Logging::setKLReportFunc(0);
  FabricSplice::DestroyClient();
  FabricSplice::Finalize();

  /*
  if (MGlobal::mayaState() == MGlobal::kInteractive)
  {
    FabricSpliceRenderCallback::unplug();
  }
  */

  return status;
}
