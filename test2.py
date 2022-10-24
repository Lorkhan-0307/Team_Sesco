from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys, cv2, numpy, time

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("cam")
        self.setGeometry(150, 150, 650, 540)
        self.initUI()
        self.show()

    def initUI(self):
        # create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)


        self.cpt = cv2.VideoCapture(0)
        self.fps = 24
        self.sens = 300
        _, self.img_o = self.cpt.read()
        self.img_o = cv2.cvtColor(self.img_o, cv2.COLOR_RGB2GRAY)
        cv2.imwrite('img_o.jpg', self.img_o)

        self.cnt = 0

        self.frame = QLabel(self)
        self.frame.resize(640, 480)
        self.frame.setScaledContents(True)
        self.frame.move(5, 5)

        self.btn_on = QPushButton("Cam_Video", self)
        self.btn_on.resize(100 , 25)
        self.btn_on.move(5, 490)
        self.btn_on.clicked.connect(self.start)

        self.btn_off = QPushButton("Cam_off", self)
        self.btn_off.resize(100, 25)
        self.btn_off.move(5+100+5, 490)
        self.btn_off.clicked.connect(self.stop)

        # self.btn_file = QPushButton("file_open", self)
        # self.btn_file.resize(100, 25)
        # self.btn_file.move(5+100+5+100+5, 490)
        # self.btn_file.clicked.connect(self.open_file)

        self.prc = QLabel(self)
        self.prt.resize(200, 25)
        self.prt.move(5+105+105, 490)

        self.sldr = QSlider(Qt.Horizontal, self)
        self.sldr.resize(100, 25)
        self.sldr.move(5+105+105+200, 490)
        self.sldr.setMinimum(1)
        self.sldr.setMaximum(30)
        self.sldr.setValue(24)
        self.sldr.valueChanged.connect(self.setFps)

        self.sldr = QSlider(Qt.Horizontal, self)
        self.sldr.resize(100, 25)
        self.sldr.move(5 + 105 + 105 + 200 + 105, 490)
        self.sldr.setMinimum(50)
        self.sldr.setMaximum(500)
        self.sldr.setValue(300)
        self.sldr.valueChanged.connect(self.setSens)
        self.show()


    def setFps(self):
        self.fps = self.sldr.value()
        self.prt.setText("FPS " + str(self.fps) + "조정!" )
        self.timer.stop()
        self.timer.start(1000./ self.fps)

    def setSens(self):
        self.sens = self.sldr.value()
        self.prt.setText("FPS " + str(self.fps) + "조정!" )


    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000. / self.fps)

    def nextFrameSlot(self):
        _, cam = self.cpt.read()
        cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
        cam = cv2.flip(cam, 0)
        self.img_p = cv2.cvtColor(cam, cv2.COLOR_RGB2GRAY)
        cv2.imwrite('img_p.jpg', self.img_p)
        self.img_o = self.img_p.copy()
        img = QImage(cam, cam.shape[1], cam.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.frame.setPixmap(pix)

    def stop(self):
        self.frame.setPixmap(QPixmap.fromImage(QImage))
        self.timer.stop()


    def compare(self, img_o, img_p):
        err = numpy.sum(img_o.astype('float') - img_p.astype("floate")) ** 2
        err /= float(img_o.shape[0] * img_p.shape[1])
        if(err>=self.sens):
            t = time.loaltime()
            self.prt.setText("{}-{}-{} {}:{}:{}".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))
