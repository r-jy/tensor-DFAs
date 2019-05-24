import numpy

class SwapMatrix:
    def getMatrix(m, r):
        k = numpy.zeros((r*m, r*m))
        for i in range(r):
            for j in range(m):
                rit = [numpy.zeros(r)]
                rit[0][i]=1
                ri = numpy.transpose(rit)
                mjt = [numpy.zeros(m)]
                mjt[0][j]=1
                mj = numpy.transpose(mjt)
                rmt = numpy.matmul(ri, mjt)
                mrt = numpy.matmul(mj, rit)
                k = numpy.add(k, numpy.kron(rmt, mrt))
        return k