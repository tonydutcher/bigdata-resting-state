#!/bin/bash

masks=(BN_105_2mm BN_106_2mm BN_107_2mm BN_108_2mm BN_187_2mm BN_188_2mm l_hip_ant_2mm r_hip_ant_2mm l_hip_tail_2mm r_hip_tail_2mm)

for mask in ${masks[@]}; do

echo "Running aggregate_connectivity.py -m $mask"
aggregate_connectivity.py -m $mask

done
