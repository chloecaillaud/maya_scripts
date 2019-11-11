# playblast shaded and shaded wireframe (200 frames)
import maya.cmds as cmds
import os

filepath = cmds.file(q=True, sn=True)
fileName = os.path.basename(filepath)
rawFileName, fileExt = os.path.splitext(fileName)
viewport = cmds.getPanel(withFocus=True)

cmds.modelEditor(viewport, edit=True, wireframeOnShaded=False)
cmds.playblast(st=1, et=200, f=(rawFileName + '_Playblast_Shaded.mov'), fo=True, fmt='avi', c='MS-RLE', p=100, qlt=100, v=False, w=1280, h=720, orn=False)
cmds.modelEditor(viewport, edit=True, wireframeOnShaded=True)
cmds.playblast(st=1, et=200, f=(rawFileName + '_Playblast_wireframe.mov'), fo=True, fmt='avi', c='MS-RLE', p=100, qlt=100, v=False, w=1280, h=720, orn=False)
cmds.modelEditor(viewport, edit=True, wireframeOnShaded=False)