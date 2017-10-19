from music21 import *
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
    htmltext = """<score vorbis="1">\\relative """ + lpc.lyPitchFromPitch(s.getTonic()).noteNamePitch + " { \\key " + lpc.lyPitchFromPitch(s.getTonic()).noteNamePitch + " \\" + s.type + " " + " ".join([lpc.lyPitchFromPitch(p).noteNamePitch + "4" for p in s.getPitches()]) + " }</score>"
    print(htmltext)



