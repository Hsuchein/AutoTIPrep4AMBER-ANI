#!/bin/bash
#SBATCH --job-name=xujian
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


