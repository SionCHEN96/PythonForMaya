from maya import cmds


class Gear(object):
    """
    This a Gear object to create and modify a gear
    """
    def __init__(self):
        self.transform = None
        self.extrude = None
        self.constructor = None

    def createGear(self, teeth=10, length=0.3):
        spans = teeth * 2

        self.transform, self.constructor = cmds.polyPipe(subdivisionsAxis=spans)
        sideFaces = range(spans * 2, spans * 3, 2)

        cmds.select(clear=True)

        for face in sideFaces:
            cmds.select('%s.f[%s]' % (self.transform, face), add=True)

        self.extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]

    def changeTeeth(self, teeth=10, length=0.3):
        spans = teeth * 2
        cmds.polyPipe(self.constructor, edit=True, subdivisionsAxis=spans)

        sideFaces = range(spans * 2, spans * 3, 2)
        facesNames = []

        for face in sideFaces:
            facesName = 'f[%s]' % (face)
            facesNames.append(facesName)

        cmds.setAttr('%s.inputComponents' % (self.extrude), len(facesNames), *facesNames, type="componentList")

        cmds.polyExtrudeFacet(self.extrude, edit=True, localTranslateZ=length)
