#!/bin/bash
#SBATCH --nodes 4
#SBATCH --ntasks-per-node 16
#SBATCH --cpus-per-task 1
#SBATCH --mem 32000
#SBATCH --time 48:00:00

module purge
module load mycompiler
module load mympi

srun /home/xiazhang/anaconda3/envs/ml/bin/python ../procar_parser.py