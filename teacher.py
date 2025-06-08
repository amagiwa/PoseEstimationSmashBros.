import numpy as np

lbl=[]
c=0
for i in range(100):
    lbl.append(1)
    c+=1
for i in range(100):
    lbl.append(2)
for i in range(100):
    lbl.append(3)
for i in range(100):
    lbl.append(4)
for i in range(100):
    lbl.append(99)
lbl = np.array(lbl)
filename="y_train"
np.save(filename,lbl)
print(c)
