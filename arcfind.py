#!/usr/bin/python3

import os
import sys
import subprocess

rfiles = []

__version__ = "1.2"
__author__ = "lvlrk"

usage = f"""{sys.argv[0]} [-df] [DIRECTORY]
     --help        print this help message and exit
     --version     print version information and exit
 -d, --different   search for non-recognized files in [DIRECTORY]
 -f, --file        identify singular file instead of DIRECTORY"""

filem = False

if len(sys.argv) < 2:
    print(usage)
    exit(1)

different = False
directory = "."

for i in range(len(sys.argv)):
    if sys.argv[i] == "-d" or sys.argv[i] == "--different":
        different = True
    if sys.argv[i] == "-f" or sys.argv[i] == "--file":
        filem = True
    elif sys.argv[i] == "--help":
        print(usage)
        exit(0)
    elif sys.argv[i] == "--version":
        print(f"{sys.argv[0]}-{__version__} by {__author__}")
        exit(0)
    else:
        directory = sys.argv[i]

def identify(filepath):
    with open(filepath, "rb") as f:
        magic = f.read(8)
        f.seek(0)
        smagic = f.read(4)
        f.close()

    file = os.path.basename(filepath)
    cdict = {"filepath": filepath, "file": file, "type": "data", "magic": magic, "smagic": smagic}

    if smagic == b"VCRA":
        cdict["type"] = "Namco Museum Remix Arcv archive"
    elif smagic == b"SSZL":
        cdict["type"] = "Namco Museum Remix lzss compressed file"
    elif magic == b"UKTP162N":
        cdict["type"] = "Namco Museum Remix PTK binary effect file"
    elif magic == b"ANP 150 ":
        cdict["type"] = "Namco Museum Remix ANP binary UI-layout file"
    elif smagic == b"bres":
        cdict["type"] = "Wii binary resource archive"
    elif smagic == b"U\xaa8-":
        cdict["type"] = "U8 archive"
    elif smagic == b"RSTM":
        cdict["type"] = "Wii binary audio stream file"
    elif smagic == b"RFNT":
        cdict["type"] = "Wii binary font file"
    elif smagic == b"RSAR":
        cdict["type"] = "Wii binary sound bank file"
    elif magic == b"MAPOOOBJ":
        cdict["type"] = "Namco Museum Remix Map object data"
    elif magic == b"MAPOOMAP":
        cdict["type"] = "Namco Museum Remix Map data"
    elif magic == b"MAPOOPNL":
        cdict["type"] = "Namco Museum Remix Binary map panel data"
    elif file.endswith(".emy"):
        cdict["type"] = "Namco Museum Remix Binary enemy pattern data"
    elif file.endswith(".scn"):
        cdict["type"] = "Namco Museum Remix Binary Scene data"
    elif "BIN" in file or file.endswith("SET_DAT"):
        cdict["type"] = "Namco Museum Remix Binary level-setting data"
    elif file.endswith(".cam"):
        cdict["type"] = "Namco Museum Remix Binary camera data"
    elif smagic == b"THP\x00":
        cdict["type"] = "Wii binary video file"
    elif "TEXT" in file or file.endswith(".txt"):
        cdict["type"] = "ASCII Text"
    elif file.endswith(".sel"):
        cdict["type"] = "Wii binary symbol table"
    elif file.endswith(".rso"):
        cdict["type"] = "Wii shared object"
    elif file.endswith(".rel"):
        cdict["type"] = "Wii relocatable binary"
    elif "RESIDENT" in file or file == "env0.dat":
        cdict["type"] = "Namco Museum Remix Shared resource file"
    elif file.endswith(".tpl"):
        cdict["type"] = "Wii TPL image data"
    elif file.endswith(".bnr"):
        cdict["type"] = "Wii channel banner animation"
    elif smagic == b"GFAC":
        cdict["type"] = "Kirby's Epic Yarn GFA archive"
    elif smagic == b"BGDT":
        cdict["type"] = "Kirby's Epic Yarn Data archive"
    elif smagic == b"BGST":
        cdict["type"] = "Kirby's Epic Yarn ST archive"
    elif smagic == b"RFNA":
        cdict["type"] = "Wii binary font archive"
    elif smagic == b"REFF":
        cdict["type"] = "Wii binary effect file"
    elif smagic == b"REFT":
        cdict["type"] = "Wii binary effect resource archive"
    elif smagic == b"Yaz0":
        cdict["type"] = "Wii Yaz0 compressed U8 archive"
    elif smagic == b"STRM":
        cdict["type"] = "Super Mario Galaxy Binary audio stream file"
    elif smagic == b"RARC":
        cdict["type"] = "Wii RARC archive"
    elif file.endswith(".aw"):
        cdict["type"] = "Super Mario Galaxy Binary sound bank file"
    elif smagic == b"RKGD":
        cdict["type"] = "Mario Kart Wii Binary time trial ghost file"
    elif smagic == b"ARC\x00":
        cdict["type"] = "Super Smash Bros. Brawl PAC archive"
    else:
        p = subprocess.run(["file", filepath], capture_output=True, text=True)
        if p.stdout != f'{filepath}: data':
            cdict["type"] = p.stdout.strip("\n").split(": ")[1]

    return cdict

if filem == False:
    for root, dirs, files in os.walk(directory):
        path = root.split(os.sep)
        for file in files:
            filepath = f'{"/".join(path)}/{file}'

            rfiles.append(identify(filepath))
else:
    rfiles.append(identify(directory))

for rfile in rfiles:
    if different:
        if rfile["type"] == "data":
            print(rfile)
            #print(rfile)
    else:
        print(f'{rfile["filepath"]}: {rfile["type"]}')
