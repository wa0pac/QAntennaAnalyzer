import sys
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

    def __init__(self, startFrequency=1000000, endFrequency=30000000, numSteps=100):
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

    def getFrequencyList(self):
        return self.frequencyArray

    def getVSWRList(self):
        return self.vswrArray

    def sweep(self):
        # build the commands for the SWR analyzer
        start_freq = "%08d" % self.startFrequency + "A"
        end_freq = "%08d" % self.endFrequency + "B"
        steps = "%04d" % self.numSteps + "N"

        ser = serial.Serial(self.comPort, baudrate=self.baudRate)

        ser.write(start_freq)  # set start frequency
        ser.write(end_freq)  # set end freq
        ser.write(steps)  # set number of steps
        ser.write("S")  # start sweep

        self.frequencyArray = np.empty(self.numSteps)
        self.vswrArray = np.empty(self.numSteps)

        for i in range(self.numSteps):  # setup loop over number of points
            in_string = ser.readline()  # read a line from the Arduino

            # parse the input string to obtain freq and swr, convert to MHz and swr
            # these values could be loaded in arrays for fancy plot and analysis
            freq_swr_string = in_string.split(",")  # break the comma-separated input string
            self.frequencyArray[i] = np.float(freq_swr_string[0]) / 1.e6
            self.vswrArray[i] = np.float(freq_swr_string[1]) / 1.e3  # voltage readings are 2 and 3

        ser = serial.Serial.close  # close the  port


    def getFrequencyList(self):
        return self.frequencyArray

    def getVSWRList(self):
        return self.vswrArray