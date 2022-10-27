# Check the MOFs selected by doscar_parser.py turn on SPIN or not

import numpy as np
import json
import pandas as pd


with open("files/mofs_with_peaks") as f:
    mofs_peak = [l.split()[0] for l in f.readlines()]

with open("qmof.json") as file:
    qmof_data = json.load(file)
    qmof_df = pd.json_normalize(qmof_data).set_index("qmof_id")

for m in mofs_peak:
    dos_path = "files/EIDyjluDQ3eZnt-gI7Fc4Q/vasp_files/%s/DOSCAR" %m
    with open(dos_path) as file:
        lines = file.readlines()
        dos_data = np.array([[float(x) for x in l.split()] for l in lines[6:6+nedos]])
    if dos_data.shape[1]>3:
        print(m, " : ", dos_data.shape[1])