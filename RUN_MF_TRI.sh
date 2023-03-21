#!/bin/bash -l

#SBATCH -J MF_TRIAD
#SBATCH --account=project_2000611
#SBATCH -o error/my_output_%j
#SBATCH -e error/my_output_err_%j
#SBATCH -t 004:15:00
#SBATCH --cpus-per-task=2
#SBATCH -p serial 
#SBATCH --partition=small
#SBATCH --mem-per-cpu=16G
#SBATCH -N 11
#SBATCH -n 11
#SBATCH --mail-type=END
#SBATCH --mail-type=ALL
#SBATCH --mail-user=kyle.eyvindson@luke.fi


module load geoconda

srun -J "Preparing optimization model"  -N 1 -n 1 python Python/MF_TRIANGLE_First.py

wait 

wait

srun -J "MAX_0"  -N 1 -n 1 python Python/MF_TRIANGLE_Second.py --v 0 &
srun -J "MAX_0.1"  -N 1 -n 1 python Python/MF_TRIANGLE_Second.py --v 0.1 &
srun -J "MAX_0.2"  -N 1 -n 1 python Python/MF_TRIANGLE_Second.py --v 0.2 &
srun -J "MAX_0.3"  -N 1 -n 1 python Python/MF_TRIANGLE_Second.py --v 0.3 &
srun -J "MAX_0.4"  -N 1 -n 1 python Python/MF_TRIANGLE_Second.py --v 0.4 &
srun -J "MAX_0.5"  -N 1 -n 1 python Python/MF_TRIANGLE_Second.py --v 0.5 &
srun -J "MAX_0.6"  -N 1 -n 1 python Python/MF_TRIANGLE_Second.py --v 0.6 &
srun -J "MAX_0.7"  -N 1 -n 1 python Python/MF_TRIANGLE_Second.py --v 0.7 &
srun -J "MAX_0.8"  -N 1 -n 1 python Python/MF_TRIANGLE_Second.py --v 0.8 &
srun -J "MAX_0.9"  -N 1 -n 1 python Python/MF_TRIANGLE_Second.py --v 0.9 &
srun -J "MAX_1"  -N 1 -n 1 python Python/MF_TRIANGLE_Second.py --v 1 &

wait 


wait


