import numpy

class SwapMatrix:
    def getMatrix(A, B):
        m = len(A)
        n = len(A[0])
        r = len(B)
        q = len(B[0])
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
                print(rmt)
                mrt = numpy.matmul(mj, rit)
                print(mrt)
                print(numpy.kron(rmt,mrt))
                k = numpy.add(k, numpy.kron(rmt, mrt))
        return k