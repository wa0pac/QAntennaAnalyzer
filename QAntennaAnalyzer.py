import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from AntennaAnalyzer import *


import random #for testing

class AnalyzerWindow(QMainWindow):
    """This class creates the main window to interface with the Antenna Analyzer"""

    #constructor
    def __init__(self):
        super().__init__()
        self.bandStart = {'10m': '28.000000',
                          '12m': '24.890000',
                          '15m': '21.000000',
                          '17m': '18.068000',
                          '20m': '14.000000',
                          '30m': '10.100000',
                          '40m': '7.000000',
                          '60m': '5.330500',
                          '80m': '3.500000',
                          '160m':'1.800000',
                          'Full': '1.000000'}

        self.bandEnd =   {'10m': '29.700000',
                          '12m': '24.990000',
                          '15m': '21.450000',
                          '17m': '18.168000',
                          '20m': '14.350000',
                          '30m': '10.150000',
                          '40m': '7.300000',
                          '60m': '5.410000',
                          '80m': '4.000000',
                          '160m': '2.000000',
                          'Full': '30.000000'}

        self.numSteps =   {'10m': '100',
                           '12m': '100',
                           '15m': '100',
                           '17m': '100',
                           '20m': '100',
                           '30m': '100',
                           '40m': '100',
                           '60m': '100',
                           '80m': '100',
                          '160m': '100',
                          'Full': '1000'}

        self.setWindowTitle("Antenna Analyzer")

        self.antennaAnalyzer = AntennaAnalyzer()

        self.create_analyzer_layout()


    def create_analyzer_layout(self):
        #Create MatPlotLib graph
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        #create the plot area layout
        self.plot_layout = QVBoxLayout()
        self.plot_layout.addWidget(self.toolbar)
        self.plot_layout.addWidget(self.canvas)


        #Create Settings widgets
        self.comport_label = QLabel("Com Port")
        self.comport_edit = QLineEdit()

        self.band_label = QLabel("Band")
        self.band_combobox = QComboBox()
        self.band_combobox.addItem('Full')
        self.band_combobox.addItem('10m')
        self.band_combobox.addItem('12m')
        self.band_combobox.addItem('15m')
        self.band_combobox.addItem('17m')
        self.band_combobox.addItem('20m')
        self.band_combobox.addItem('30m')
        self.band_combobox.addItem('40m')
        self.band_combobox.addItem('60m')
        self.band_combobox.addItem('80m')
        self.band_combobox.addItem('160m')
        self.band_combobox.currentIndexChanged.connect(self.band_selection_changed)


        self.start_frequency_label = QLabel("Start Frequency")
        self.start_frequency_edit = QLineEdit()
        self.start_frequency_edit.setInputMask('09.999999')
        self.start_frequency_edit.setValidator(QDoubleValidator(1.0,30.0, 6))
        self.end_frequency_label = QLabel("End Frequency")
        self.end_frequency_edit = QLineEdit()
        self.end_frequency_edit.setInputMask('09.999999')
        self.end_frequency_edit.setValidator(QDoubleValidator(1.0,30.0, 6))
        self.steps_label = QLabel("Number of Steps")
        self.steps_edit = QLineEdit()
        self.steps_edit.setValidator(QIntValidator(1, 9999))
        self.sweep_button = QPushButton("Sweep")
        self.sweep_button.clicked.connect(self.sweep)

        # Create Layout to hold the widgets
        self.settings_layout = QGridLayout()
        self.settings_layout.addWidget(self.comport_label, 0, 0)
        self.settings_layout.addWidget(self.comport_edit, 0, 1)
        self.settings_layout.addItem(QSpacerItem(10,30),1,0)
        self.settings_layout.addWidget(self.band_label, 2, 0)
        self.settings_layout.addWidget(self.band_combobox, 2,1 )
        self.settings_layout.addWidget(self.start_frequency_label, 3,0)
        self.settings_layout.addWidget(self.start_frequency_edit, 3, 1)
        self.settings_layout.addWidget(self.end_frequency_label, 4, 0)
        self.settings_layout.addWidget(self.end_frequency_edit,4, 1)
        self.settings_layout.addWidget(self.steps_label, 5, 0)
        self.settings_layout.addWidget(self.steps_edit, 5, 1)
        self.settings_layout.addWidget(self.sweep_button, 6, 1)

        self.spacing_layout = QVBoxLayout()
        self.spacing_layout.addItem(QSpacerItem(100, 100))

        self.left_layout = QVBoxLayout()
        self.left_layout.addLayout(self.settings_layout, 0)
        self.left_layout.addLayout(self.spacing_layout, 1)

        self.analyzer_layout = QHBoxLayout()
        self.analyzer_layout.addLayout(self.left_layout)
        self.analyzer_layout.addLayout(self.plot_layout, 1)

        self.analyzer_widget = QWidget()
        self.analyzer_widget.setLayout(self.analyzer_layout)

        self.setCentralWidget(self.analyzer_widget)

        #Initialize start and end frequency values and steps
        self.band_selection_changed(0)

    def band_selection_changed(self, i):
        #set Start and End Frequencies
        self.start_frequency_edit.setText(self.bandStart[self.band_combobox.currentText()])
        self.end_frequency_edit.setText(self.bandEnd[self.band_combobox.currentText()])
        self.steps_edit.setText(self.numSteps[self.band_combobox.currentText()])


    def sweep(self):
        self.antennaAnalyzer.setComPort(self.comport_edit.text())
        self.antennaAnalyzer.setBaudRate(115200)
        self.antennaAnalyzer.setStartFrequency(float(self.start_frequency_edit.text()))
        self.antennaAnalyzer.setEndFrequency(float(self.end_frequency_edit.text()))
        self.antennaAnalyzer.setNumSteps(float(self.steps_edit.text()))
        self.antennaAnalyzer.sweep()
        print(self.antennaAnalyzer.getFrequencyList())
        print(self.antennaAnalyzer.getVSWRList())


        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(1000)]

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        #ax.hold(False)

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()




def main():
    analyzer = QApplication(sys.argv)
    analyzerWin = AnalyzerWindow()
    analyzerWin.show()
    analyzerWin.raise_()
    analyzer.exec_()

if __name__ == "__main__":
    main()
