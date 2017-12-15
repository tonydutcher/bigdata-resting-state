#!/bin/bash

masks=(BN_105_2mm_r_con-4mm_rsfc BN_106_2mm_r_con-4mm_rsfc BN_107_2mm_r_con-4mm_rsfc BN_108_2mm_r_con-4mm_rsfc BN_187_2mm_r_con-4mm_rsfc BN_188_2mm_r_con-4mm_rsfc l_hip_ant_2mm_r_con-4mm_rsfc r_hip_ant_2mm_r_con-4mm_rsfc l_hip_tail_2mm_r_con-4mm_rsfc r_hip_tail_2mm_r_con-4mm_rsfc)
#masks=(BN_029_2mm_group_rsfc BN_030_2mm_group_rsfc BN_177_2mm_group_rsfc BN_178_2mm_group_rsfc BN_179_2mm_group_rsfc BN_180_2mm_group_rsfc BN_187_2mm_group_rsfc BN_188_2mm_group_rsfc BN_217_2mm_group_rsfc BN_218_2mm_group_rsfc)

for mask in ${masks[@]}; do

echo "Running plot_group_brain.py $mask"
plot_group_brain.py $mask 'rsfc' 'v2' 
#plot_group_brain.py $mask 'non_rsfc' 'v1'

done