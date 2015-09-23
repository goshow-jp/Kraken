# Kraken_Plugin

import win32com.client
from win32com.client import constants
import os
import inspect

from win32com.client import constants
from multiprocessing import Pool

import webbrowser

import Qt
Qt.initialize()
from Qt.QtGui import QMainWindow
from Qt.QtGui import QWidget

from PySide import QtWebKit
from PySide import QtGui, QtCore

from kraken.core.objects.rig import Rig
from kraken import plugins

import kraken.ui.kraken_window
reload(kraken.ui.kraken_window)
from kraken.ui.kraken_window import KrakenWindow
from kraken.ui.kraken_window import createSplash

si = Application
log = si.LogMessage


def XSILoadPlugin(in_reg):
    in_reg.Author = 'Eric Thivierge & Phil Taylor'
    in_reg.Name = 'Kraken_Plugin'
    in_reg.Major = 1
    in_reg.Minor = 0

    pluginPath = in_reg.OriginPath
    krakenDir = os.path.normpath(XSIUtils.BuildPath(pluginPath, "..", "..", "..", ".."))
    os.environ['KRAKEN_PATH']  = krakenDir

    krakenExtsDir = os.path.join(krakenDir, 'KLExts')
    if krakenExtsDir not in  os.environ['FABRIC_EXTS_PATH']:
        os.environ['FABRIC_EXTS_PATH'] = krakenExtsDir + ';' + os.environ['FABRIC_EXTS_PATH']

    krakenLoadMenu = os.getenv('KRAKEN_LOAD_MENU', 'True')
    if krakenLoadMenu == 'True':
        in_reg.RegisterMenu(constants.siMenuMainTopLevelID, "Kraken", False, False)

    in_reg.RegisterCommand('OpenKrakenEditor', 'OpenKrakenEditor')
    in_reg.RegisterCommand('BuildKrakenGuide', 'BuildKrakenGuide')
    in_reg.RegisterCommand('BuildKrakenRig', 'BuildKrakenRig')


def XSIUnloadPlugin(in_reg):
    log(in_reg.Name + ' has been unloaded.', constants.siVerbose)

    return True


def Kraken_Init( in_ctxt ):

    menu = in_ctxt.source;
    menu.AddCommandItem( "Open UI", "OpenKrakenEditor")
    menu.AddSeparatorItem();
    menu.AddCommandItem("Build Guide", "BuildKrakenGuide")
    menu.AddCommandItem("Build Rig", "BuildKrakenRig")
    menu.AddSeparatorItem();
    menu.AddCallbackItem( "Help", "OpenKrakenHelp" )


# =========
# Commands
# =========
def OpenKrakenEditor_Init(in_ctxt):
    cmd = in_ctxt.Source
    cmd.Description = 'Opens the Kraken Editor'
    cmd.SetFlag(constants.siCannotBeUsedInBatch, True)
    cmd.ReturnValue = True

    return True


def OpenKrakenEditor_Execute():

    sianchor = Application.getQtSoftimageAnchor()
    sianchor = Qt.wrapinstance(long(sianchor), QWidget)

    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication([])

    for widget in app.topLevelWidgets():
            if widget.objectName() == 'KrakenMainWindow':
                widget.showNormal()

                return

    splash = createSplash(app)
    splash.show()

    window = KrakenWindow(parent=sianchor)
    window.show()

    splash.finish(window)

    return True


def BuildKrakenGuide_Init(in_ctxt):
    cmd = in_ctxt.Source
    cmd.Description = 'Builds a Kraken Guide from a .krg File'
    cmd.ReturnValue = True

    args = cmd.Arguments
    args.Add('rigFilePath', constants.siArgumentInput, "", constants.siString)

    return True


def BuildKrakenGuide_Execute(rigFilePath):

    if rigFilePath == "" and si.Interactive is True:

        fileBrowser = XSIUIToolkit.FileBrowser
        fileBrowser.DialogTitle = "Select a Kraken Rig File"
        fileBrowser.InitialDirectory = si.ActiveProject3.Path
        fileBrowser.Filter = "Kraken Rig (*.krg)|*.krg||"
        fileBrowser.ShowOpen()

        fileName = fileBrowser.FilePathName
        if fileName != "":
            rigFilePath = fileName
        else:
            log("User Cancelled.", 4)
            return False

    elif rigFilePath == "" and si.Interactive is False:
        log("No rig file path specified in batch mode!", 2)
        return False

    guideRig = Rig()
    guideRig.loadRigDefinitionFile(rigFilePath)

    builtRig = None
    progressBar = None
    try:

        progressBar = XSIUIToolkit.ProgressBar
        progressBar.Caption = "Building Kraken Guide: " + guideRig.getName()
        progressBar.CancelEnabled = False
        progressBar.Visible = True

        builder = plugins.getBuilder()
        builtRig = builder.build(guideRig)

    finally:
        if progressBar is not None:
            progressBar.Visible = False

    return builtRig


def BuildKrakenRig_Init(in_ctxt):
    cmd = in_ctxt.Source
    cmd.Description = 'Builds a Kraken Rig from a .krg File'
    cmd.ReturnValue = True

    args = cmd.Arguments
    args.Add('rigFilePath', constants.siArgumentInput, "", constants.siString)

    return True


def BuildKrakenRig_Execute(rigFilePath):

    if rigFilePath == "" and si.Interactive is True:

        fileBrowser = XSIUIToolkit.FileBrowser
        fileBrowser.DialogTitle = "Select a Kraken Rig File"
        fileBrowser.InitialDirectory = si.ActiveProject3.Path
        fileBrowser.Filter = "Kraken Rig (*.krg)|*.krg||"
        fileBrowser.ShowOpen()

        fileName = fileBrowser.FilePathName
        if fileName != "":
             rigFilePath = fileName
        else:
            log("User Cancelled.", 4)
            return False

    elif rigFilePath == "" and si.Interactive is False:
        log("No rig file path specified in batch mode!", 2)
        return False

    guideRig = Rig()
    guideRig.loadRigDefinitionFile(rigFilePath)
    rigBuildData = guideRig.getRigBuildData()

    rig = Rig()
    rig.loadRigDefinition(rigBuildData)
    rig.setName(guideRig.getName().replace('_guide', ''))

    builtRig = None
    progressBar = None
    try:

        progressBar = XSIUIToolkit.ProgressBar
        progressBar.Caption = "Building Kraken Rig: " + rig.getName()
        progressBar.CancelEnabled = False
        progressBar.Visible = True

        builder = plugins.getBuilder()
        builtRig = builder.build(rig)

    finally:
        if progressBar is not None:
            progressBar.Visible = False

    return builtRig


# ==========
# Callbacks
# ==========
def OpenKrakenHelp(in_ctxt):
    menuItem = in_ctxt.source

    webbrowser.open_new_tab('http://fabric-engine.github.io/Kraken')