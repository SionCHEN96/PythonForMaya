from maya import cmds


def createGear(teeth=10, length=0.3):
    """
    This function will create a gear with the given paras
    Args:
        teeth: The number of teeth to create
        length: the length of the teeth

    Returns:
        A tuple of the transform, constructor and extrude node

    """
    print("Creating Gear", teeth, length)
    # Teeth are every altenate face, so span *2
    spans = teeth * 2

    transform, constructor = cmds.polyPipe(subdivisionsAxis=spans)

    sideFaces = range(spans * 2, spans * 3, 2)
    cmds.select(clear=True)

    for face in sideFaces:
        cmds.select('%s.f[%s]' % (transform, face), add=True)

    extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]
    return transform, constructor, extrude


def changeTeeth(constructor, extrude, teeth=10, length=0.3):
    spans = teeth * 2
    cmds.polyPipe(constructor, edit=True, subdivisionsAxis=spans)

    sideFaces = range(spans * 2, spans * 3, 2)
    facesNames = []

    for face in sideFaces:
        facesName = 'f[%s]' % (face)
        facesNames.append(facesName)

    cmds.setAttr('%s.inputComponents' % (extrude), len(facesNames), *facesNames, type="componentList")

    cmds.polyExtrudeFacet(extrude, edit=True, localTranslateZ=length)
