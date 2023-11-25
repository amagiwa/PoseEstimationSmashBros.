# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import time

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

    #ここまでテンプレ
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

class Cam_Kp:
    def __init__(self):
        # Read frames on camera
        self.cap = cv2.VideoCapture(0)
        # Process and display images
        # 解析結果とfpsを表示
        self.fps_time = 0
        
    def update(self):
            datum = op.Datum()
            ret, imageToProcess = self.cap.read()
            imageToProcess = cv2.flip(imageToProcess, 1)
            cv2.putText(imageToProcess,
                "FPS: %f" % (1.0 / (time.time() - self.fps_time)),
                (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 0), 2)
            datum.cvInputData = imageToProcess
            opWrapper.emplaceAndPop(op.VectorDatum([datum]))
            self.fps_time = time.time()
            #print("Body keypoints: \n" + str(datum.poseKeypoints))
            if not args[0].no_display:
                cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
                cv2.waitKey(1)
            if datum.poseKeypoints is None:
                return None
            return datum.poseKeypoints[0]
