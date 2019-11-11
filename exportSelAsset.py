# export selection to separate file

import maya.cmds as cmds
import os

EXPORT_SUBFOLDER = 'exportedAsset'    #define folder to send file to

#get required information
selItems = cmds.ls(sl=True, long=True)
projDir = cmds.workspace(q=True, rd=True)
filepath = cmds.file(q=True, exn=True)
fileName = os.path.basename(filepath)
rawFileName, fileExt = os.path.splitext(fileName)

#create path
exportFileDir = (projDir + EXPORT_SUBFOLDER + '/')
exportFileName = (rawFileName + '_Export' + fileExt)
exportFilePath = (exportFileDir + exportFileName)

#export without hierarchy
cmds.group(selItems, n=rawFileName, w=True)
cmds.file(exportFilePath, type='mayaBinary', es=True)
cmds.undo()    #reset changes to hierarchy