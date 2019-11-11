# UI for opening assets across a list of projects

# Note: project and scene name must be named the same
# TODO: add support for mixed file types

import maya.cmds as cmds

GLOBAL_ASSETS_DIR = 'H:/folder/'
ASSET_LIST = ['Asset0' ,'Asset1' ,'Asset2']

assetListLen = len(ASSET_LIST)
#------------------------------------------------------
#

def showUI():
    DRW = 'AssetSelectionWindow'

    if cmds.window(DRW, q=True, exists=True):
        cmds.deleteUI(DRW)

    cmds.window('AssetSelectionWindow', title='Asset Selection Window', nde=True, s=False, rtf=True)
    cmds.windowPref('AssetSelectionWindow', remove=True)

    cmds.columnLayout()



    cmds.optionMenu('Asset')
    for i in range(0, assetListLen):
        cmds.menuItem(label=ASSET_LIST[i])


    cmds.rowLayout(nc=3)

    cmds.button(label='Save&&Open', width=75, c='SelectedItem = cmds.optionMenu("Asset", q=True, value=True) openAsset(SelectedItem, True)')
    cmds.button(label='Open', width=50, c='SelectedItem = cmds.optionMenu("Asset", q=True, value=True) openAsset(SelectedItem, False)')
    cmds.button(label='Cancel', width=50, c='cmds.deleteUI("%s")' % DRW)


    cmds.showWindow()

#------------------------------------------------------
#

def openAsset(SelectedItem, doSave):

    assetProjDir = (GLOBAL_ASSETS_DIR + SelectedItem + '/')
    assetFileName = (SelectedItem + '.ma')


    if doSave == True:
        cmds.file(save=True)

    cmds.workspace(assetProjDir, openWorkspace=True)
    cmds.file(assetFileName, open=True, force=True)

#------------------------------------------------------

showUI()
