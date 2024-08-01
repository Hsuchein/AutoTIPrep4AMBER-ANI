#!/bin/bash
#SBATCH --job-name=gas_ch006
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



echo "Gas Minimization 1"
mpirun -np 1 /ix1/jwang/tan77/xujian/software/amber22_ori/amber22/bin/sander.MPI -O -i ../mdin/general/gas_min.in -p ch006_gaff2_gas.prmtop -c crd_gas.inpcrd   -o output_gas_min1.out -r gas_min1.rst
sleep 2
echo "Gas Simulation 1"
mpirun -np 2 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI -ng 2 -groupfile ./group/gas_s1.group
sleep 2
echo "Gas Simulation 2"
mpirun -np 2 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 2 -groupfile ./group/gas_s2.group
sleep 2
echo "Gas Simulation 3"
mpirun -np 2 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 2 -groupfile ./group/gas_s3.group
sleep 2
echo "Gas Simulation 4"
mpirun -np 2 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 2 -groupfile ./group/gas_s4.group
sleep 2
echo "Gas Simulation 5"
mpirun -np 2 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 2 -groupfile ./group/gas_s5.group
sleep 2
echo "Gas Simulation 6"
mpirun -np 2 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 2 -groupfile ./group/gas_s6.group
sleep 2
echo "Gas Simulation 7"
mpirun -np 2 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 2 -groupfile ./group/gas_s7.group
sleep 2
echo "Gas Simulation 8"
mpirun -np 2 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 2 -groupfile ./group/gas_s8.group
sleep 2
echo "Gas Simulation 9"
mpirun -np 2 /ix1/jwang/tan77/xujian/software/amber22/bin/sander.MPI  -ng 2 -groupfile ./group/gas_s9.group
sleep 2
gzip *.trj
sleep 10