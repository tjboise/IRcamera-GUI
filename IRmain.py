from PyQt5.QtWidgets import QApplication, QMessageBox,QPushButton
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import cv2
import matplotlib.pyplot as plt
from util import damage_density_func
import numpy as np

class Stats:
    def __init__(self):
        # 从文件中加载UI定义
        self.ui = uic.loadUi("ui/IR.ui")
        self.ui.pushButton.clicked.connect(self.handleCalc)
        self.ui.process.clicked.connect(self.processIR)
        self.ui.horizontalSlider.valueChanged.connect(self.valuechange)

    def handleCalc(self):
        self.img_path = QFileDialog.getOpenFileName(None,'open file', './')[0]
        # img,damage_density,seg,gm0,gm=damage_density_func.damage_density(img_path)
        # img2 = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        # self.ui.label.setPixmap(QPixmap(gm0))
        # image = QImage(img2.data, img2.shape[1], img2.shape[0], QImage.Format_RGB888)
        img = cv2.imread(self.img_path)
        rawimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = QImage(rawimg.data, rawimg.shape[1], rawimg.shape[0], QImage.Format_RGB888)
        self.ui.label.setPixmap(QPixmap.fromImage(image))

        # self.ui.label.setPixmap(QPixmap(self.img_path))

        self.ui.label.setScaledContents(True)
    def processIR(self):

        img, damage_density, seg, gm0, gm = damage_density_func.damage_density(self.img_path)


        img2 = cv2.cvtColor(seg, cv2.COLOR_BGR2RGB)
        image = QImage(img2.data, img2.shape[1], img2.shape[0], QImage.Format_RGB888)
        self.ui.IR_processed.setPixmap(QPixmap.fromImage(image))

        self.ui.IR_processed.setScaledContents(True)

        self.ui.label_2.setText(str(format(damage_density, '.5f')))
        self.ui.label_2.setScaledContents(True)
    def valuechange(self):
        img, damage_density, seg, gm0, gm = damage_density_func.damage_density(self.img_path)
        img = cv2.imread(self.img_path)
        rawimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        segimg = cv2.cvtColor(seg, cv2.COLOR_BGR2RGB)
        rawimg = cv2.resize(rawimg,(segimg.shape[1],segimg.shape[0]))
        finalimg =self.ui.horizontalSlider.value()/100*rawimg+(100-self.ui.horizontalSlider.value())/100*segimg
        finalimg = finalimg.astype(np.uint8)
        finalimg = np.clip(finalimg,0,255)
        image = QImage(finalimg.data, finalimg.shape[1], finalimg.shape[0], QImage.Format_RGB888)
        self.ui.IR_processed.setPixmap(QPixmap.fromImage(image))
        self.ui.IR_processed.setScaledContents(True)
        self.ui.label_2.setText(str(format(damage_density, '.5f')))
        self.ui.label_2.setScaledContents(True)

app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()