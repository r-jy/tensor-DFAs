import numpy as np
class STP:
	def compute(M,N):
		m,n,p,q = len(M), len(M[0]), len(N), len(N[0])
		s = np.lcm(n,p)
		i1,i2 = s//n,s//p
		I1 = np.identity(i1)
		I2 = np.identity(i2)
		MI = np.kron(M,I1)
		NI = np.kron(N,I2)
		return np.matmul(MI,NI)