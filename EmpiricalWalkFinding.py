import timeit
import AcceptingStringGenerator
import TensorGenerator, TensorGenerator2, STP, SwapMatrix
import numpy as np
import matplotlib.pyplot as plt

global tens, tens1, LENGTH

tens = TensorGenerator.TensorGenerator(2,3) # 2 states
print(tens.tensor)
print(tens.accept)

tens1 = TensorGenerator2.TensorGenerator(2,3)
tens1.tensor = []
tens1.accept = tens.accept
tentemp = tens.tensor
for symbolMat in tens.tensor:
    transSymMat = np.transpose(symbolMat)
    tens1.tensor.append(transSymMat)

tens1.STM = np.concatenate(tens1.tensor, 1)
tens1.swappedSTM = STP.STP.compute(tens1.STM, SwapMatrix.SwapMatrix.getMatrix(tens1.state, tens1.symbol))

trialNum = 10
tKate = [0 for i in range(trialNum)]
tJonan = [0 for i in range(trialNum)]
length = [0]
for i in range(1,trialNum):
    length.append(i)
    LENGTH = i
    AcceptingStringGenerator.STRING_LENGTH = LENGTH
    tKate[i] = timeit.timeit('import AcceptingStringGenerator; AcceptingStringGenerator.count_wrapper(tens)', number=2, globals = globals())
    tJonan[i] = timeit.timeit('for acceptState in tens1.accept: tens1.pathAlgorithm(LENGTH, 0, acceptState)', number=2, globals = globals())
    print(str(i)+"terms")
    print("Kate: "+str(tKate[i]))
    print("Jonan: "+str(tJonan[i]))
print(tKate)
print(tJonan)

plt.plot(tKate)
plt.plot(tJonan)

