#!/usr/bin/python3

import os
import sys

rfiles = []

__version__ = 1.0
__author__ = "lvlrk"

usage = f"""{sys.argv[0]} [-d] [DIRECTORY]
     --help        print this help message and exit
     --version     print version information and exit
 -d, --different   search for non-recognized files in [DIRECTORY]"""

if len(sys.argv) < 2:
    print(usage)
    exit(1)

different = False
directory = "."

for i in range(len(sys.argv)):
    if sys.argv[i] == "-d" or sys.argv[i] == "--different":
        different = True
    elif sys.argv[i] == "--help":
        print(usage)
        exit(0)
    elif sys.argv[i] == "--version":
        print(f"{sys.argv[0]}-{__version__} by {__author__}")
        exit(0)
    else:
        directory = sys.argv[i]

# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk(directory):
    path = root.split(os.sep)
    for file in files:
        filepath = f'{"/".join(path)}/{file}'

        with open(filepath, "rb") as f:
            magic = f.read(8)
            f.seek(0)
            smagic = f.read(4)
            f.close()

        cdict = {"filepath": filepath, "path": "/".join(path), "file": file, "type": "data", "magic": magic, "smagic": smagic}

        if smagic == b"VCRA":
            cdict["type"] = "namco museum remix: arcv archive"
        elif smagic == b"SSZL":
            cdict["type"] = "namco museum remix: sszl-compressed file"
        elif magic == b"UKTP162N":
            cdict["type"] = "namco museum remix: ptk effect file"
        elif magic == b"ANP 150 ":
            cdict["type"] = "namco museum remix: anp layout file"
        elif smagic == b"bres":
            cdict["type"] = "wii binary resource archive"
        elif smagic == b"U\xaa8-":
            cdict["type"] = "u8 archive"
        elif file.endswith(".csv") or "CSV" in filepath:
            cdict["type"] = "csv spreadsheet"
        elif smagic == b"RSTM":
            cdict["type"] = "wii binary audio stream file"
        elif smagic == b"RFNT":
            cdict["type"] = "wii binary font file"
        elif smagic == b"RSAR":
            cdict["type"] = "wii binary sound bank file"
        elif magic == b"MAPOOOBJ":
            cdict["type"] = "namco museum remix: map data (OBJ)"
        elif magic == b"MAPOOMAP":
            cdict["type"] = "namco museum remix: map data (MAP)"
        elif magic == b"MAPOOPNL":
            cdict["type"] = "namco museum remix: map data (PNL)"
        elif file.endswith(".emy"):
            cdict["type"] = "namco museum remix: galaga remix: enemy file"
        elif file.endswith(".scn"):
            cdict["type"] = "namco museum remix: galaga remix: scene file"
        elif "BIN" in file or file.endswith("SET_DAT"):
            cdict["type"] = "namco museum remix: pac n roll remix: binary setting file"
        elif file.endswith(".cam"):
            cdict["type"] = "namco museum remix: pac n roll remix: binary camera file"
        elif smagic == b"THP\x00":
            cdict["type"] = "wii binary video file"
        elif "TEXT" in file or file.endswith(".txt"):
            cdict["type"] = "text file"
        elif file.endswith(".sel"):
            cdict["type"] = "wii symbol table"
        elif file.endswith(".rso"):
            cdict["type"] = "wii shared object"
        elif file.endswith(".rel"):
            cdict["type"] = "wii relocatable binary"
        elif file.endswith(".bin"):
            cdict["type"] = "binary file"
        elif "RESIDENT" in file or file == "env0.dat":
            cdict["type"] = "namco museum remix: resident data file"
        elif file.endswith(".tpl"):
            cdict["type"] = "wii image file"
        elif file.endswith(".bnr"):
            cdict["type"] = "wii channel banner animation"
        elif file in sys.argv[0]:
            cdict["type"] = "this program"
        elif smagic == b"GFAC":
            cdict["type"] = "kirbys epic yarn: gfa archive"
        elif smagic == b"BGDT":
            cdict["type"] = "kirbys epic yarn: data archive"
        elif smagic == b"BGST":
            cdict["type"] = "kirbys epic yarn: st archive"
        elif smagic == b"RFNA":
            cdict["type"] = "wii binary font archive"
        elif smagic == b"REFF":
            cdict["type"] = "wii binary effect file"
        elif smagic == b"REFT":
            cdict["type"] = "wii binary effect resource file"
        elif smagic == b"Yaz0":
            cdict["type"] = "wii Yaz0-compressed u8 archive"
        elif smagic == b"STRM":
            cdict["type"] = "super mario galaxy: binary audio stream file"
        elif smagic == b"RARC":
            cdict["type"] = "wii rarc archive"
        elif file.endswith(".aw"):
            cdict["type"] = "super mario galaxy: binary sound bank file"
        elif smagic == b"RKGD":
            cdict["type"] = "mario kart wii: binary time trial ghost file"
        elif smagic == b"RKWD":
            cdict["type"] = "mario kart wii: WadlistR.dat"
        elif smagic == b"ARC\x00":
            cdict["type"] = "super smash bros brawl: PAC archive"

        rfiles.append(cdict)

for rfile in rfiles:
    if different:
        if rfile["type"] == "data":
            print(rfile)
    else:
        print(f'{rfile["filepath"]}: {rfile["type"]}')
