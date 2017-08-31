import numpy as np

aMaxPhyPacketSize = 2047 # The maximum PSDU size (in octets) the PHY shall be able to receive
preamble = np.array([0,1,0,1,0,1,0,1], dtype=int)
SFD = np.array([0,1,1,1,0,0,0,0,1,1,1,0,1,1,1,0,1,1,0,1,0,0,1,0], dtype=int)
lambda_PHR = 4
lambda_PSDU = 6
n_PHR = 44 # nDepth (nPhr = 4*11)
n_PSDU = 72 # nDepth (nPsdu = 6*12)
spreading_alternating_0 = np.array([0,1], dtype=int)
spreading_alternating_1 = np.array([1,0], dtype=int)
spreading_non_alternating8_0 = np.array([1,0,1,1,0,0,0,1], dtype=int)
spreading_non_alternating8_1 = np.array([0,1,0,0,1,1,1,0], dtype=int)
spreading_non_alternating16_0 = np.array([0,0,1,0, 0,0,1,1, 1,1,0,1, 0,1,1,0], dtype=int)
spreading_non_alternating16_1 = np.array([1,1,0,1, 1,1,0,0, 0,0,1,0, 1,0,0,1], dtype=int)

preamble_FSK =  np.array([-1, 1, -1, 1, -1, 1, -1, 1], dtype=int)
SFD_FSK = np.array([-1,  1,  1,  1, -1, -1, -1, -1,  1,  1,  1, -1,  1,  1,  1, -1,  1,  1, -1,  1, -1, -1,  1, -1], dtype=int)