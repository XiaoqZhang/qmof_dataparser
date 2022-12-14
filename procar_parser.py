import os
import json
import numpy as np
import pandas as pd

path = "files/EIDyjluDQ3eZnt-gI7Fc4Q/vasp_files/b1"

def min_max(arr):
    return (arr-np.min(arr))/(np.max(arr)-np.min(arr))

def extract_projection(s):
    # read PROCAR file
    with open(os.path.join(path, s, "PROCAR")) as file:
        lines = file.readlines()
        band_ids = [lines.index(line) for line in lines if "energy" in line]
        ion_num = int(lines[1].split()[-1])
    
    site_atts = []
    for id in band_ids:
        tot = float(lines[id+ion_num+3].split()[-1])
        site_att = [float(line.split()[-1])/tot for line in lines[id+3:id+ion_num+3]]
        site_atts.append(site_att)
    
    # normalization
    ion_weight = min_max(np.mean(site_atts, axis=0))

    # change name to qmof_id
    with open("qmof.json") as file:
        qmof_data = pd.read_json(file)
    if len(qmof_data[qmof_data["name"] == s]["qmof_id"]) != 0:
        s_id = qmof_data[qmof_data["name"] == s]["qmof_id"].item()
    else:
        s_id = s
    print(qmof.index(s), " : ", s_id)

    return {s_id: ion_weight.tolist()}

if __name__ == '__main__':
    qmof = os.listdir(path)
    print("Get structure list. ")
    
    weights = {}
    for q in qmof:
        print(qmof.index(q), end=' : ')
        weights.update(extract_projection(q))

    weights_object = json.dumps(weights, indent=4)
    with open("files/qmof_expl_ref1.json", "w") as file:
        file.write(weights_object)
 