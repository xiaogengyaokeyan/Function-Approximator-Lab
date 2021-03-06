#!/usr/local/bin/python
"""
-----Put your information here-----
	
	authors: "???", "???", "???"
	emails: "???", "???", "???"

-----------------------------------
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import time
import psutil

class fa_lw():
	
	def __init__(self, numberOfFeatures, minDelta=0.00001, maxIteration = 20000):
		"""
		Initialize class member data based on user defined variables.
		
		:param numberOfFeatures: Number of features/basis functions used in the FA.
		:param minDelta: Minimum change between thetas between two consecutive iterations. This is used as a convergence criterion. (Iterative methods only. Defaults to 0.00001)
		:param maxIteration: Maximum number of iterations used for training the FA. (Iterative methods only. Defaults to 20000)
		
		:returns: A function approximator object with the desired variable initializations.
		"""
		
		# Variables pertinent to the core learning algorithms
		self.numFeatures 	= numberOfFeatures 
		self.theta 			= np.zeros((2,self.numFeatures)) #initialize theta vector to appropriate size
		self.maxIter 		= maxIteration
		self.threshold 		= minDelta
		
		# Auxiliary variables used in the class
		self.theta_old 		= np.zeros((2,self.numFeatures))
		self.delta 			= 100
		self.iterationCount = 0
		self.deltaHistory 	= []
		self.cpuHistory 	= []
		self.memHistory 	= []
		self.timeHistory 	= []
		self.trainingTime 	= 0.0
		self.method 		= 'LWLS'
		self.performance()
		self.setCentersAndWidths()
		
		
		
##########################################################################################		
############################### Various Training Methods #################################
##########################################################################################	
	
		
	####################################
	## Locally Weighted Least Squares ##
	####################################
		
	def train_LWLS(self, data):
				
		#Get x and y values separated from 'data'
		xData = data[0,:]
		yData = data[1,:]
		numDataPoints = np.size(xData)
		
						
		t0 = time.time()
		
		#----------------------#		
		## Training Algorithm ##
		#----------------------#
				
		for k in range(self.numFeatures):
		
			self.theta[:,k] = """???"""
		
		#-----------------------------#	
		## End of Training Algorithm ##	
		#-----------------------------#
		
		t1 = time.time()
		self.timeHistory.append(t1 - t0)
		self.performance()
				
	
	
##########################################################################################		
############################ End of Training Method Code #################################
##########################################################################################
 
		
	def setCentersAndWidths(self):
		"""
		Set the center location and width for each basis function assuming the dependent variable
		range is [0,1].
		"""
		xMin = 0.0
		xMax = 1.0
		self.centers = np.linspace(xMin, xMax, self.numFeatures)
		self.widthConstant = (xMax - xMin) / self.numFeatures / 10
		self.widths = np.ones(self.numFeatures,) * self.widthConstant
 
	
	def getWeights(self, input):
		"""
		Get the weights for a given input variable(s)
		
		:param input: A single or vector of dependent variables with size [Ns] for which to calculate the FA features
		
		:returns:   A vector of feature outputs with size [NumFeats x Ns]
		"""
		if np.size(input) == 1:
			W = np.exp(-np.divide(np.square(input - self.centers), self.widths))
		
		elif np.size(input) > 1:
			numEvals = np.shape(input)[0]
			#Repeat vectors to vectorize output calculation
			inputMat = np.array([input,]*self.numFeatures)
			centersMat = np.array([self.centers,]*numEvals).transpose() 
			widthsMat = np.array([self.widths,]*numEvals).transpose() 
			W = np.exp(-np.divide(np.square(inputMat - centersMat), widthsMat))
			
		return W
	
	def featureOutput(self, input):
		"""
		Get the output of the features for a given input variable(s)
		
		:param input: A single or vector of dependent variables with size [Ns] for which to calculate the FA features
		
		:returns: A vector of feature outputs with size [NumFeats x Ns]
		"""		
 		if np.size(input) == 1:
 			phi = np.vstack(([input], [1]))
 			
 		elif np.size(input) > 1:
 			phi = np.vstack((input, np.ones((1,np.size(input)))))
			
		return phi
	
	def functionApproximatorOutput(self, input):
		"""
		Get the FA output for a given input variable(s)
		
		:param input: A single or vector of dependent variables with size [Ns] for which to calculate the FA features
		
		:returns: A vector of function approximator outputs with size [Ns]
		"""
		phi = self.featureOutput(input)
		W = self.getWeights(input)
		if np.size(input) == 1:
			pass
			#fa_out = np.dot(phi, self.theta.transpose())
		elif np.size(input) > 1:
			g = (np.dot(phi.transpose(), self.theta)).transpose() #[numFeats x Ns]
			fa_out = np.sum((W*g), axis=0) / np.sum(W, axis=0)
		return fa_out
		
	
	def calculateDelta(self):
		"""
		Function used to calculate the change in characteristic variables between iterations. 
		Used to estimate the convergence of the iterative learning methods.
		
		:returns: A scalar estimation of the difference between consecutive iterations
		"""
		#delta = math.fabs(np.linalg.norm(self.theta - self.theta_old))
		delta = np.mean(np.abs(self.theta - self.theta_old))
		
		#xData = data[0,:]
		#yData = data[1,:]
		#delta = np.linalg.norm(yData - self.functionApproximatorOutput(xData))
		
		return delta
		
	
	def printStats(self):
		"""
		Print various iteration/convergence statistics during training
		"""
		print 'Iteration: ', self.iterationCount, ' Delta: ', self.delta
		
		
	def performance(self):
		"""
		Get Cpu and RAM usage statistics using the psutil library
		"""
		if psutil.__version__ == '1.1.2':
			self.memHistory.append(psutil.virtual_memory().percent)
			self.cpuHistory.append(psutil.cpu_percent(interval=None, percpu=True))
		else:
			self.memHistory.append([0])
			self.cpuHistory.append([0])
			
			
	
		