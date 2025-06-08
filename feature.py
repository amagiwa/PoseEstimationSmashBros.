import sys
import cv2
import os
import argparse
import numpy as np

try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../../bin/python/openpose/Release');
        os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
        import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Flags
    parser = argparse.ArgumentParser()
    #parser.add_argument("--image_dir", default="../examples/media/", help="Process a directory of images. Read all standard formats (jpg, png, bmp, etc.).")
    parser.add_argument("--no_display", default=False, help="Enable to disable the visual display.")
    parser.add_argument("--number_people_max", type=str, default=1)
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../../models/"

    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()
except Exception as e:
    print(e)
    sys.exit(-1)

class Feature:
    def __init__(self):
        self.rng = 400
        self.n_bin = 16

    def subVec2(self,vo,vt):
        v = np.zeros(2)
        v[0] = vt[0] - vo[0]
        v[1] = vt[1] - vo[1]
        return v
    
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
        for i in range(len(camKp)):
            for j in range(len(camKp)):
                v = self.subVec2(camKp[i],camKp[j])
                f.append(self.vec2Bin(v))
        return np.array(f)

    def describe(self,filename):
        img = cv2.imread(filename,cv2.IMREAD_COLOR)
        datum = op.Datum()
        datum.cvInputData = img
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        return self.compute(datum.poseKeypoints[0])
    
if __name__=="__main__":
    feat = Feature()
    features = []
    for i in range(1,feat.rng+1):
        filename = "data/img_%03d.png" % i
        print(filename)
        vec = feat.describe(filename)
        features.append(vec)
    for i in range(9901, 10000+1):
        filename = "data/img_%03d.png" % i
        print(filename)
        vec = feat.describe(filename)
        features.append(vec)
    X_train = np.array(features)
    outFilename = "X_train"
    np.save(outFilename,X_train)
