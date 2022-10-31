# Check the MOFs selected by doscar_parser.py turn on SPIN or not
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def min_max(arr):
    return (arr-np.min(arr))/(np.max(arr)-np.min(arr))

weights = {}
result = []

thre = 0.1

with open("qmof.json") as file:
    qmof_data = json.load(file)
    qmof_df = pd.json_normalize(qmof_data).set_index("qmof_id")

mofs = os.listdir("files/EIDyjluDQ3eZnt-gI7Fc4Q/vasp_files/")
for i in range(len(mofs)):
    dos_path = "files/EIDyjluDQ3eZnt-gI7Fc4Q/vasp_files/%s/DOSCAR" %mofs[i]
    qmof_id = qmof_df[qmof_df["name"] == mofs[i]].index.item()
    bandgap = qmof_df[qmof_df["name"]==mofs[i]]["outputs.pbe.bandgap"].item()
    with open(dos_path) as file:
        lines = file.readlines()
        nions = int(lines[0].split()[1])
        e_info = [float(i) for i in lines[5].split()]
        e_min, e_max, nedos, efermi = e_info[0], e_info[1], int(e_info[2]), e_info[3]
        dos_data = np.array([[float(x) for x in l.split()] for l in lines[6:6+nedos]])
        atom_line_idx = np.array([7+ion_idx+(ion_idx+1)*nedos for ion_idx in range(nions)])
        atom_dos_data = np.array([[[float(x) for x in l.split()] for l in lines[idx:idx+nedos]] for idx in atom_line_idx])
    
    # select data in the bandgap
    dos_data_bg = dos_data[(dos_data[:,0] > efermi) & (dos_data[:,0] < efermi+bandgap)]
    atom_dos_bg = atom_dos_data[(atom_dos_data[:,:,0] > efermi) & (atom_dos_data[:,:,0] < efermi+bandgap)]
    atom_dos_bg = atom_dos_bg.reshape(
        atom_dos_data.shape[0],
        dos_data_bg.shape[0],
        atom_dos_data.shape[2]
    )

    if dos_data_bg.shape[0] == 0:
        # for metal
        peak = 0
        weights.update({qmof_id: np.array([0]*nions).tolist()})
    else:
        # for semiconductors and insulators
        atom_bg_sum = np.sum(atom_dos_bg, axis=2) - atom_dos_bg[:,:,0]
        if dos_data_bg.shape[1] == 3:
            peak = np.sum(dos_data_bg, axis=0)[1]
            if peak == 0:
                weights.update({qmof_id: np.array([0]*nions).tolist()})
            else:
                atom_attr = np.sum(atom_bg_sum, axis=1) / np.sum(dos_data_bg, axis=0)[1]
                if sum(atom_attr < thre) == nions:
                    peak = 0
                    weights.update({qmof_id: np.array([0]*nions).tolist()})
                else:
                    weights.update({qmof_id: min_max(atom_attr).tolist()})
        else:
            peak_up = np.sum(dos_data_bg, axis=0)[1]
            peak_down = np.sum(dos_data_bg, axis=0)[2]
            peak = peak_up + peak_down
            # define the colum index of spin-up and spin-down orbitals
            up = np.array([1,3,5,7,9,11,13,15,17])
            down = np.array([2,4,6,8,10,12,14,16,18])
            if peak_up == 0:
                up_attr = np.array([0]*nions)
            else:
                up_attr = np.sum(np.sum(atom_dos_bg[:,:,up], axis=2), axis=1)/np.sum(dos_data_bg, axis=0)[1]
            
            if peak_down == 0:
                down_attr = np.array([0]*nions)
            else: 
                down_attr = np.sum(np.sum(atom_dos_bg[:,:,down], axis=2), axis=1)/np.sum(dos_data_bg, axis=0)[2]
            
            atom_attr = up_attr + down_attr

            if sum(atom_attr < 2*thre) == nions:
                peak = 0
                weights.update({qmof_id: np.array([0]*nions).tolist()})
            else:
                weights.update({qmof_id: min_max(atom_attr).tolist()})

    result.append({
        "qmof_id": qmof_id,
        "name": mofs[i],
        "dos_in_bandgap": peak
    })
    print(i, ": ", mofs[i], "finished!")

# write atom weights
weights_obj = json.dumps(weights, indent=4)
with open("files/peak_output.json", "w") as file:
    file.write(weights_obj)

# write peak to qmof.json
result_obj = json.dumps(result, indent=4)
with open("files/qmof_update.json", "w") as file:
    file.write(result_obj)