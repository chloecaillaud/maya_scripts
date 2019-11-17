# create Locator(s) at selected object(s)

import maya.cmds as cmds

targetObjs = cmds.ls(selection=True)

for i in targetObjs:
    cmds.spaceLocator()
    createdObj = cmds.ls(selection=True, tail=1)

    cmds.matchTransform(createdObj, i)