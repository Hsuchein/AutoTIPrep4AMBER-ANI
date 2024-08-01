#!/bin/bash
#SBATCH --job-name=wat_ch008
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=6  ## 1 for gpu job; <=24 for cpu job.
#SBATCH --cluster=gpu        ## gpu, smp
##SBATCH --partition=gtx1080  ## gtx1080, v100, a100, a100_nvlink
##SBATCH --partition=v100     ## gtx1080, v100, a100, a100_nvlink
#SBATCH --partition=a100     ## gtx1080, v100, a100, a100_nvlink
##SBATCH --partition=a100_nvlink  ## gtx1080, v100, a100, a100_nvlink
#SBATCH --time=5-23:59:59    ## 1-00:00:00
#SBATCH --qos=long          ##long (3~6days), normal (1-3days), short (<1day)
##SBATCH --time=1-00:09:00    ## 1-00:00:00
##SBATCH --qos=normal         ##long (3~6days), normal (1-3days), short (<1day)
##SBATCH --time=3-00:09:00    ## 1-00:00:00
##SBATCH --qos=long           ##long (3~6days), normal (1-3days), short (<1day)
##SBATCH --output=myjob.out   ## default output file slurm-<jobid>.out
#SBATCH --exclude=gpu-n28,gpu-n42
#SBATCH --gres=gpu:1         ## only for GPU jobs.

module purge

module load gcc/10.2.0
module load openmpi/4.1.1
module load cuda/12.1

module load cmake/3.27.7
source /ix1/jwang/tan77/xujian/software/amber22/amber.sh
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/ix1/jwang/tan77/xujian/software/amber22_src/build/AmberTools/src/sander
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/ix1/jwang/tan77/xujian/software/amber22_src/AmberTools/libtorch/lib
module load gcc/10.2.0



echo "Water Minimization 1"
mpirun -np 16 /ix1/jwang/tan77/xujian/software/amber22_ori/amber22/bin/sander.MPI -O -i ../mdin/general/wat_min1.in -p ch008_gaff2_wat.prmtop -c crd_wat.inpcrd   -o output_wat_min1.out -r wat_min1.rst
sleep 2
echo "Water Minimization 2"
mpirun -np 16 /ix1/jwang/tan77/xujian/software/amber22_ori/amber22/bin/sander.MPI -O -i ../mdin/general/wat_min2.in -p ch008_gaff2_wat.prmtop -c wat_min1.rst -o output_wat_min2.out -r wat_min2.rst
sleep 2
echo "Water cMD Simulation 1"
mpirun -np 16 /ix1/jwang/tan77/xujian/software/amber22_ori/amber22/bin/sander.MPI -O -i ../mdin/general/wat_md_1.in -p ch008_gaff2_wat.prmtop -c wat_min2.rst -o output_wat_md1.out  -r wat_md1.rst
sleep 2
echo "Water ANI-MD Simulation"
mpirun -np 16 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI -O -i ../mdin/general/wat_md_2.in -p ch008_gaff2_wat.prmtop -c wat_md1.rst  -o output_wat_md2.out  -r md_final_wat.rst
sleep 2
echo "Water Simulation 1"
mpirun -np 16 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 16 -groupfile ./group/wat_s1.group
sleep 2
echo "Water Simulation 2"
mpirun -np 16 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 16 -groupfile ./group/wat_s2.group
sleep 2
echo "Water Simulation 3"
mpirun -np 16 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 16 -groupfile ./group/wat_s3.group
sleep 2
echo "Water Simulation 4"
mpirun -np 16 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 16 -groupfile ./group/wat_s4.group
sleep 2
echo "Water Simulation 5"
mpirun -np 16 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 16 -groupfile ./group/wat_s5.group
sleep 2
echo "Water Simulation 6"
mpirun -np 16 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 16 -groupfile ./group/wat_s6.group
sleep 2
echo "Water Simulation 7"
mpirun -np 16 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 16 -groupfile ./group/wat_s7.group
sleep 2
echo "Water Simulation 8"
mpirun -np 16 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 16 -groupfile ./group/wat_s8.group
sleep 2
echo "Water Simulation 9"
mpirun -np 16 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 16 -groupfile ./group/wat_s9.group
sleep 2