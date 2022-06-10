#########################################################
##                                                     ##
##  Program Name: vna.py                               ##
##                                                     ##
##  Python programming example for CMT VNA             ##
##                                                     ##
##  Author: Ben Maxson, Copper Mountain Technologies   ##
##      ben.m@coppermountaintech.com                   ##
##                                                     ##
##  Support:  support@coppermountaintech.com           ##
##                                                     ##
#########################################################
##  Program Description: This example demonstrates how ##

##   to connect to the instrument, configure a         ##
##   measurement, retrieve a result, and store it to   ##
##   file.  Measurements are collected in a loop which ##
##   runs num_iter times.                              ##
##                                                     ##
#########################################################

# Allows communication via COM interface
try:
	import win32com.client
except:
	print("You will first need to import the pywin32 extension")
	print("to get COM interface support.")
	print("Try http://sourceforge.net/projects/pywin32/files/ )?")
	input("\nPress Enter to Exit Program\n")
	exit()

# Allows time.sleep() command
import time

###########################
#
#  Input parameters
#
instrument = "TR1300"			#"S5048","S7530","Planar804","Planar304",
							#  "S8081" (Planar808/1), "R54", "R140",
							#  "TR1300", "TR5048", or "TR7530"
use_center_and_span = 0		#false = use fstart/fstop, true = use center/span
power_level_dbm  = 0		#dBm power level (ignored for R54/140)
f1_hz = 400e6               #fstart=400e6 or center, as per above, in Hz
f2_hz = 600e6               #fstop=600e6 or span, as per above, in Hz
num_points = 401			#number of measurement points
parameter = "S21"			#"S21", "S11", "S12", etc. R54/140 must use
							#  "S11"; TR devices must use "S11" or "S21";
							#  Ports 3 and 4 available for S8081 only
format = "mlog" 			#"mlog" or "phase"
time_per_iter_sec = 1		#1.0 seconds per measurement interval
num_iter = 10				#10 number of times to loop
num_iter_to_store = 2		#1 number of function iterations to store

###########################
#
#  Example code
#

#Instantiate COM client
try:
	app = win32com.client.Dispatch(instrument + ".application")
except:
	print("Error establishing COM server connection to " + instrument + ".")
	print("Check that the VNA application COM server was registered")
	print("at the time of software installation.")
	print("This is described in the VNA programming manual.")
	input("\nPress Enter to Exit Program\n")
	exit()

#Wait up to 20 seconds for instrument to be ready
if app.Ready == 0:
    print("Instrument not ready! Waiting...")
    for k in range (1, 21):
        time.sleep(1)
        if app.Ready != 0:
            break
        print("%d" % k)

# If the software is still not ready, cancel the program
if app.Ready == 0:
	print("Error, timeout waiting for instrument to be ready.")
	print("Check that VNA is powered on and connected to PC.")
	print("The status Ready should appear in the lower right")
	print("corner of the VNA application window.")
	input("\nPress Enter to Exit Program\n")
	exit()
else:
    print("Instrument ready! Continuing...")

#Get and echo the instrument name, serial number, etc.
#
#  [This is a simple example of getting an ActiveX property in Python]
#
print(app.name)
	
# Sets the instrument to a preset state
#
#  [This is an example of executing an ActiveX "method" in Python]
#
app.scpi.system.preset()

#Configure the stimulus
if use_center_and_span == 1:
#
#  [This is a simple example of setting an ActiveX property in Python. Note 
#	that when indexed parameters are referenced, the Get prefix and SCPI 
#	 capitalization must be used (e.g. GetSENSe(1) rather than simply sense(1) )]
	app.scpi.GetSENSe(1).frequency.center = f1_hz
	app.scpi.GetSENSe(1).frequency.span = f2_hz
else:
	app.scpi.GetSENSe(1).frequency.start = f1_hz
	app.scpi.GetSENSe(1).frequency.stop = f2_hz

app.scpi.GetSENSe(1).sweep.points = num_points
	
if instrument[0] != "R":
	app.scpi.GetSOURce(1).power.level.immediate.amplitude = power_level_dbm 

#Configure the measurement
app.scpi.GetCALCulate(1).GetPARameter(1).define = "S11"
app.scpi.GetCALCulate(1).GetPARameter(1).select()
app.scpi.GetCALCulate(1).selected.format = "mlog"
app.scpi.trigger.sequence.source = "bus"

for iter in range(1,num_iter):

	#Execute the measurement
	app.scpi.trigger.sequence.single()

	app.scpi.GetCALCulate(1).GetPARameter(1).select()
	Y = app.scpi.GetCALCulate(1).selected.data.Fdata
	
	#Discard complex-valued points
	Y = Y[0::2]

	F = app.scpi.GetSENSe(1).frequency.data

	
	if iter <= num_iter_to_store:
		app.scpi.mmemory.store.image = str(iter) + ".png"
		app.scpi.mmemory.store.fdata = str(iter) + ".csv"
	
	time.sleep(time_per_iter_sec)
		
#Echo last measurement
print("\nFrequency data\n")
print(F)
print("\nMeasurement result\n")
print(Y)

#Wait for a keystroke to exit, so as to 
# keep the VNA application open
raw_input("\nPress Enter to Exit Program\n")
