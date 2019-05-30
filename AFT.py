#run below command
#C:\Python27\python.exe C:\Users\ndhavalikar\Desktop\Allegion_Nand\Personal\GIT\BL_Pic16f-master\test_automation\AFT.py
#C:\Python27\python.exe C:\Users\acer\Desktop\MASTER_DOCUMENT_V1\START_UP\GIT_Repo\Plat_Pic16f\5_Test_Automation\Test_Automation\AFT.py
#give below test templet as input

'''
pre requesit : BLE dongal 
BLE conneted Hardwar
'''
from Tkinter import *
import bluetooth
import csv
import datetime
import time
outpath_file=""
temp_file_data =""
sock = None
bd_addr = None
def DUT_FFR(arg1, arg2, arg3):
	return "PASS"
 
def DUT_ENROL_MAC(arg1, arg2, arg3):
	return "FAIL"
	
def WIN_DELAY(arg1, arg2, arg3):
	time.sleep(float(arg1))
	return "PASS"
def WIN_CONNECT(arg1, arg2, arg3):
	#Create an array with all the MAC
	#addresses of the detected devices
	nearby_devices = bluetooth.discover_devices()
	num = 0
	num_final = -1
	for i in nearby_devices:
		if ':' in 'arg1':
			if(arg1 == i):
				num_final = num
				break
		else:
			if(arg1 == bluetooth.lookup_name( i )):
				num_final = num
				break; # got the name
		num = num + 1
	global sock
	global bd_addr
	if(sock):
		#Close socket if connected previouslly 
		print "Disconnecting :" + str(bd_addr)
		sock.close()
        sock = None
	if(num_final >= 0):
		bd_addr = nearby_devices[num_final]
		print "Connecting " + str(bd_addr) + " " + bluetooth.lookup_name( i )
		port = 1
		sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
		sock.connect((bd_addr, port))
		print "Connected " + str(bd_addr) + " " + bluetooth.lookup_name( i )
		return "PASS"
	else:
		print "Device Not Found  " + arg1 
		return "FAIL"
	
def WIN_SEND_BLE(arg1, arg2, arg3): # send data to connected socat, pre requisit CONNECT should go Success
	global sock
	sock.send(b'\x11\x00\x00\x00\x00')
	return "PASS"
#---------------connect BLE docgal to PC-------------------

# try connecing to ble dongal

# Read CVS
print("\n\n``````````AFT (Automatic Function Tester)``````````` ")
print "This tool Simulates BLE dongal to send differant command to test device and AFT device"
print("\nInputs :")
#............User inupt Read...................
path_file = raw_input ("Drag and drop the test.csv file (comma seperated) : ")
outpath_file=path_file
outpath_file= outpath_file.replace(".csv", "_new.csv")
tmp_cmd = ""
fieldnames = ['SN', 'CMD','PERAM_01', 'PERAM_02','PERAM_03', 'RESULT']
'''
file_object = open(path_file,"r")
temp_file_data = file_object.read() 
file_object.close()
'''
lines = ""

with open(path_file, 'r') as csvFile:
	reader = csv.DictReader(csvFile)
	fieldnames = ('SN', 'CMD', 'PERAM_01','PERAM_02','PERAM_03','ITERATIONS','EXPECTED','OBSERVED','RESULT','TIME_STAMP','DURATION','REMARK')
	#lines = list(reader)
	#print reader
	myFile = open(outpath_file, 'wb')
	writer = csv.DictWriter(myFile, fieldnames=fieldnames)
	writer.writeheader()
	myFile.close()
	for row in reader:	  # go throug each row 
		#------------Read COmmand in each row and execute it by passing perameters---------------------------------
		iterations = -1
		iterations_base = 0
		out = "ERROR"
		observed_out = ""
		fail_count = 0
		time_now = time.time()
		if(row != None):
			tmp_cmd = row['CMD'].strip() #remove tab and white spaces
			tmp_per1 = row['PERAM_01'].strip()
			tmp_per2 = row['PERAM_02'].strip()
			tmp_per3 = row['PERAM_03'].strip()	# read nth row	command
			expected_out = row['EXPECTED'].strip()
			observed_out = ""
			print"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" # command spliter
			if(iterations is - 1):
				temp_str = (row['ITERATIONS'].strip())
				if (temp_str.isdigit()):
					iterations = int(temp_str,10)
					iterations_base = iterations
					if(iterations == 0):
						print "Skipping :" + tmp_cmd
					else:
						print "Executing :" + tmp_cmd + " for " + str(iterations) + " Iterations"
			while(iterations > 0) :
				try:
					observed_out = locals()[tmp_cmd](tmp_per1, tmp_per2, tmp_per3)
				except:
					print"Error : Executing command (" + tmp_cmd + ")"
				#print "OBS" + observed_out
				#print "EXP" + expected_out
				if(expected_out	 == observed_out): #and execute it
					out_temp = "PASS"
				else:
					out_temp = "FAIL"
					fail_count = fail_count + 1;
				iterations = iterations - 1
				if((out is "ERROR" ) or (out is "PASS" )):	# update out if its value is ERROR or PASS 
					out = out_temp
			#-----------Read and update the Result-----------------------------------------------------------
			if((fail_count != 0) and (iterations_base > 1)):
				row['RESULT'] = out + str(fail_count)
			else:
				if(iterations_base > 0):
					row['RESULT'] = out
				else:
					row['RESULT'] = "SKIPPED"
			time_after = time.time()
			row['OBSERVED'] = observed_out
			row['TIME_STAMP'] = datetime.datetime.fromtimestamp(time_now).strftime('%Y-%m-%d %H:%M:%S')
			row['DURATION'] = str(time_after - time_now)
			myFile = open(outpath_file, 'ab+')
			writer = csv.DictWriter(myFile, fieldnames=fieldnames)	  
			writer.writerow(row)
			myFile.close()
			#print row
		else:
			break
	  
csvFile.close()

#end

