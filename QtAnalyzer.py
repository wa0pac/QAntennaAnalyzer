import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import serial
import numpy as np # numerical analysis package

class AntennaAnalyzer(object):
  """ A class for interacting with the Antenna Analyzer
  
  Attributes:
  startFrequency: A string representing the frequency to begin scanning
  endFrequency: A string representing the frequency to stop scanning
  numSteps: A string representing the number of steps to sample between the 
    startFrequency and the endFrequency
  comPort: Com Port of the serial interface
  baudRate: baud rate of the serial interface
  """
  def __init__(self, startFrequency=1000000, endFrequency = 30000000, numSteps = 100):
    self.startFrequency = startFrequency
    self.endFrequency = endFrequency
    self.numSteps = numSteps
    self.comPort = '/dev/ttyACM0'
    self.baudRate = 115200

    
  def setStartFrequency(self, frequency):
    self.startFrequency = frequency
    
  def getStartFrequency(self):
    return self.startFrequency

  def setEndFrequency(self, frequency):
    self.endFrequency = frequency
    
  def getEndFrequency(self):
    return self.endFrequency
    
  def setNumSteps(self, numSteps):
    self.numSteps = numSteps
    
  def getNumSteps(self):
    return self.numSteps
    
  def setComPort(self, comPort):
    self.comPort = comPort
  
  def getComPort(self):
    return self.comPort
    
  def setBaudRate(self, baudRate):
    self.baudRate = baudRate
    
  def getBaudRate(self):
    return self.baudRate
    
  def sweep(self):
    # build the commands for the SWR analyzer
    start_freq =  "%08d" % self.startFrequency + "A"
    end_freq   =  "%08d" %self.endFrequency   + "B"
    steps      =  "%04d" %self.numSteps   + "N"

    ser = serial.Serial(self.comPort, baudrate = self.baudRate)


    ser.write(start_freq) # set start frequency
    ser.write(end_freq)   # set end freq
    ser.write(steps)      # set number of steps
    ser.write("S")        # start sweep
    
    self.frequencyArray = np.empty(self.numSteps)
    self.vswrArray = np.empty(self.numSteps)

    for i in range(self.numSteps): # setup loop over number of points
      in_string = ser.readline() # read a line from the Arduino

      # parse the input string to obtain freq and swr, convert to MHz and swr
      # these values could be loaded in arrays for fancy plot and analysis
      freq_swr_string = in_string.split(",") # break the comma-separated input string
      self.frequencyArray[i] = np.float(freq_swr_string[0])/1.e6
      self.vswrArray[i]     = np.float(freq_swr_string[1])/1.e3 # voltage readings are 2 and 3
  
    ser = serial.Serial.close # close the  port
    
class Window(QtGui.QMainWindow):

  def __init__(self):
    super(Window,self).__init__()
    #self.setGeometry(50,50,500,300)
    self.setWindowTitle("QtAnalyzer")
		# todo - create icon
		# self.setWindowIcon(QtGui.QIcon("???"))

    self.aa = AntennaAnalyzer()
    
    
    
		# Set up Actions
    exitAction = QtGui.QAction("E&xit", self)
    exitAction.setShortcut("Ctrl+Q")
    exitAction.setStatusTip("Exit the Application")
    exitAction.triggered.connect(self.close_application)
		
		#Set up MenuBar
    mainMenu = self.menuBar()
    fileMenu = mainMenu.addMenu("&File")
    fileMenu.addAction(exitAction)

		#Set up StatusBar
    self.statusBar()

    self.create_main_window_layout()
	
  def create_main_window_layout(self):
    #this is the initial layout of the window
    
    #create Band Drop Down menu
    self.bandComboBox = QtGui.QComboBox(self)
    self.bandComboBox.addItem("10m")
    self.bandComboBox.addItem("12m")
    self.bandComboBox.addItem("15m")
    self.bandComboBox.addItem("17m")
    self.bandComboBox.addItem("20m")
    self.bandComboBox.addItem("30m")
    self.bandComboBox.addItem("40m")
    self.bandComboBox.addItem("60m")
    self.bandComboBox.addItem("80m")
    self.bandComboBox.addItem("160m")
    self.bandComboBox.addItem("Full Sweep")
    #self.bandComboBox.move(50,100)
    self.bandComboBox.activated[str].connect(self.band_choice)

    #Sweep Button
    self.sweepButton = QtGui.QPushButton("Sweep", self)
    self.sweepButton.clicked.connect (self.send_sweep)
    self.sweepButton.resize(self.sweepButton.minimumSizeHint())
    #self.sweepButton.move(50,50)

    # Field Labels
    self.startLabel = QtGui.QLabel('Start Frequency',self)
    self.endLabel = QtGui.QLabel('End Frequency',self)
    self.stepsLabel= QtGui.QLabel('Steps',self)
 
    # fields
    self.startEdit = QtGui.QLineEdit(self)
    #self.startEdit.move(170,130)
    self.endEdit = QtGui.QLineEdit(self)
    #self.endEdit.move(170,160)
    self.stepsEdit = QtGui.QLineEdit(self)
    #self.stepsEdit.move(170, 190)

    # Create layout to hold the widgets
    self.initial_layout =  QGridLayout()
    self.initial_layout .addWidget(self, self.startLabel, 0, 0)
    self.initial_layout .addWidget(self, self.endLabel, 1, 0)
    self.initial_layout .addWidget(self, self.stepLabel, 2, 0)
    self.initial_layout .addWidget(self, self.startEdit, 0, 1)
    self.initial_layout .addWidget(self, self.endEdit, 1, 1)
    self.initial_layout .addWidget(self, self.stepEdit, 2, 1)
    
    self.selection_widget = QWidget()
    self.selection_widget.setLayout(self.initial_layout)
    
    self.setCentralWidget(self.selection_widget)

  def home(self):
		#Band Drop Down
    BandComboBox = QtGui.QComboBox(self)
    BandComboBox.addItem("10m")
    BandComboBox.addItem("12m")
    BandComboBox.addItem("15m")
    BandComboBox.addItem("17m")
    BandComboBox.addItem("20m")
    BandComboBox.addItem("30m")
    BandComboBox.addItem("40m")
    BandComboBox.addItem("60m")
    BandComboBox.addItem("80m")
    BandComboBox.addItem("160m")
    BandComboBox.addItem("Full Sweep")
    BandComboBox.move(50,100)
    BandComboBox.activated[str].connect(self.band_choice)

    #Sweep Button
    sweepButton = QtGui.QPushButton("Sweep", self)
    sweepButton.clicked.connect (self.send_sweep)
    sweepButton.resize(sweepButton.minimumSizeHint())
    sweepButton.move(50,50)

    startLabel = QtGui.QLabel('Start Frequency',self)
    startLabel.move(50,130)
    startLabel.resize(startLabel.minimumSizeHint())
    endLabel = QtGui.QLabel('End Frequency',self)
    endLabel.move(50,160)
    endLabel.resize(endLabel.minimumSizeHint())
    stepsLabel= QtGui.QLabel('Steps',self)
    stepsLabel.move(50,190)
    stepsLabel.resize(stepsLabel.minimumSizeHint())

    startEdit = QtGui.QLineEdit(self)
    startEdit.move(170,130)
    endEdit = QtGui.QLineEdit(self)
    endEdit.move(170,160)
    stepsEdit = QtGui.QLineEdit(self)
    stepsEdit.move(170, 190)



    self.show()

  def close_application(self):
    sys.exit()

  def send_sweep(self):
    self.aa.sweep()

  def band_choice(self, text):
    self.bandChoice = text
		

def main():
  app = QtGui.QApplication(sys.argv)
  mainWindow = Window()
  mainWindow.show()
  mainWindow.raise_()
  app.exec_()
  
  sys.exit(app.exec_())


if __name__ == "__main__":
  main()
