import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["font.size"] = 17


def dos_checker(s):
    # read bandgap
    with open("qmof.json") as file:
        qmof_data = json.load(file)
        qmof_df = pd.json_normalize(qmof_data).set_index("qmof_id")
        qmof_id = qmof_df[qmof_df["name"] == s].index.item()
        bandgap = qmof_df[qmof_df["name"]==s]["outputs.pbe.bandgap"].item()


    # read DOSCAR file
    with open(os.path.join(path, s, "DOSCAR")) as file:
        lines = file.readlines()
        e_info = [float(i) for i in lines[5].split()]
        e_min, e_max, nedos, efermi = e_info[0], e_info[1], int(e_info[2]), e_info[3]

        dos_data = np.array([[float(x) for x in l.split()] for l in lines[6:6+nedos]])
    
    energies = dos_data[:,0]
    bandgap_data = dos_data[(energies > efermi) & (energies<efermi+bandgap)][:-1]

    # check if there is peaks in the bandgap
    flag = False
    if sum(bandgap_data[:,1]>0) > 0:
        flag = True

    # plot dos
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 6)
    ax.plot(
        energies[(energies>efermi-1) & (energies<efermi+7)]-efermi, 
        dos_data[:, 1][(energies>efermi-1) & (energies<efermi+7)]
    )
    ax.plot([0,0], [0,25], 'r--')
    ax.plot([bandgap, bandgap], [0,25], 'r--')
    ax.set_xlabel("$E-E_{Fermi}\ /\ eV$")
    ax.set_ylabel("Density of states")
    ax.set_title("%s" %qmof_id)
    fig.savefig("files/dos_plots/b1/%s.png" %qmof_id)
    plt.close(fig)

    return flag


if __name__ == '__main__':
    path = "files/EIDyjluDQ3eZnt-gI7Fc4Q/vasp_files/b1"
    qmof = os.listdir(path)
    print("Get structure list. ")
    
    for q in qmof:
        f = dos_checker(q)
        if f == True:
            print(q)
        