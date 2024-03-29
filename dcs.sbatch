#!/bin/bash
#
#SBATCH --job-name=siumai_10000 # Job name for tracking
#SBATCH --partition=cpu-batch  # Partition you wish to use (see above for list)
#SBATCH --cpus-per-task=1      # Number of CPU threads used by your job, set this upto 40 as required.
#SBATCH --mem-per-cpu=1500     # RAM in MB needed per core (i.e. 1500MB * 40 threads = 60GB RAM)
#SBATCH --time=2-00:00:00      # Job time limit set to 2 days (48 hours)
#
#SBATCH --mail-type=END,FAIL,TIME_LIMIT_80 # Events to send email on, remove if you don't want this
#SBATCH --output=joboutput_%j.out # Standard out from your job
#SBATCH --error=joboutput_%j.err  # Standard error from your job

## Initialisation ##
source /etc/profile.d/modules.sh
source /etc/profile.d/conda.sh

## Execute your program(s) ##
## A Python program

## Rule based
## srun python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 10000 -csv game_history_hhhh -agents h,h,h,h &
## python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 10000 -csv game_history_ssss -agents s,s,s,s &
## python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 10000 -csv game_history_rrrr -agents m,r,r,r

## Monte Carlo
srun python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mmmm_10000 -agents m,m,m,m &
python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mmmh_10000 -agents m,m,m,h &
python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mmhh_10000 -agents m,m,h,h &
python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mhhh_10000 -agents m,h,h,h &
python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mmms_10000 -agents m,m,m,s &
python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mmss_10000 -agents m,m,s,s &
python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 10000 -completed 10000 -csv game_history_msss_10000 -agents m,s,s,s &
python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mmmr_10000 -agents m,m,m,r &
python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mmrr_10000 -agents m,m,r,r &
python3 /dcs/21/u2011915/siu-mai/code/v1/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mrrr_10000 -agents m,r,r,r &
python3 /dcs/21/u2011915/siu-mai/code/v2/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mmmm_10000 -agents m,m,m,m &
python3 /dcs/21/u2011915/siu-mai/code/v2/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mmmh_10000 -agents m,m,m,h &
python3 /dcs/21/u2011915/siu-mai/code/v2/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mmhh_10000 -agents m,m,h,h &
python3 /dcs/21/u2011915/siu-mai/code/v2/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mhhh_10000 -agents m,h,h,h &
python3 /dcs/21/u2011915/siu-mai/code/v2/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mmms_10000 -agents m,m,m,s &
python3 /dcs/21/u2011915/siu-mai/code/v2/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mmss_10000 -agents m,m,s,s &
python3 /dcs/21/u2011915/siu-mai/code/v2/metrics.py -save y -n 10000 -completed 10000 -csv game_history_msss_10000 -agents m,s,s,s &
python3 /dcs/21/u2011915/siu-mai/code/v2/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mmmr_10000 -agents m,m,m,r &
python3 /dcs/21/u2011915/siu-mai/code/v2/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mmrr_10000 -agents m,m,r,r &
python3 /dcs/21/u2011915/siu-mai/code/v2/metrics.py -save y -n 10000 -completed 10000 -csv game_history_mrrr_10000 -agents m,r,r,r 


