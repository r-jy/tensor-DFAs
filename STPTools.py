import numpy

def STPVector(row, column):
    bigger = []  # 1 = row bigger; ends as row, 0 = column bigger; ends as column
    rowMultiplied = []
    columnMultiplied = []
    if len(row) > len(column) or len(row) == len(column):
        bigger = 1
        rowMultiplied = row
        columnMultiplied = column
        if len(row) % len(column) != 0:
            print("failed")
            return
    else:
        bigger = 0
        rowMultiplied = column
        columnMultiplied = row
        if len(column) % len(row) != 0:
            print("failed")
            return
    print(rowMultiplied)
    numpy.lcm
    print(columnMultiplied)
    partitionSize = len(rowMultiplied)//len(columnMultiplied)
    numPartitions = len(columnMultiplied)
    partitionArray = [numpy.multiply(rowMultiplied[i:i + partitionSize], columnMultiplied[i//partitionSize]) for i in range(0, len(rowMultiplied), partitionSize)]
    return numpy.asarray(partitionArray).sum(axis=0)
