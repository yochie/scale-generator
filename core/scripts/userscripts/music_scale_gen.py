from music21 import *
import pywikibot
from scripts import pagefromfile
import string

pagefile = "toUpload.txt"
sep = "@@@@@\n"

fh = open(pagefile, "w")

us = environment.UserSettings()
us['lilypondPath'] = 'E:\\apps\\LilyPond\\usr\\bin\\lilypond.exe'

cKey = key.Key('C')
cScale = cKey.getPitches()

baseScales =[]
for p in cScale[:-1]:
    baseScales.append(key.Key(p).getScale())

allScales = []
for currentScale in baseScales:
    currentMinorScale = scale.MinorScale(currentScale.tonic.name)
    majorflat = scale.MajorScale(currentScale.tonic.name + "-")
    minorflat = scale.MinorScale(currentScale.tonic.name + "-")
    majorsharp = scale.MajorScale(currentScale.tonic.name + "#")
    minorsharp = scale.MinorScale(currentScale.tonic.name + "#")
    allScales.append(majorflat)
    allScales.append(minorflat)
    allScales.append(currentScale)
    allScales.append(currentMinorScale)
    allScales.append(majorsharp)
    allScales.append(minorsharp)
    
lpc = lily.translate.LilypondConverter()
for s in allScales:
    title = """'''""" + s.getTonic().name.replace("#","is").replace("-", "es") + " " + s.type + """'''\n"""
    lynote = lpc.lyPitchFromPitch(s.getTonic()).noteNamePitch
    attributes = []
    attributes.append("<noinclude>[[Category:Gamme]]</noinclude>\n")
    attributes.append("""{{#set: Est une gamme du mode=""" + s.type + "}}\n")
    if s.getTonic().alter == 1.0 :
        accidental = "is"
    elif s.getTonic().alter == -1.0:
        accidental = "es"
    else:
        accidental = "none"
    attributes.append("""{{#set: A l accent=""" + accidental + "}}\n")
    attributes.append("""{{#set: A la racine=""" + s.getTonic().name[0] + "}}\n")
    htmltext = sep + title + "".join(attributes) + """<score vorbis="1">\\relative """ + lynote + "'" + " { \\key " + lynote + " \\" + s.type + " " + " ".join([lpc.lyPitchFromPitch(p).noteNamePitch + "4" for p in s.getPitches()]) + " }</score>\n" + sep
    
    fh.write(htmltext)
    print(htmltext)

fh.close()

pagefromfile.main('-file:' + pagefile ,'-begin:' + '@@@@@', '-end:' + '@@@@@', '-notitle', '-force', '-putthrottle:1')


