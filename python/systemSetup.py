from numpy import array,nonzero
from math import pi
from FDObjNetwork import FDObjNetwork
from FDString import FDString
from FDPlate import FDPlate
import os,sys

file = open('networkArgs.txt','r')
args = file.readlines()
objs = eval(args[0]); connPointMatrix = eval(args[1]); massRatioMatrix = eval(args[2])
excPointMatrix = eval(args[3]); readoutPointMatrix = eval(args[4]); gain = eval(args[5])
file.close()

network = FDObjNetwork(objs,connPointMatrix,massRatioMatrix,excPointMatrix,readoutPointMatrix)
beta = network.calcModes(); coefs = network.calcBiquadCoefs(gain)

#path = os.path.abspath(os.path.dirname(sys.argv[0]))
file = open('modalData.txt','w')

def writeArrToFile(arr,fl):
    fl.write('[')
    for row,i in zip(arr,xrange(0,arr.shape[0])):
        if i < arr.shape[0]-1:
            fl.write('%14.9f, ' % row)
        else:
            fl.write('%14.9f]' % row)

def write2DArrToFile(arr,fl):
    fl.write('[')
    for col,j in zip(arr,range(0,arr.shape[0])):
        writeArrToFile(col,fl)
        if j < arr.shape[0]-1:
            fl.write(',\n')
        else:
            fl.write(']')

def write3DArrToFile(arr,fl):
    if arr.shape[0] > 1 and arr.shape[1] > 1:
        fl.write('[')
        for matr,i in zip(arr,range(0,arr.shape[0])):
            fl.write('[')
            for row,j in zip(matr,range(0,matr.shape[0])):
                writeArrToFile(row,fl)
                if j < matr.shape[0]-1:
                    fl.write(',\n')
                else:
                    if i < arr.shape[0]-1:
                        fl.write('],\n')
                    else:
                        fl.write(']')
        fl.write(']')
    elif arr.shape[0] == 1 and arr.shape[1] > 1:
        write2DArrToFile(arr[0,:,:],fl)
    elif arr.shape[0] > 1 and arr.shape[1] == 1:
        write2DArrToFile(arr[:,0,:],fl)
    else:
        writeArrToFile(arr[0,0,:],fl)

writeArrToFile(beta['freq'],file); file.write('\n&\n')
writeArrToFile(beta['t60'],file); file.write('\n&\n')
write3DArrToFile(coefs['a1'],file); file.write('\n&\n')
write3DArrToFile(coefs['a2'],file); file.write('\n&\n')
writeArrToFile(coefs['b1'],file); file.write('\n&\n')
writeArrToFile(coefs['b2'],file); file.write('\n&\n%6.3f' % network.calcTime)
file.close()
