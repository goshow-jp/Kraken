//
// Copyright (C) goshow
// 
// File: Test2Node.h
//
// Dependency Graph Node: {{ node.class_name }}
//
// Author: Maya Plug-in Wizard 2.0
//
#pragma once

#define FEC_SHARED
#define FECS_SHARED
#include "FabricDFGWidget.h"
#include "FabricDFGBaseInterface.h"

#include <maya/MPxNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MTypeId.h> 
#include <maya/MNodeMessage.h>
#include <maya/MStringArray.h>

 
class {{ node.class_name }} : public MPxNode, public FabricDFGBaseInterface
{
public:
  static void* creator();
  static MStatus initialize();

  {{ node.class_name }}();
  void postConstructor();
  ~{{ node.class_name }}();

  // implement pure virtual functions
  virtual MObject getThisMObject() { return thisMObject(); }
  virtual MPlug getSaveDataPlug() { return MPlug(thisMObject(), saveData); }
  virtual MPlug getRefFilePathPlug() { return MPlug(thisMObject(), refFilePath); }

  void loadJSON();
  MStatus compute(const MPlug& plug, MDataBlock& data);
  bool transferStaticInputValuesToDFG(MPlug& plug, MDataBlock& data);
  void transferStaticOutputValuesToMaya(MPlug& plug, MDataBlock& data, bool isDeformer = false);

  // node attributes
  static MTypeId id;
  static MObject saveData;
  static MObject evalID;
  static MObject refFilePath;
  static MObject drawDebug;
  static MObject rigScale;

  {% for in_port in node.input_ports %}
  static MObject m_{{ in_port.name }};
  {% endfor %}
  {% for out_port in node.output_ports %}
  static MObject m_{{ out_port.name }};
  {% endfor %}
};
