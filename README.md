# PoseEstimationSmashBros.

# これは何？
姿勢推定モデルOpenPoseにより、Nintendo Switch©のゲームをリアルタイムで操作するためのものです。
ポーズ分類のための学習データ(教師データ)を予め作成しておき、カメラに映る人物のポーズに基づいてゲーム機に入力します。

# 使い方
OpenPose(https://github.com/CMU-Perceptual-Computing-Lab/openpose)をビルドし、直下のpythonフォルダでgit cloneします。
OpenPoseの事前学習済みモデルのダウンロードも忘れないようにしてください。

# プログラムの説明
## pose.py
OpenPoseを呼び出すPythonラッパーです。
## cap_data.py
学習データとなる画像を撮影します。
## feature.py
dataフォルダの画像に対して姿勢推定と特徴量抽出を行い、学習データを作成します。
## teacher.py
dataフォルダの画像に対応する教師データを作成します。
## main.py
カメラの映像をもとにした分類結果をArduinoに送信します。
## arduino/sample.ino
main.pyから送信された分類結果のIDに基づいて操作情報をゲーム機に送信します。
