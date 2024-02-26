#!/bin/bash
#
#SBATCH --job-name=siumai_v1_50 # Job name for tracking
#SBATCH --partition=cpu-batch  # Partition you wish to use (see above for list)
#SBATCH --cpus-per-task=1      # Number of CPU threads used by your job, set this upto 40 as required.
#SBATCH --mem-per-cpu=1500     # RAM in MB needed per core (i.e. 1500MB * 40 threads = 60GB RAM)
# SBATCH --time=2-00:00:00      # Job time limit set to 2 days (48 hours)
#
#SBATCH --mail-type=END,FAIL,TIME_LIMIT_80 # Events to send email on, remove if you don't want this
#SBATCH --output=joboutput_%j.out # Standard out from your job
#SBATCH --error=joboutput_%j.err  # Standard error from your job

## Initialisation ##
source /etc/profile.d/modules.sh
source /etc/profile.d/conda.sh

## Execute your program(s) ##
## A Python program

## V1
## srun python3 /dcs/21/u2011915/siu-mai/code/v1_completed/metrics.py -save y -n 100 -completed 1000 -csv game_history_mmmm_1000 -agents m,m,m,m &
## python3 /dcs/21/u2011915/siu-mai/code/v1_completed/metrics.py -save y -n 100 -completed 1000 -csv game_history_mmms_1000 -agents m,m,m,s &
## python3 /dcs/21/u2011915/siu-mai/code/v1_completed/metrics.py -save y -n 100 -completed 1000 -csv game_history_mmss_1000 -agents m,m,s,s &
## python3 /dcs/21/u2011915/siu-mai/code/v1_completed/metrics.py -save y -n 100 -completed 1000 -csv game_history_msss_1000 -agents m,s,s,s & 
## python3 /dcs/21/u2011915/siu-mai/code/v1_completed/metrics.py -save y -n 100 -completed 100 -csv game_history_mmmm_100 -agents m,m,m,m &
## python3 /dcs/21/u2011915/siu-mai/code/v1_completed/metrics.py -save y -n 100 -completed 100 -csv game_history_mmms_100 -agents m,m,m,s &
## python3 /dcs/21/u2011915/siu-mai/code/v1_completed/metrics.py -save y -n 100 -completed 100 -csv game_history_mmss_100 -agents m,m,s,s &
## python3 /dcs/21/u2011915/siu-mai/code/v1_completed/metrics.py -save y -n 100 -completed 100 -csv game_history_msss_100 -agents m,s,s,s & 
## python3 /dcs/21/u2011915/siu-mai/code/v1_completed/metrics.py -save y -n 100 -completed 500 -csv game_history_mmmm_500 -agents m,m,m,m &
## python3 /dcs/21/u2011915/siu-mai/code/v1_completed/metrics.py -save y -n 100 -completed 500 -csv game_history_mmms_500 -agents m,m,m,s &
## python3 /dcs/21/u2011915/siu-mai/code/v1_completed/metrics.py -save y -n 100 -completed 500 -csv game_history_mmss_500 -agents m,m,s,s &
## python3 /dcs/21/u2011915/siu-mai/code/v1_completed/metrics.py -save y -n 100 -completed 500 -csv game_history_msss_500 -agents m,s,s,s & 
## python3 /dcs/21/u2011915/siu-mai/code/v1_completed/metrics.py -save y -n 100 -completed 50 -csv game_history_mmmm_50 -agents m,m,m,m &
## python3 /dcs/21/u2011915/siu-mai/code/v1_completed/metrics.py -save y -n 100 -completed 50 -csv game_history_mmms_50 -agents m,m,m,s &
## python3 /dcs/21/u2011915/siu-mai/code/v1_completed/metrics.py -save y -n 100 -completed 50 -csv game_history_mmss_50 -agents m,m,s,s &
## python3 /dcs/21/u2011915/siu-mai/code/v1_completed/metrics.py -save y -n 100 -completed 50 -csv game_history_msss_50 -agents m,s,s,s & 



## V2
srun python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 100 -completed 50 -csv game_history_mmmm_50 -agents m,m,m,m &
python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 100 -completed 50 -csv game_history_mmms_50 -agents m,m,m,s &
python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 100 -completed 50 -csv game_history_mmss_50 -agents m,m,s,s &
python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 100 -completed 50 -csv game_history_msss_50 -agents m,s,s,s
