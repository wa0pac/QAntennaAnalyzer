# QAntennaAnalyzer
QAntennaAnalyzer is a graphical python program written to interface with the K6BEZ Antenna Analyzer Project.
The code has currently only been tested on Ubuntu Gnome 16.04 and does not have much in the way of error checking or exception handling. Please feel free to add issues or submit changes to improve the code.

After installing dependancies, to execute the application type the following on the command line. 
```
python3 QAntennaAnalyzer.py
```

Dependencies include 
- Python 3
- Pip
- PyQt4
- Matplotlib
- PySerial

## Set up environment to develop QAntennaAnalyzer on Ubuntu 16.04
install pip, pyqt4, matplotlib and pyserial
```
	sudo apt install pip

	sudo apt update
	sudo apt install python3-pyqt4

	sudo apt install python3-matplotlib
	pip3 install pyserial
```

install PyCharm
```
	umake ide pycharm
'''
