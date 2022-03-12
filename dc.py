# Batch converts dcm to png

import pydicom
import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import PySide6

basedir = os.path.dirname("../t2/")

targetdir = os.path.dirname("../t2png/")

patients = os.listdir(basedir)

for patient in patients:
    dirpath = os.path.join(basedir, patient)
    files = os.listdir(dirpath)
    for file in files:
        f = os.path.join(dirpath, file)
        dcm = pydicom.dcmread(f)
        id = dcm.PatientID
        targetpath = os.path.join(targetdir, id)
        if not os.path.exists(targetpath):
            os.mkdir(targetpath)

        # info = {}
        # info["PatientID"] = dcm.PatientID  # 患者ID
        # info["PatientName"] = dcm.PatientName  # 患者姓名
        # # info["PatientBirthData"] = dcm.PatientBirthData # 患者出生日期
        # info["PatientAge"] = dcm.PatientAge  # 患者年龄
        # info['PatientSex'] = dcm.PatientSex  # 患者性别
        # info['StudyID'] = dcm.StudyID  # 检查ID
        # info['StudyDate'] = dcm.StudyDate  # 检查日期
        # info['StudyTime'] = dcm.StudyTime  # 检查时间
        # info['InstitutionName'] = dcm.InstitutionName  # 机构名称
        # info['Manufacturer'] = dcm.Manufacturer  # 设备制造商
        # info['StudyDescription'] = dcm.StudyDescription  # 检查项目描述
        # print(info)

        raw = dcm.pixel_array
        manu = dcm.Manufacturer.split(" ")[0]

        raw_flatten = raw.flatten()
        max_val = max(raw_flatten)
        min_val = min(raw_flatten)
        raw = (raw - min_val) / (max_val - min_val)  # Normalization
        raw = raw * 255
        im = Image.fromarray(raw)

        print(file)
        print(os.path.join(targetpath, file.split(".")[-2] + "_" + manu + ".png"))

        im.convert("RGB").save(os.path.join(targetpath, file.split(".")[-2] + "_" + manu + ".png"), format="png")
