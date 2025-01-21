#!/bin/sh

# This bash script is to run a pNet job in the desired cluster environment
# created on 12/22/2024, 09:59:14

# Use command to submit this job:
# $ sbatch --parsable --propagate=NONE --time=2-00:00:00 --ntasks-per-node=4 --mem=20G --output=/cbica/home/fanyo/COORDINATE_MDD/CoordMDD_20241220/Group_FN/cluster_job_visualization.log /cbica/home/fanyo/COORDINATE_MDD/CoordMDD_20241220/Group_FN/cluster_job_visualization.sh

source activate /cbica/home/fanyo/.conda/envs/fmripnet

echo -e "Start time : `date +%F-%H:%M:%S`\n" 

/cbica/home/fanyo/.conda/envs/fmripnet/bin/python /cbica/home/fanyo/COORDINATE_MDD/CoordMDD_20241220/Group_FN/cluster_job_visualization.py

echo -e "Finished time : `date +%F-%H:%M:%S`\n" 
