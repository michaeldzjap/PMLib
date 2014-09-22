import os,sys
from numpy import array
from math import pi
from FDObjNetwork import FDObjNetwork
from FDString import FDString
from FDPlate import FDPlate

"""a = FDObjNetwork([FDString(b1=.858236,b2=.000530,kappa=1e-09),\
                  FDString(101,b1=.858236,b2=.000541,kappa=1e-09),\
                  FDString(200,b1=.858236,b2=.002121,kappa=1e-09),\
                  FDString(201,b1=.858235,b2=.002143,kappa=1e-09)],\
                 array([[0.,0.2,0,0.3],[0.5,0,0.2,0],[0.7,0.2,0,0.3],[0.,0,0.5,0]]),\
                 array([[0,1,0,1],[1,0,1,0],[1,1,0,1],[0,0,1,0]]),\
	         array([[0.5],[0.],[0.],[0.]]),\
	         array([[0],[0.],[0.4],[0.6]]))"""

"""a = FDObjNetwork([FDPlate(0,100,0.61,0.0062,"AllSidesSimplySupported",1,1),\
                  FDPlate(0,200,0.61,0.0062,"AllSidesSimplySupported",1,1),\
                  FDPlate(0,400,0.61,0.0062,"AllSidesSimplySupported",1,1),\
                  FDPlate(0,800,0.61,0.0062,"AllSidesSimplySupported",1,1)],\
                  [[[0.74,0.53],0,0],[[0.12,0.45],[0.87,0.82],0],[0,[0.61,0.49],[0.23,0.78]],[0,0,[0.84,0.34]]],\
                  array([[1,0,0],[1,1,0],[0,1,1],[0,0,1]]),\
                  [[[0.23,0.77],0,0,0],[0,[0.32,0.64],0,0],[0,0,[0.49,0.27],0],[0,0,0,[0.57,0.67]]],\
                  [[[0.41,0.31],[0.41,0.31],0,0,0],[[0.74,0.14],0,[0.74,0.14],0,0],[[0.12,0.63],0,0,[0.12,0.63],0],[[0.33,0.78],0,0,0,[0.33,0.78]]])"""

"""a = FDObjNetwork([FDPlate(0,100,0.61,0.0062),FDPlate(0,200,0.61,0.0062)],\
                 [[[0.74,0.53]],[[0.12,0.45]]],array([[1],[1]]),[[[0.23,0.77],0],[0,[0.32,0.64]]],\
                 [[[0.41,0.31],[0.41,0.31],0],[[0.74,0.34],0,[0.74,0.34]]])"""

a = FDObjNetwork([FDString(202,b1=.685698,b2=.000515,boundaryCond='LeftSimplySupportedRightFree'),\
		  FDString(203,b1=.685698,b2=.000515,boundaryCond='LeftSimplySupportedRightFree')],\
                 array([[1],[1]]),array([[1],[1]]),array([[0.3],[0]]),array([[0.2],[0.]]))

"""a = FDObjNetwork([FDPlate(0,100,0.634,0.0034,"AllSidesSimplySupported",1,1),FDPlate(0,200,0.634,0.0034,"AllSidesSimplySupported",1,1)],\
                 [[[0.3,0.6]],[0.7]],array([[ 1 ],[ 1 ]]),[[[0.2,0.2]],[0]],[[[0.5,0.7]],[0]])"""

"""a = FDObjNetwork([FDString(100,i_b1=.685698,i_b2=.000515,i_boundaryCond='LeftSimplySupportedRightFree'),\
          FDString(101,i_b1=.685698,i_b2=.000515,i_boundaryCond='LeftSimplySupportedRightFree'),
          FDString(150,i_b1=.685698,i_b2=.000515,i_boundaryCond='LeftSimplySupportedRightFree')],\
                 array([[1,1],[1,0],[0,1]]),array([[1,1],[1,0],[0,1]]),array([[0.3],[0],[0]]),array([[0.2],[0.],[0]]))"""

"""a = FDObjNetwork([FDString(50,1e-03,.0798698,i_b2=.011515),\
                  FDString(100,1e-04,.079768,i_b2=.011515)],\
                 array([[1],[1]]),array([[1],[1]]),array([[0.3],[0]]),array([[0.6],[0]]))"""

"""a = FDObjNetwork([FDString(100,1,.685698,.000515,'LeftFreeRightSimplySupported'),
                  FDString(101,1,.685698,.000515,'LeftFreeRightSimplySupported')],
                 array([[1],[1]]),array([[1],[100]]),array([[0],[0.3]]),array([[0.2],[0]]))"""

"""a = FDObjNetwork([FDString(100,1,.685698,.000515,'LeftSimplySupportedRightFree'),
                  FDPlate(100,100,.685698,.000515,'AllSidesSimplySupported',1)],
                 [[1],[[0.5,0.5]]],array([[1],[100]]),[[0.3],[0]],[[0],[[0.4,0.8]]])"""

"""a = FDObjNetwork([FDPlateDesc(0,50,0.61,0.0062),FDPlateDesc(0,100,0.61,0.0062)],
[[[0.74,0.53]],[[0.12,0.45]]],array([[1],[50]]),[[[0.23,0.77],0],[0,[0.42,0.84]]],[[[0.41,0.31],[0.41,0.31],0],[[0.74,0.14],0,[0.74,0.14]]]
)"""

"""a = FDObjNetwork([FDString(100,1,.685698,.000515,'LeftSimplySupportedRightFree'),
                  FDPlate(100,100,.685698,.000515,'AllSidesSimplySupported',1)],
                 [[1],[[0.5,0.5]]],array([[1],[1]]),[[0],[[0.4,0.8]]],[[0.3],[0]])"""

"""a = FDObjNetwork([FDPlate(0,300,0.61,0.0062,"AllSidesSimplySupported",1,1),FDString(100,0.8,0.62,0.0062,"BothSimplySupported")],
                 [[[0.807,0.353]],[0.312]],array([[1],[1]]),[[0],[0.607]],[[[0.607,0.303]],[0]])"""

"""a = FDObjNetwork([FDString(200,0.3,0.62,0.0062,"BothSimplySupported"),FDString(100,0.8,0.62,0.0062,"BothSimplySupported")],
                 [[0.56],[0.312]],array([[1],[1]]),[[0],[0.607]],[[0.607],[0]])"""

beta = a.calcModes(); coefs = a.calcBiquadCoefs(63.095734448019)
#print 'approximate time it took to calculate all modes: %3.4f seconds' % a.calcTime
#print beta['freq']; print coefs['b1']; print coefs['b2']
#print coefs['a1']

path =  os.path.abspath(os.path.dirname(sys.argv[0]))
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

writeArrToFile(beta['freq'],file)
file.write('\n&\n')
writeArrToFile(beta['sigma'],file)
file.write('\n&\n')
write3DArrToFile(coefs['a1'],file)
file.write('\n&\n')
write3DArrToFile(coefs['a2'],file)
file.write('\n&\n')
writeArrToFile(coefs['b1'],file)
file.write('\n&\n')
writeArrToFile(coefs['b2'],file)
file.write('\n&\n%6.3f' % a.calcTime)
file.close()
