#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, os.path
import json
import xml.etree.ElementTree as ET
import errno

# <Instrument id="db-piccolo">
#       <longName>D♭ Piccolo</longName>
#       <shortName>D♭ Picc.</shortName>
#       <description>Piccolo Flute in Db</description>
#       <musicXMLid>wind.flutes.flute.piccolo</musicXMLid>
#       <transposingClef>G</transposingClef>
#       <concertClef>G8va</concertClef>
#       <barlineSpan>1</barlineSpan>
#       <aPitchRange>75-106</aPitchRange>
#       <pPitchRange>75-109</pPitchRange>
#       <transposeDiatonic>8</transposeDiatonic>
#       <transposeChromatic>13</transposeChromatic>
#       <Channel>
#             <program value="72"/>
#       </Channel>
# </Instrument>

SPN_data_head =  ["Octave/Note","-1","0","1","2","3","4","5","6","7","8","9"]

# Scraped from https://en.wikipedia.org/wiki/Scientific_pitch_notation
SPN_data_table = (
    [ ["C",  "8.176 (0)","16.352 (12)","32.703 (24)","65.406 (36)","130.81 (48)","261.63 (60)","523.25 (72)","1046.5 (84)","2093.0 (96)","4186.0 (108)","8372.0 (120)"]
    , ["C#", "8.662 (1)","17.324 (13)","34.648 (25)","69.296 (37)","138.59 (49)","277.18 (61)","554.37 (73)","1108.7 (85)","2217.5 (97)","4434.9 (109)","8869.8 (121)"]
    , ["Db", "8.662 (1)","17.324 (13)","34.648 (25)","69.296 (37)","138.59 (49)","277.18 (61)","554.37 (73)","1108.7 (85)","2217.5 (97)","4434.9 (109)","8869.8 (121)"]
    , ["D",  "9.177 (2)","18.354 (14)","36.708 (26)","73.416 (38)","146.83 (50)","293.66 (62)","587.33 (74)","1174.7 (86)","2349.3 (98)","4698.6 (110)","9397.3 (122)"]
    , ["Eb", "9.723 (3)","19.445 (15)","38.891 (27)","77.782 (39)","155.56 (51)","311.13 (63)","622.25 (75)","1244.5 (87)","2489.0 (99)","4978.0 (111)","9956.1 (123)"]
    , ["D#", "9.723 (3)","19.445 (15)","38.891 (27)","77.782 (39)","155.56 (51)","311.13 (63)","622.25 (75)","1244.5 (87)","2489.0 (99)","4978.0 (111)","9956.1 (123)"]
    , ["E",  "10.301 (4)","20.602 (16)","41.203 (28)","82.407 (40)","164.81 (52)","329.63 (64)","659.26 (76)","1318.5 (88)","2637.0 (100)","5274.0 (112)","10548.1 (124)"]
    , ["F",  "10.914 (5)","21.827 (17)","43.654 (29)","87.307 (41)","174.61 (53)","349.23 (65)","698.46 (77)","1396.9 (89)","2793.8 (101)","5587.7 (113)","11175.3 (125)"]
    , ["F#", "11.563 (6)","23.125 (18)","46.249 (30)","92.499 (42)","185.00 (54)","369.99 (66)","739.99 (78)","1480.0 (90)","2960.0 (102)","5919.9 (114)","11839.8 (126)"]
    , ["Gb", "11.563 (6)","23.125 (18)","46.249 (30)","92.499 (42)","185.00 (54)","369.99 (66)","739.99 (78)","1480.0 (90)","2960.0 (102)","5919.9 (114)","11839.8 (126)"]
    , ["G",  "12.250 (7)","24.500 (19)","48.999 (31)","97.999 (43)","196.00 (55)","392.00 (67)","783.99 (79)","1568.0 (91)","3136.0 (103)","6271.9 (115)","12543.9 (127)"]
    , ["Ab", "12.979 (8)","25.957 (20)","51.913 (32)","103.83 (44)","207.65 (56)","415.30 (68)","830.61 (80)","1661.2 (92)","3322.4 (104)","6644.9 (116)","13289.8 (128)"]
    , ["G#", "12.979 (8)","25.957 (20)","51.913 (32)","103.83 (44)","207.65 (56)","415.30 (68)","830.61 (80)","1661.2 (92)","3322.4 (104)","6644.9 (116)","13289.8 (128)"]
    , ["A",  "13.750 (9)","27.500 (21)","55.000 (33)","110.00 (45)","220.00 (57)","440.00 (69)","880.00 (81)","1760.0 (93)","3520.0 (105)","7040.0 (117)","14080.0 (129)"]
    , ["Bb", "14.568 (10)","29.135 (22)","58.270 (34)","116.54 (46)","233.08 (58)","466.16 (70)","932.33 (82)","1864.7 (94)","3729.3 (106)","7458.6 (118)","14917.2 (130)"]
    , ["A#", "14.568 (10)","29.135 (22)","58.270 (34)","116.54 (46)","233.08 (58)","466.16 (70)","932.33 (82)","1864.7 (94)","3729.3 (106)","7458.6 (118)","14917.2 (130)"]
    , ["B",  "15.434 (11)","30.868 (23)","61.735 (35)","123.47 (47)","246.94 (59)","493.88 (71)","987.77 (83)","1975.5 (95)","3951.1 (107)","7902.1 (119)","15804.3 (131)"]
    ])

def get_midi_data_table():
    # Construct a table of note data indexed by MIDI note number
    # Each entry is of the form: { "SPN": "C4", "freq": "261.3"}
    midi_data_table = {}
    for row in SPN_data_table:
        SPN_note = row[0]
        for j in range(1,len(row)):
            octave = SPN_data_head[j]
            freq, midi = row[j].split(" ")
            # print "octave %r, freq %r, midi %r"%(octave, freq, midi)
            midi = midi[1:-1]
            midi_data_table[midi] = {"SPN": SPN_note+octave, "freq": freq}
    return midi_data_table

def get_instrument_data(instrument):
    midi_data_table = get_midi_data_table()
    i_data    = None
    shortname = instrument.find("shortName")
    longname  = instrument.find("longName")
    if (shortname is not None) and (longname is not None):
        i_id   = instrument.attrib['id'].replace("-", "_")
        i_data = (
            { "@id": "Instrument/%s"%(i_id,)
            , "@type":
                [
                "micat:Instrument",
                "annal:EntityData"
                ]
            })
        i_data["rdfs:label"]   = longname.text
        description = instrument.find("description")
        if description is not None:
            description_text = description.text
        else:
            description_text = ""
        i_data["rdfs:comment"] = (
            """## %s\n\n%s"""%(
                longname.text,
                description_text
                )
            )
        i_data["annal:id"]      = i_id
        i_data["annal:type"]    = "micat:Instrument"
        i_data["annal:type_id"] = "Instrument"
        musicXMLid_elem = instrument.find("musicXMLid")
        if musicXMLid_elem is not None:
            i_data["micat:InstrumentTypeId"] = (
                 "micat:musicXMLid/%s"%(musicXMLid_elem.text,)
                 )
        else:
            i_data["micat:InstrumentTypeId"] = ""
        noterange_elem = instrument.find("aPitchRange")
        if noterange_elem is not None:
            noterange = noterange_elem.text
            lonote, hinote = noterange.split("-")
        else:
            lonote, hinote = "", ""
        i_data["sofa:minMidi"]  = lonote
        i_data["sofa:maxMidi"]  = hinote
        i_data["sofa:minNote"]  = ""
        i_data["sofa:maxNote"]  = ""
        i_data["sofa:minPitch"] = ""
        i_data["sofa:maxPitch"] = ""
        if lonote in midi_data_table:
            i_data["sofa:minNote"]  = midi_data_table[lonote]["SPN"]
            i_data["sofa:maxNote"]  = midi_data_table[hinote]["SPN"]
        if hinote in midi_data_table:
            i_data["sofa:minPitch"] = midi_data_table[lonote]["freq"]
            i_data["sofa:maxPitch"] = midi_data_table[hinote]["freq"]
    return i_data

def save_instrument_entity(i_data):
    i_text  = json.dumps(i_data, indent=4, sort_keys=True)
    dirname = i_data["@id"]
    try:
        os.makedirs(dirname)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise
    filename = os.path.join(dirname, "entity_data.jsonld")
    with open(filename, "w") as f:
        f.write(i_text)
    return

def main():
    tree = ET.parse('musescore-instruments.xml')
    root = tree.getroot()
    count = 0
    for instrument in root.iter("Instrument"):
        print("##### %s"%(instrument.attrib['id'],))
        i_data = get_instrument_data(instrument)
        if i_data:
            # i_text = json.dumps(i_data, indent=4, sort_keys=True)
            save_instrument_entity(i_data)
            # print (i_text)
            count += 1
    print("Number of instruments: %d"%(count,))


if __name__ == "__main__":
    main()
