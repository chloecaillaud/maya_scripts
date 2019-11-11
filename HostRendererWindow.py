# pack scene and generate batch render command for rendering across multiple machines

import os
import maya.app.general.zipScene
import zipfile
import getpass

RENDER_DIR = 'H:\\Rendering\\'    #typically a network/shared drive
RENDERER_PATH = ('"C:\\Program Files\\Autodesk\\Maya2018\\bin\\Render.exe"')

#---------------------------------------------------------------------
def defineJobPath():
    filepath = cmds.file(q=True, sn=True)
    fileName = os.path.basename(filepath)
    rawFileName, fileExt = os.path.splitext(fileName)

    jobPath = (RENDER_DIR + rawFileName + '_Render\\')
    return jobPath
#---------------------------------------------------------------------
def archiveAndCopy():
    scenePath = cmds.file(q=True, sn=True)
    archivePath = (scenePath + '.zip')

    maya.app.general.zipScene.zipScene(1)

    zip_ref = zipfile.ZipFile(archivePath, 'r')
    zip_ref.extractall(defineJobPath())
    zip_ref.close()

#---------------------------------------------------------------------
def generateRenderCommand(startFrame, endFrame, customFlags):
    localAbsProjPath = cmds.workspace(q=True, rd=True)
    localAbsScenePath = cmds.file(q=True, sn=True)
    localRelativeProjPath = "/".join(localAbsProjPath.strip("/").split('/')[1:])
    localRelativeScenePath = "/".join(localAbsScenePath.strip("/").split('/')[1:])
    startFrameStr = str(startFrame)
    endFrameStr = str(endFrame)

    projectOption = (' -proj "' + defineJobPath() + localRelativeProjPath + '/"')
    sceneOption = (' "' + defineJobPath() + localRelativeScenePath + '"')
    imageOutputOption = (' -rd "' + defineJobPath() + '/imageOutput/"')
    frameRangeOption = (' -s ' + startFrameStr + ' -e ' + endFrameStr)
    customFlagsOption = (' ' + customFlags)

    renderCommand = (RENDERER_PATH + projectOption + ' -skipExistingFrames True' + imageOutputOption + frameRangeOption + customFlagsOption + sceneOption)

    f = open((defineJobPath() + 'renderCommand.bat'), 'w')
    f.write(renderCommand)
    f.close()

#---------------------------------------------------------------------
def sendRender():
    outStartFrame = cmds.intFieldGrp('startFrameValue', q=True, value=True)
    outEndFrame = cmds.intFieldGrp('endFrameValue', q=True, value=True)
    outCustomFlag = cmds.textFieldGrp('customFlagBox', q=True, text=True)

    defineJobPath()
    print(defineJobPath())
    archiveAndCopy()
    generateRenderCommand(outStartFrame[0], outEndFrame[0], outCustomFlag)
    cmds.deleteUI('DistrRendWin')


#---------------------------------------------------------------------
def showUI():
    DRW = 'DistrRendWin'
    defaultStartFrame = cmds.getAttr('defaultRenderGlobals.startFrame')
    defaultEndFrame = cmds.getAttr('defaultRenderGlobals.endFrame')

    if cmds.window(DRW, q=True, exists=True):
        cmds.deleteUI(DRW)


    cmds.window('DistrRendWin', title='Distributed Render', s=False, rtf=True)
    cmds.windowPref('DistrRendWin', remove=True)

    cmds.columnLayout()

    cmds.separator(h=20, w=400, st='none')
    cmds.intFieldGrp('startFrameValue', numberOfFields=1, label='Start Frame', value1=defaultStartFrame)
    cmds.intFieldGrp('endFrameValue', numberOfFields=1, label='End Frame', value1=defaultEndFrame)
    cmds.separator(h=20, w=400, st='none')
    cmds.textFieldGrp('customFlagBox', label='Custom Flag Option')
    cmds.separator(h=20, w=400, st='none')

    cmds.rowLayout(nc=3)
    cmds.button(label='Send', width=100, c='sendRender()')
    cmds.button(label='Cancel', width=100, c='cmds.deleteUI("%s")' % DRW)
    cmds.showWindow()

#---------------------------------------------------------------------

showUI()