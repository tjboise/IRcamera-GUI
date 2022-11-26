from PyQt5.QtWidgets import QApplication, QMessageBox,QPushButton
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import matplotlib.pyplot as plt
from util import damage_density_func, predict
import numpy as np
import traceback
from PIL import Image


class Stats:

    def __init__(self):
        # input UI
        self.ui = uic.loadUi("ui/IR.ui")
        #push button
        self.ui.pushButton.clicked.connect(self.inputIR)
        self.ui.input_visual.clicked.connect(self.inputv)

        self.ui.process.clicked.connect(self.processIR)
        self.ui.horizontalSlider.valueChanged.connect(self.valuechange)
        self.ui.horizontalSlider_2.valueChanged.connect(self.valuechange2)
        self.ui.pushButton_2.clicked.connect(self.open_video)
        self.timer_camera = QTimer()
        self.ui.pushButton_3.clicked.connect(self.Btn_Start)
        self.ui.pushButton_4.clicked.connect(self.Btn_Stop)
        self.ui.pushButton_5.clicked.connect(self.inputcrack)
        self.ui.pushButton_6.clicked.connect(self.detectcrack)


    def Btn_Start(self):

        self.timer_camera.start(25)
        self.timer_camera.timeout.connect(self.OpenFrame)

    def Btn_Stop(self):
        self.timer_camera.stop()

    def open_video(self):
        openfile_name = QFileDialog.getOpenFileName(None,'open file', './')

        self.file_name = openfile_name[0]
        # suffix = self.file_name.split("/")[-1][self.file_name.split("/")[-1].index(".") + 1:]

        if self.file_name == '':
            pass
        else:
            self.cap = cv2.VideoCapture(self.file_name)
            self.ui.label_13.setText(str(format('Success input video')))
            self.ui.label_13.setScaledContents(True)

    def OpenFrame(self):
        ret, image = self.cap.read()
        if ret:
            if len(image.shape) == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                vedio_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            elif len(image.shape) == 1:
                vedio_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_Indexed8)
            else:
                vedio_img = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)

            self.ui.label_13.setPixmap(QPixmap(vedio_img))
            self.ui.label_13.setScaledContents(True)  # 自适应窗口
        else:
            self.cap.release()
            self.timer_camera.stop()


    def start_setting(self):
        pitch_path = './logo/pitch.jpeg'
        boisestate_path = './logo/boisestate.jpeg'

        self.ui.label_10.setPixmap(QPixmap(pitch_path))
        self.ui.label_10.setScaledContents(True)
        self.ui.label_11.setPixmap(QPixmap(boisestate_path))
        self.ui.label_11.setScaledContents(True)


    def inputIR(self):
        try:
            self.IR_path = QFileDialog.getOpenFileName(None,'open file', './')[0]
            img = cv2.imread(self.IR_path)
            self.IR_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # image = QImage(self.IR_img.data, self.IR_img.shape[1], self.IR_img.shape[0], QImage.Format_RGB888)
            # self.ui.label.setPixmap(QPixmap.fromImage(image))
            self.ui.label.setPixmap(QPixmap(self.IR_path))
            self.ui.label.setScaledContents(True)
        except:
            pass

    def inputcrack(self):
        try:
            self.crack_path = QFileDialog.getOpenFileName(None,'open file', './')[0]
            img = cv2.imread(self.crack_path)
            self.crack_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.ui.label_12.setPixmap(QPixmap(self.crack_path))
            self.ui.label_12.setScaledContents(True)
        except:
            pass

    def inputv(self):
        try:
            self.visual_path = QFileDialog.getOpenFileName(None, 'open file', './')[0]
            self.visual_img = cv2.cvtColor(cv2.imread(self.visual_path), cv2.COLOR_BGR2RGB)
            # image = QImage(self.visual_img.data, self.visual_img.shape[1], self.visual_img.shape[0], QImage.Format_RGB888)
            # self.ui.label_3.setPixmap(QPixmap.fromImage(image))
            self.ui.label_3.setPixmap(QPixmap(self.visual_path))
            self.ui.label_3.setScaledContents(True)
        except:
            pass

    def processIR(self):
        img, self.damage_density, self.IR_seg,erosion, gm0, gm = damage_density_func.damage_density(self.IR_path)


        img2 = cv2.cvtColor(self.IR_seg, cv2.COLOR_BGR2RGB)
        # image = QImage(img2.data, img2.shape[1], img2.shape[0], QImage.Format_RGB888)
        image = QImage(img2.data, img2.shape[1], img2.shape[0],img2.strides[0],QImage.Format_RGB888)
        self.ui.label_13.setPixmap(QPixmap.fromImage(image))
        self.ui.label_13.setScaledContents(True)
        self.ui.label_2.setText(str(format(self.damage_density, '.5f')))
        self.ui.label_2.setScaledContents(True)

    def detectcrack(self):
        self.model_path = 'util/best_model.pth'
        save_path = 'data/crack_demo_predict.jpg'
        img3 = predict.crack_segment(self.crack_path,self.model_path,save_path)

        self.ui.label_13.setPixmap(QPixmap(save_path))
        self.ui.label_13.setScaledContents(True)


    def valuechange(self):
        segimg = cv2.cvtColor(self.IR_seg, cv2.COLOR_BGR2RGB)

        rawimg = cv2.resize(self.IR_img,(segimg.shape[1],segimg.shape[0]))

        finalimg =self.ui.horizontalSlider.value()/100*rawimg+(100-self.ui.horizontalSlider.value())/100*segimg
        finalimg = finalimg.astype(np.uint8)
        finalimg = np.clip(finalimg,0,255)
        image1 = QImage(finalimg.data, finalimg.shape[1], finalimg.shape[0],finalimg.strides[0], QImage.Format_RGB888)
        self.ui.label_13.setPixmap(QPixmap.fromImage(image1))
        self.ui.label_13.setScaledContents(True)
        self.ui.label_2.setText(str(format(self.damage_density, '.5f')))
        self.ui.label_2.setScaledContents(True)

    def valuechange2(self):
        # visual + IR
        IR_img = cv2.resize(self.IR_img,(self.visual_img.shape[1],self.visual_img.shape[0]))
        finalimg =self.ui.horizontalSlider_2.value()/100*IR_img+(100-self.ui.horizontalSlider_2.value())/100*self.visual_img
        finalimg = finalimg.astype(np.uint8)
        finalimg = np.clip(finalimg,0,255)
        image2 = QImage(finalimg.data, finalimg.shape[1], finalimg.shape[0],finalimg.strides[0], QImage.Format_RGB888)
        # self.ui.IR_processed.clear()
        self.ui.label_13.setPixmap(QPixmap.fromImage(image2))
        self.ui.label_13.setScaledContents(True)


app = QApplication([])
stats = Stats()
stats.start_setting()
stats.ui.show()

app.exec_()