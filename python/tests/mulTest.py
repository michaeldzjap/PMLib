import numpy as np

#a = np.array([[1,1,1,1,1],[2,2,2,2,2],[3,3,3,3,3]])
#b = np.array([[5,2],[5,2],[5,2],[5,2],[5,2]])
a = np.array([[1,1,1,1,1]])
b = np.array([[5],[5],[5],[5],[5]])
c = np.empty((a.shape[0],b.shape[1],a.shape[1]))

print a; print b
for row,i in zip(a,range(0,c.shape[0])):
    c[i,:,:] = row*b.T
print c