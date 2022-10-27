# Check the MOFs selected by doscar_parser.py turn on SPIN or not
import os
import json
import numpy as np
import pandas as pd

with open("qmof.json") as file:
    qmof_data = json.load(file)
    qmof_df = pd.json_normalize(qmof_data).set_index("qmof_id")

'''
with open("files/mofs_with_peaks") as f:
    mofs_peak = [l.split()[0] for l in f.readlines()]
for m in mofs_peak:
    dos_path = "files/EIDyjluDQ3eZnt-gI7Fc4Q/vasp_files/%s/DOSCAR" %m
    bandgap = qmof_df[qmof_df["name"]==m]["outputs.pbe.bandgap"].item()
'''

mofs = os.listdir("files/EIDyjluDQ3eZnt-gI7Fc4Q/vasp_files/")
for i in range(len(mofs)):
    dos_path = "files/EIDyjluDQ3eZnt-gI7Fc4Q/vasp_files/%s/DOSCAR" %mofs[i]
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

    if dos_data_bg.shape[1] == 3:
        if dos_data_bg[-1, 0] == 0:
            print(i, ": ", m)
        else: print(i)
    else:
        if (dos_data_bg[-1, 0] == 0) & (dos_data_bg[-1, 1] == 0):
            print(i, ": ", m)
        else: print(i)

    '''
    atom_dos_bg = atom_dos_data[(atom_dos_data[:,:,0] > efermi) & (atom_dos_data[:,:,0] < efermi+bandgap)]
    atom_dos_bg = atom_dos_bg.reshape(
        atom_dos_data.shape[0],
        dos_data_bg.shape[0],
        atom_dos_data.shape[2]
    )
    
    # check if there are peaks in the bandgap

    if dos_data.shape[1] > 3:
        dos_sum = np.sum(dos_data[:,1] + dos_data[:,2])
        atom_dos_sum = np.sum(atom_dos_data, axis=2) - atom_dos_data[:,:,0]
        print("Spin on: ", m, ", ", dos_data.shape[1])

    else:
        bandgap_data = dos_data[(dos_data[:,0] > efermi) & (dos_data[:,0]<efermi+bandgap)]
        if 
    '''