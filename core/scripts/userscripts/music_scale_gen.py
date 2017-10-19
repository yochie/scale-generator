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
    title = """'''""" + s.getTonic().name.replace("#","+") + " " + s.type + """'''\n"""
    lynote = lpc.lyPitchFromPitch(s.getTonic()).noteNamePitch
    attribute0 = "<noinclude>[[Category:Gamme]]</noinclude>\n"
    attribute1 = """{{#set: Est une gamme du mode=""" + s.type + "}}\n"
    if s.getTonic().alter == 1.0 :
        accidental = "+"
    elif s.getTonic().alter == -1.0:
        accidental = "-"
    else:
        accidental = "none"
    attribute2 = """{{#set: A l accent=""" + accidental + "}}\n"
    attribute3 = """{{#set: A la racine=""" + s.getTonic().name[0] + "}}\n"
    attributes = attribute0 + attribute1 + attribute2 + attribute3
    htmltext = sep + title + attributes + """<score vorbis="1">\\relative """ + lynote + " { \\key " + lynote + " \\" + s.type + " " + " ".join([lpc.lyPitchFromPitch(p).noteNamePitch + "4" for p in s.getPitches()]) + " }</score>\n" + sep
    
    fh.write(htmltext)
    print(htmltext)

fh.close()

pagefromfile.main('-file:' + pagefile ,'-begin:' + '@@@@@', '-end:' + '@@@@@', '-notitle', '-force', '-putthrottle:1')


