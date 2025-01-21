# This python file is to run a pNet job
# created on 12/24/2024, 11:21:17

import sys
import os

dir_pnet = '/cbica/home/fanyo/pNet/src/pnet'
sys.path.append(dir_pnet)
import pnet

dir_pnet_result = '/cbica/home/fanyo/nichart/nichart_FN17_20241222'

pnet.run_gFN_Visualization(dir_pnet_result)

