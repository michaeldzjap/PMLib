from FDPlate import FDPlate

a = FDPlate(0,500,.4117698,.031115,boundaryCond='AllSidesSimplySupported',epsilon=1,nu=1)
a.calcUpdateMatrices()
print a.B.shape
