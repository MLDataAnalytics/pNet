#!/bin/sh

# This bash script is to run a pNet job in the desired cluster environment
# created on 12/24/2024, 11:21:17

# Use command to submit this job:
# $ sbatch --parsable --propagate=NONE --time=2-00:00:00 --ntasks-per-node=4 --mem=20G --output=/cbica/home/fanyo/nichart/nichart_FN17_20241222/Group_FN/cluster_job_visualization.log /cbica/home/fanyo/nichart/nichart_FN17_20241222/Group_FN/cluster_job_visualization.sh

source activate /cbica/home/fanyo/.conda/envs/fmripnet

echo -e "Start time : `date +%F-%H:%M:%S`\n" 

/cbica/home/fanyo/.conda/envs/fmripnet/bin/python /cbica/home/fanyo/nichart/nichart_FN17_20241222/Group_FN/cluster_job_visualization.py

echo -e "Finished time : `date +%F-%H:%M:%S`\n" 
