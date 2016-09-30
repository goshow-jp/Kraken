#pragma once
#define FEC_SHARED
#define FECS_SHARED

#include "FabricDFGCommands.h"

// -------------------------
// -------------------------
class MonolithDFGReloadJSONCommand
  : public FabricDFGBaseCommand
{
public:

  static void* creator()
    { return new MonolithDFGReloadJSONCommand; }

  virtual MString getName()
    { return "monolithReloadJSON"; }

  static MSyntax newSyntax();
  virtual MStatus doIt( const MArgList &args );
  virtual bool isUndoable() const { return false; }
};
