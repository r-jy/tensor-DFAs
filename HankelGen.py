import random
import numpy


def hankel_gen():
    lists = []
    lists.append([])
    lists[0].extend(['0','1'])
    for i in range(3):
        lists.append([])
        for j in lists[i]:
            lists[i+1].append(j + '0')
            lists[i+1].append(j + '1')
    list = [x for y in lists for x in y]
    matrix = numpy.zeros((len(list), len(list)))
    for row in range(len(list)):
        for column in range(len(list)):
            matrix[row][column] = int(int('0b' + list[row] + list[column], 2) % 3 == 0)
    return matrix