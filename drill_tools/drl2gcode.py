#!/usr/bin/env python3

import argparse
import sys

import yaml


config = None
with open('drill.cfg') as f:
  
    config = yaml.load(f, Loader=yaml.FullLoader)
    print(config)

parser = argparse.ArgumentParser(
    description="This program converts Excellon .drl files into G-Code for a CNC machine. Originally by Franco Lanza."
)
parser.add_argument("drlfile", metavar="DRLFILE", nargs=1, help="Excellon .drl file")

parser.add_argument(
    "-s",
    "--single-file",
    help="Do not split drill files on separate gcodes by diameters",
    action="store_true",
)

parser.add_argument(
    "-o",
    "--offset",
    help="Offset all coordinates, X Y",
    nargs=2,
    type=float,
    default=[0, 0],
)

args = parser.parse_args()
print(args)
header = (
"""; select absolute coordinate system
G90
; metric
G21
; G61 exact path mode was requested but not implemented
""" +
"G0 Z" + str(config['safe_move_z']) + " F" + str(config['fast_move_z_speed']) + '\r\n' +
"G0 X" + str(config['tool_change_place']['x']) +" F" + str(config['fast_move_xy_speed']) + '\r\n' +
"""
; start spindle
M3
"""
)

footer = (
    """
; go tool change point
""" + 
"G1 Z" + str(config['safe_move_z']) + " F" + str(config['fast_move_z_speed']) + '\r\n' +
"M5" + '\r\n'
"G0 X" + str(config['tool_change_place']['x']) +" F" + str(config['fast_move_xy_speed']) + '\r\n' +
"G0 Y" + str(config['tool_change_place']['y']) +" F" + str(config['fast_move_xy_speed']) + '\r\n' +
"""
; program ends
M2
"""
)


tools = {}
tsel = "1"

move_z_up_line = "".join(["G1 F", str(config['fast_move_z_speed']), " Z" + str(config['safe_move_z'])])
move_z_down_line = "".join(["G1 F", str(config['drill_params']['drilling_speed_down']), " Z" + str(config["drill_params"]["drill_move_z"])])

first_drill = True
with open(args.drlfile[0]) as fp:
    line = fp.readline()
    while line:
        line = fp.readline()
        # Means this line is "tool pool" section
        if line.startswith("T") and "C" in line:
            tnum = line.split("C")[0][1:]
            if "F" in line:
                tnum = line.split("F")[0][1:]
            diameter = "{:.2f}".format(float(line.split("C")[1]))
            tools[tnum] = {
                "diameter": diameter,
                "file": "".join(
                    [
                        args.drlfile[0][:-4],
                        "_T",
                        tnum.rjust(2, "0"),
                        "_",
                        diameter,
                        "mm",
                        ".gcode",
                    ]
                ),
                "output": "".join(
                    [
                        "\n\n; T",
                        tnum,
                        " Diameter: ",
                        diameter,
                        "mm",
                        "\n",
                        "M06\n",
                        "M117 insert d= ",
                        diameter,
                        "mm",
                        "\n",
                    ]
                ),
                "first": True,
            }
        # Tool select section
        elif line.startswith("T"):
            tsel = line[1:].rstrip("\r\n")
            tsel = tsel.lstrip("0") # Remove leading zeros in the beginning
            print(tools)
            first_drill = True
        elif line.startswith("X") and tsel != "0":
            newl1 = "".join(
                ["G1 F", str(config['fast_move_z_speed']), " Z", str(config['drill_params']['between_drill_z'])]
            )
            # Do not move z low for the first drill at the beginning
            if first_drill:
                newl1 = ''
                first_drill = False
            x = float(line.split("Y")[0].strip("X")) + config['workpiece_offset']['x']
            y = float(line.split("Y")[1].strip("\r\n")) + config['workpiece_offset']['y']
            # print(x, y)
            newl2 = "".join(
                [
                    "G1 F",
                    str(config['fast_move_xy_speed']),
                    " X",
                    str(x),
                    " Y",
                    str(y),
                ]
            )

            tools[tsel]["output"] += "\n".join([newl1, newl2, move_z_down_line, ""])

if args.single_file:
    out_file = "".join([args.drlfile[0][:-4], "_Tall.gcode"])
    output = header
    for t in tools:
        output += tools[t]["output"]
    output += footer
    with open(out_file, "w") as f:
        f.write(output)
    print("Writtent to %s" % out_file)

else:
    for t in tools:
        tools[t]["output"] = "".join([header, tools[t]["output"], footer])
        print("writing", tools[t]["file"])
        with open(tools[t]["file"], "w") as f:
            f.write(tools[t]["output"])
