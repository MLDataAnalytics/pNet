# This python file is to run a pNet job
# created on 12/22/2024, 09:59:14

import sys
import os

dir_pnet = '/cbica/home/fanyo/pNet/src/pnet'
sys.path.append(dir_pnet)
import pnet

dir_pnet_result = '/cbica/home/fanyo/COORDINATE_MDD/CoordMDD_20241220'

pnet.run_gFN_Visualization(dir_pnet_result)

