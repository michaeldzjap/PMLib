from FDObjNetwork import FDObjNetwork
from FDString import FDString
from FDPlate import FDPlate
from numpy import array

"""a = FDObjNetwork([FDString(202,kappa=0.1,b1=.685698,b2=.000515,boundaryCond='LeftSimplySupportedRightFree'),\
FDString(203,kappa=0.1,b1=.685698,b2=.000515,boundaryCond='LeftSimplySupportedRightFree')],\
array([[1],[1]]),array([[1],[1]]),array([[0.3],[0]]),array([[0.2],[0.]]))"""

"""a = FDObjNetwork([FDString(b1=.858236,b2=.000530,kappa=1e-09),\
FDString(101,b1=.858236,b2=.000541,kappa=1e-09),\
FDString(200,b1=.858236,b2=.002121,kappa=1e-09),\
FDString(201,b1=.858235,b2=.002143,kappa=1e-09)],\
array([[0.,0.2,0,0.3],[0.5,0,0.2,0],[0.7,0.2,0,0.3],[0.,0,0.5,0]]),\
array([[0,1,0,1],[1,0,1,0],[1,1,0,1],[0,0,1,0]]),\
array([[0.5],[0.],[0.],[0.]]),\
array([[0],[0.],[0.4],[0.6]]))"""

"""a = FDObjNetwork([FDPlate(0,100,0.61,0.0062,"AllSidesSimplySupported",1,1),\
FDPlate(0,100,0.61,0.0062,"AllSidesSimplySupported",1,1),\
FDPlate(0,150,0.61,0.0062,"AllSidesSimplySupported",1,1),\
FDPlate(0,200,0.61,0.0062,"AllSidesSimplySupported",1,1)],\
array([[[0.74,0.53],0,0],[[0.12,0.45],[0.87,0.82],0],[0,[0.61,0.49],[0.23,0.78]],[0,0,[0.84,0.34]]]),\
array([[1,0,0],[1,1,0],[0,1,1],[0,0,1]]),\
array([[[0.23,0.77],0,0,0],[0,[0.32,0.64],0,0],[0,0,[0.49,0.27],0],[0,0,0,[0.57,0.67]]]),\
array([[[0.41,0.31],[0.41,0.31],0,0,0],[[0.74,0.14],0,[0.74,0.14],0,0],[[0.12,0.63],0,0,[0.12,0.63],0],\
[[0.33,0.78],0,0,0,[0.33,0.78]]]))"""

"""a = FDObjNetwork([FDPlate(50,15,0.31,0.0032,"AllSidesSimplySupported",2,1),\
FDString(278,0.8,0.62,0.0062,"BothSimplySupported"),\
FDString(346,0.6,0.62,0.0062,"BothSimplySupported"),\
FDString(392,0.4,0.62,0.0062,"BothSimplySupported"),\
FDString(422,0.2,0.62,0.0062,"BothSimplySupported"),\
FDString(468,0.2,0.62,0.0062,"BothSimplySupported"),\
FDString(522,0.1,0.62,0.0062,"BothSimplySupported"),\
FDPlate(100,45,0.31,0.0032,"AllSidesSimplySupported",2,1)],\
array([[[0.69324522018433,0.37769627571106],0,[0.17801229953766,0.63850489854813],0,[0.1092128276825,0.60866134166718],0,[0.39991699457169,0.49936369657516],0,[0.79874020814896,0.23207870721817],0,[0.7727711558342,0.1962097287178],0],\
[0.0001,1,0,0,0,0,0,0,0,0,0,0],\
[0,0,0.0001,1,0,0,0,0,0,0,0,0],\
[0,0,0,0,0.0001,1,0,0,0,0,0,0],\
[0,0,0,0,0,0,0.0001,1,0,0,0,0],\
[0,0,0,0,0,0,0,0,0.0001,1,0,0],\
[0,0,0,0,0,0,0,0,0,0,0.0001,1],\
[0,[0.7698256611824,0.20680885314941],0,[0.67281718254089,0.78421717882156],0,[0.37481219768524,0.48550273180008],0,[0.34726183414459,0.50783618688583],0,[0.5338115811348,0.49133831262589],0,[0.74707589149475,0.54565798044205]]]),\
array([[1,0,1,0,1,0,1,0,1,0,1,0],\
[1,1,0,0,0,0,0,0,0,0,0,0],\
[0,0,1,1,0,0,0,0,0,0,0,0],\
[0,0,0,0,1,1,0,0,0,0,0,0],\
[0,0,0,0,0,0,1,1,0,0,0,0],\
[0,0,0,0,0,0,0,0,1,1,0,0],\
[0,0,0,0,0,0,0,0,0,0,1,1],\
[0,1,0,1,0,1,0,1,0,1,0,1]]),\
array([[0,0,0,0,0,0],[0.77510565519333,0,0,0,0,0],\
[0,0.40025804042816,0,0,0,0],\
[0,0,0.61174936294556,0,0,0],\
[0,0,0,0.4783195734024,0,0],\
[0,0,0,0,0.59414782524109,0],\
[0,0,0,0,0,0.69618312120438],\
[0,0,0,0,0,0]]),\
array([[[0.1470809340477,0.28775855302811],0,0,0,0,0,0,0],\
[0,0,0.43420165777206,0,0,0,0,0],\
[0,0,0,0.70914711952209,0,0,0,0],\
[0,0,0,0,0.57941033840179,0,0,0],\
[0,0,0,0,0,0.76575038433075,0,0],\
[0,0,0,0,0,0,0.63076648712158,0],\
[0,0,0,0,0,0,0,0.22677526473999],\
[0,[0.32830913066864,0.4558664560318],0,0,0,0,0,0]])
)"""

a = FDObjNetwork([FDPlate(0,20,0.61,0.0015,"AllSidesClamped",1,1),\
FDString(100,0.3,0.698698,0.001515,"BothClamped"),\
FDPlate(0,50,0.61,0.0015,"AllSidesClamped",1,1)],\
array([[[0.74,0.53],0],[0.45,0.82],[0,[0.61,0.49]]]),\
array([[1,0],[5,5],[0,1]]),\
array([[[0.23,0.77],0,0],[0,0.32,0],[0,0,[0.49,0.27]]]),\
array([[[0.41,0.31],[0.41,0.31],0,0,0,0],[0,0,0.74,0.14,0,0],[0,0,0,0,[0.12,0.63],[0.33,0.78]]])\
)

beta = a.calcModes()
coefs = a.calcBiquadCoefs()

#print a.readoutPointMatrix.shape,a.excPointMatrix.shape

#for _a1 in coefs['a1'][0,0]: print _a1

"""file = open('modalData.txt','w')

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
writeArrToFile(beta['sigma'],file); file.write('\n&\n')
write3DArrToFile(coefs['a1'],file); file.write('\n&\n')
write3DArrToFile(coefs['a2'],file); file.write('\n&\n')
writeArrToFile(coefs['b1'],file); file.write('\n&\n')
writeArrToFile(coefs['b2'],file); file.write('\n&\n%6.3f' % network.calcTime)
file.close()"""
