#!/bin/bash
#SBATCH --nodes 1
#SBATCH --ntasks-per-node 8
#SBATCH --cpus-per-task 1
#SBATCH --mem 32000
#SBATCH --time 48:00:00

module purge

srun /home/xiazhang/anaconda3/envs/ml/bin/python procar_parser.py