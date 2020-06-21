from maya import cmds
from tweenerUI import tween
from gearClassCreator import Gear


class BaseWindow(object):
    windowName = "BaserWindow"

    def show(self):
        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)

        self.buildUI()
        cmds.showWindow()

    def buildUI(self):
        pass

    def reset(self, *args):
        pass

    def close(self, *args):
        cmds.deleteUI(self.windowName)


class TweenerUI(BaseWindow):
    windowName = "TwennerWindow"

    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label="Use this slider to set the tween amount")

        row = cmds.rowLayout(numberOfColumns=2)

        self.slider = cmds.floatSlider(min=0, max=100, value=50, step=1, changeCommand=tween)
        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def reset(self, *args):
        cmds.floatSlider(self.slider, edit=True, value=50)


class GearUI(BaseWindow):
    windowName = "GearWindow"

    def __init__(self):
        self.gear = None

    def buildUI(self):
        column = cmds.columnLayout()
        cmds.text(label="Use the slider to modify the gear")

        cmds.setParent(column)
        self.label = cmds.text(label="Teeth Num: 10")
        cmds.setParent(column)
        self.slider = cmds.intSlider(min=5, max=30, value=10, step=1, dragCommand=self.modifyGearTeeth)

        cmds.setParent(column)
        self.lengthLabel = cmds.text(label="Length: 0.5")
        cmds.setParent(column)
        self.LengthSlider = cmds.floatSlider(min=0.1, max=1, value=0.5, step=0.1, dragCommand=self.modifyGearLength)

        cmds.setParent(column)
        cmds.rowLayout(numberOfColumns=2)
        cmds.button(label="Make Gear", command=self.makeGear)
        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def makeGear(self, *args):
        teeth = cmds.intSlider(self.slider, query=True, value=True)
        length = cmds.floatSlider(self.LengthSlider, query=True, value=True)
        self.gear = Gear()
        self.gear.createGear(teeth=teeth,length=length)

    def modifyGearTeeth(self, teeth):
        if self.gear:
            self.gear.changeTeeth(teeth=teeth)
        cmds.text(self.label, edit=True, label="Teeth Num: "+str(teeth))

    def modifyGearLength(self, length):
        if self.gear:
            self.gear.changeTeeth(teeth=cmds.intSlider(self.slider, query=True, value=True),length=length)
        cmds.text(self.lengthLabel, edit=True, label="Length: "+str(length))

    def reset(self, *args):
        self.gear = None
        cmds.intSlider(self.slider, edit=True, value=10)
        cmds.text(self.label, edit=True, label=10)
        cmds.text(self.lengthLabel, edit=True, label=0.5)
