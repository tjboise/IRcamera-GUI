from PyQt5.QtWidgets import QApplication, QMessageBox,QPushButton
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import cv2
import matplotlib.pyplot as plt
from util import damage_density_func
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


        img2 = cv2.cvtColor(gm0, cv2.COLOR_BGR2RGB)
        # image = QImage(img2.data, img2.shape[1], img2.shape[0], QImage.Format_RGB888)
        image = QImage(img2.data, img2.shape[1], img2.shape[0],img2.strides[0],QImage.Format_RGB888)
        self.ui.IR_processed.setPixmap(QPixmap.fromImage(image))
        self.ui.IR_processed.setScaledContents(True)
        self.ui.label_2.setText(str(format(self.damage_density, '.5f')))
        self.ui.label_2.setScaledContents(True)

    def valuechange(self):
        segimg = cv2.cvtColor(self.IR_seg, cv2.COLOR_BGR2RGB)

        rawimg = cv2.resize(self.IR_img,(segimg.shape[1],segimg.shape[0]))

        finalimg =self.ui.horizontalSlider.value()/100*rawimg+(100-self.ui.horizontalSlider.value())/100*segimg
        finalimg = finalimg.astype(np.uint8)
        finalimg = np.clip(finalimg,0,255)
        image1 = QImage(finalimg.data, finalimg.shape[1], finalimg.shape[0],finalimg.strides[0], QImage.Format_RGB888)
        self.ui.IR_processed.setPixmap(QPixmap.fromImage(image1))
        self.ui.IR_processed.setScaledContents(True)
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
        self.ui.IR_processed.setPixmap(QPixmap.fromImage(image2))
        self.ui.IR_processed.setScaledContents(True)


app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()