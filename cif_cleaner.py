import os

import json
import pandas as pd
import shutil

with open("qmof.json") as file:
    qmof_data = json.load(file)
    qmof_df = pd.json_normalize(qmof_data).set_index("qmof_id")

known_qmof = [k for k in qmof_df["name"]]
raw_qmof = os.listdir("files/EIDyjluDQ3eZnt-gI7Fc4Q/vasp_files/")

for q in raw_qmof:
    if q not in known_qmof:
        print(q)
        shutil.rmtree(os.path.join("files/EIDyjluDQ3eZnt-gI7Fc4Q/vasp_files/", q))
