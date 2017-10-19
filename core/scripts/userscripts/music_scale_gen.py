from music21 import *
import pywikibot
from scripts import pagefromfile
import string
import webbrowser


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
    #Open page on wiki create names automatically
    base = "http://leviolondejos.wiki/index.php?title=Spécial:AjouterDonnées/Tonalité"
    qstring = "&Tonalité[A la racine]=" + s.getTonic().name[0]
    if s.getTonic().alter == 1.0 :
        accidental = "+"
    elif s.getTonic().alter == -1.0:
        accidental = "-"
    else:
        accidental = "none"
    qstring += "&Tonalité[A l accent]=" + accidental
    qstring += "&Tonalité[Est une gamme du mode]=" + s.type
    myurl = base + qstring
    webbrowser.open(myurl)
