import fsk_lecim_const as cst
import numpy as np

from math import ceil
from cmath import exp, pi

class physical_layer:
	def __init__(self, 
		sps=10, 
		modulation_index=1.0, 
		band_169_MHz=False, 
		phyLecimFskPreambleLength=4, 
		FCS=False, 
		data_whitening=False, 
		PFSK=False, 
		phyLecimFskSpreading = False, phyLecimFskSpreadingAlternating = False, phyLecimFskSpreadingFactor = 2, 
		phyPacketSize=1):
	
		#SHR parameter
		self.preamble = cst.preamble	
		self.SFD = cst.SFD
		#PHR parameter	
		self.phyLecimFskPreambleLength = phyLecimFskPreambleLength
		self.FCS = FCS
		self.data_whitening = data_whitening
		self.phyPacketSize = phyPacketSize if phyPacketSize <= cst.aMaxPhyPacketSize else cst.aMaxPhyPacketSize
		#SHR & PHR generation
		self.SHR = self.gen_SHR()
		self.PHR = self.gen_PHR()
		#interleaver parameter
		self.n_PHR = cst.n_PHR
		self.n_PSDU = cst.n_PSDU
		self.lambda_PHR = cst.lambda_PHR
		self.lambda_PSDU = cst.lambda_PSDU
		self.n_block = int(ceil((8*self.phyPacketSize+6)/(self.n_PSDU/2.0)))
		#spreading
		self.phyLecimFskSpreading = phyLecimFskSpreading
		self.phyLecimFskSpreadingFactor = phyLecimFskSpreadingFactor
		self.phyLecimFskSpreadingAlternating = phyLecimFskSpreadingAlternating
		#zero padding
		self.n_pad = int((self.n_block*(cst.n_PSDU/2))-(8*phyPacketSize+6))
		#modulation
		self.PFSK = PFSK
		self.sps  = sps
		self.modulation_index = modulation_index
		self.band_169_MHz = band_169_MHz
		self.symbol_rate = self.symbol_rate()
		self.freq_dev = self.freq_dev()
		self.SHR_mod = self.SHR_modulator()
		self.preamble_mod = self.SHR_mod[0:len(self.preamble)*self.sps*self.phyLecimFskPreambleLength]
		self.SFD_mod = self.SHR_mod[len(self.preamble)*self.sps*self.phyLecimFskPreambleLength:]
		
	#Compute symbol rate
	def symbol_rate(self):
		if self.band_169_MHz:
			if self.modulation_index == 1:
				R = 12500 #bit/s
				print "Symbol rate is 12.5 kb/s"
			elif self.modulation_index == 0.5:
				R = 25000
				print "Symbol rate is 25 kb/s"
			else:
				raise Exception("Modulation index must be 0.5 or 1.0 for the 169 MHz band")
		else:
			if self.modulation_index == 0.5:
				R = 37500
				print "Symbol rate is 37.5 kb/s"
			elif self.modulation_index == 1.0:
				R = 25000
				print "Symbol rate is 25 kb/s"
			elif self.modulation_index == 2.0:
				R = 12500
				print "Symbol rate is 12.5 kb/s"
			else:
				raise Exception("Modulation index must be 0.5 or 1.0 or 2.0 for bands > 169 MHz band")
		return R		

	#Frequency deviation
	def freq_dev(self):
		freq_dev = (self.modulation_index*self.symbol_rate)/2
		print "Frequency deviation is " + str(freq_dev) + " Hz"
		return freq_dev

	#SHR generator
	def gen_SHR(self):
		if self.phyLecimFskPreambleLength < 4 and self.phyLecimFskPreambleLength > 64:
			raise Exception("Preamble length must be between 4 and 64")
		SHR = np.tile(self.preamble,self.phyLecimFskPreambleLength)
		SHR = np.concatenate((SHR,self.SFD))
		#print SHR
		return SHR

	#PHR generator
	def gen_PHR(self):
		PHR = np.zeros((16, ), dtype=int)
		if self.FCS:
			PHR[12] = 1
		else:
			PHR[12] = 0
		if self.data_whitening:
			PHR[11] = 1
		else:
			PHR[11] = 0
		payl_len_bitstring = '{0:011b}'.format(self.phyPacketSize)
		payl_len_list = [int(payl_len_bitstring[i],2) for i in range(0,len(payl_len_bitstring))]
		PHR[0:11] = np.flipud(payl_len_list)
		parity_bit = PHR[0]
		for i in range(1,13):
			parity_bit = parity_bit^PHR[i]
		PHR[13] = parity_bit
		return PHR

	#SHR modulator for the correaltion estimator 
	def SHR_modulator(self):

	    SHR = np.tile(cst.preamble_FSK,self.phyLecimFskPreambleLength)
	    SHR = np.concatenate((SHR,cst.SFD_FSK))
	    SHR_mod = np.zeros((len(SHR)*self.sps, ), dtype=complex)

	    for i in range(len(SHR)):
	        for k in range(self.sps):
	            SHR_mod[self.sps*i+k] = exp(1j*2*pi*(SHR[i]*self.freq_dev)*(self.sps*i+k)/(self.sps*self.symbol_rate)) 
	  
	    return SHR_mod