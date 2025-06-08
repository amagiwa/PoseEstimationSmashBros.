from pose import Pose
import cv2
import numpy as np
from sklearn import svm
import serial
import time

class Classify:
    def __init__(self):
        self.pose = Pose()
        self.n_bin = 16

    def subVec2(self,vo,vt):
        v = np.zeros(2)
        v[0] = vt[0] - vo[0]
        v[1] = vt[1] - vo[1]
        return v
    
    def normalizeVec2(self,vec):
        vec[0] /= np.linalg.norm(vec,ord=2)
        vec[1] /= np.linalg.norm(vec,ord=2)
        return vec

    def vec2Rad(self,vec):
        rad = np.arctan(vec[1]/(vec[0]+0.001))
        return rad
    
    def rad2Bin(self,rad):
        rBin = np.pi/self.n_bin
        rad /= rBin
        rad = int(rad)
        return rad
    
    def vec2Bin(self,vec):
        rad = self.vec2Rad(vec)
        return self.rad2Bin(rad)

    def compute(self,camKp):
        f = []
        #print(type(camKp))
        if camKp is None:
            for i in range(625):
                f.append(0)
        else:
            for i in range(len(camKp)):
                for j in range(len(camKp)):
                    v = self.subVec2(camKp[i],camKp[j])
                    f.append(self.vec2Bin(v))
        return np.array([f])

if __name__ == "__main__":
    classify = Classify()
    X_train = np.load("X_train.npy")
    y_train = np.load("y_train.npy")
    ser = serial.Serial()
    ser.port = "COM7"     # デバイスマネージャでArduinoのポート確認
    ser.baudrate = 9600     # Arduinoと合わせる
    ser.setDTR(False)     # DTRを常にLOWにしReset阻止
    ser.open()      
    clf = svm.LinearSVC(random_state=0, tol=1e-1, max_iter=3000, C=100)
    clf.fit(X_train, y_train)
    while 1:
        vec = classify.compute(classify.pose.update())
        lbl = clf.predict(vec)
        poss = clf.decision_function(vec)
        print("Decision: ")
        print(poss[0])
        if lbl[0] < 99 and poss[0][lbl[0]] < 0:
            #lbl[0]=99
            a=0
        s = str(lbl[0])+'0'
        ser.write(bytes(s,'ascii'))
        ser.flush()
        time.sleep(0.3)
        print("Class: %d"%lbl[0])
        print("\n")
        key = cv2.waitKey(1)
        if key==27: break
    ser.close()
    print("end")
