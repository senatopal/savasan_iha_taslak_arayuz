from PyQt5.QtWidgets import  QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt
import json
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = plt.figure(figsize=(4, 4)) 
        self.plot_aircraft_positions()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)  

    def update_plot(self):
        self.plot_aircraft_positions()
        self.canvas.draw()

    def myPlaneCoordinat(self):
        with open('telemetry_response.json', 'r') as f:
            data = json.load(f)
        
        for ucak in data['konumBilgileri']:
            if ucak['takim_numarasi'] == 5:
                kendi_enlem, kendi_boylam = ucak['iha_enlem'], ucak['iha_boylam']
                return kendi_enlem, kendi_boylam
                
    def plot_aircraft_positions(self):
        
        with open('telemetry_response.json', 'r') as f:
            data = json.load(f)

        kendi_enlem, kendi_boylam = self.myPlaneCoordinat()
        uçaklar = {
            "Rakip1": (data['konumBilgileri'][0]['iha_boylam'], data['konumBilgileri'][0]['iha_enlem']),
            "Rakip2": (data['konumBilgileri'][1]['iha_boylam'], data['konumBilgileri'][1]['iha_enlem']),
            "Rakip3": (data['konumBilgileri'][2]['iha_boylam'], data['konumBilgileri'][2]['iha_enlem']),
            "Rakip4": (data['konumBilgileri'][3]['iha_boylam'], data['konumBilgileri'][3]['iha_enlem']),
            "Rakip5": (data['konumBilgileri'][4]['iha_boylam'], data['konumBilgileri'][4]['iha_enlem']),
            "Rakip6": (data['konumBilgileri'][5]['iha_boylam'], data['konumBilgileri'][5]['iha_enlem']),
            "Rakip7": (data['konumBilgileri'][6]['iha_boylam'], data['konumBilgileri'][6]['iha_enlem']),
            "Rakip8": (data['konumBilgileri'][7]['iha_boylam'], data['konumBilgileri'][7]['iha_enlem']),
            "Rakip9": (data['konumBilgileri'][8]['iha_boylam'], data['konumBilgileri'][8]['iha_enlem']),
            "BenimUçağım": (kendi_boylam, kendi_enlem)  
        }

        self.figure.clear()
        ax = self.figure.add_subplot(111)


        airplane_image_path = 'plane.png'  # Burada uygun yolu belirleyin
        my_airplane_image_path = "myplane.png"
        airplane_img = mpimg.imread(airplane_image_path)
        my_airplane_img = mpimg.imread(my_airplane_image_path)


        for uçak, konum in uçaklar.items():
            if uçak == "BenimUçağım":
                imagebox = OffsetImage(my_airplane_img, zoom=0.9)  # Benim uçağım için özel resim
            else:
                imagebox = OffsetImage(airplane_img, zoom=0.9)  # Diğer uçaklar için genel resim

            ab = AnnotationBbox(imagebox, (konum[0], konum[1]), frameon=False, pad=0.1)
            ax.add_artist(ab)
            
            if uçak == "BenimUçağım":
                ax.scatter(float(konum[0]), float(konum[1]), label=uçak, color="red")  # Renk seçebilirsiniz
            else:
                ax.scatter(float(konum[0]), float(konum[1]), label=uçak, color="blue")  # Renk seçebilirsiniz

        ax.set_xlabel('Boylam')
        ax.set_ylabel('Enlem')
        ax.set_title('Uçak Konumları')
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        ax.legend()
        ax.axis('equal')
        ax.set_xlim(36.50, 36.59)  
        ax.set_ylim(41.50, 41.59) 

        ax.set_xticks(np.arange(36.0, 37.5, 0.2))
        ax.set_yticks(np.arange(41.0, 42.5, 0.1))

        self.figure.tight_layout()