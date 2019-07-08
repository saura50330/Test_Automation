#run below command
#C:\Python27\python.exe C:\Users\ndhavalikar\Desktop\Allegion_Nand\Personal\GIT\BL_Pic16f-master\test_automation\Test_Automation-master\AFT.py
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
RCV_DATA_SIZE = 5
outpath_file=""
temp_file_data =""
sock = None
bd_addr = None
#DUT_MAC = [20,255,254,200]
def intList_toHexList(list):
	b=[]
	for item in list:
		b.append(hex(item))
	return b
def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False
"""
HexByteConversion

Convert a byte string to it's hex representation for output or visa versa.

ByteToHex converts byte string "\xFF\xFE\x00\x01" to the string "FF FE 00 01"
HexToByte converts string "FF FE 00 01" to the byte string "\xFF\xFE\x00\x01"
"""

#-------------------------------------------------------------------------------

def ByteToHex( byteStr ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """
    
    # Uses list comprehension which is a fractionally faster implementation than
    # the alternative, more readable, implementation below
    #   
    #    hex = []
    #    for aChar in byteStr:
    #        hex.append( "%02X " % ord( aChar ) )
    #
    #    return ''.join( hex ).strip()        

    return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()

#-------------------------------------------------------------------------------

def HexToByte( hexStr ): # convert string to raw binary bytes
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    # The list comprehension implementation is fractionally slower in this case    
    #
    #    hexStr = ''.join( hexStr.split(" ") )
    #    return ''.join( ["%c" % chr( int ( hexStr[i:i+2],16 ) ) \
    #                                   for i in range(0, len( hexStr ), 2) ] )
 
    bytes = []

    hexStr = ''.join( hexStr.split(" ") )

    for i in range(0, len(hexStr), 2):
        bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

    return ''.join( bytes )
	
def DUT_FFR(arg1, arg2, arg3):
	'''
	#-----------------------------FDR sequence turn off battery, hold switch turn on power release switch
	print"FDR sequence started"
	AFT_RELAY(b'\xF1\x00',"","") # turn off Power
	time.sleep(1)
	AFT_DIO(b'\xF2\x01',"","")	 # press switch
	time.sleep(0.5)
	AFT_RELAY(b'\xF1\x01',"","") # turn ON Power
	time.sleep(2)
	AFT_DIO(b'\xF2\x00',"","")	 # Realease switch
	#validate FDR
	#read fdr eep region and check
	err_flag = 0
	i = 0xF0
	while(i<0xF7):
		i = i+1
		temp_data_1 = (b'\x04\x7F') + bytes(chr(i), 'ascii') + (b'\x00\x00')
		temp_data = WIN_SEND_RCV_BLE(temp_data_1, "", "")
		expected_data = (b'\x04\x7F') + bytes(chr(i), 'ascii') + (b'\x00\xFF')
		if( expected_data != temp_data ): # check if all data set to 0xFF
			err_flag = 1
			break;
	if(err_flag):
		print"FDR Fail"
		return "FAIL"
	print"FDR Pass"
	'''
	temp = raw_input("manually FDR the device and press enter: ")
	return "PASS"
def WIN_FLASH(arg1, arg2, arg3):
	temp_data = b'\x00'
	status = "PASS"
	try:
		with open(arg1, 'r') as text_file:
		# One option is to call readline() explicitly
		# single_line = text_file.readline()

		# It is easier to use a for loop to iterate each line
			for line in text_file:
				line = line.rstrip("\n\r")
				tx_dat = list(line.split(" "))
				tx_dat = list(map(int, tx_dat))
				temp_chk = tx_dat[0]
				tx_dat = ''.join(format(x, '02x') for x in tx_dat)
				temp_data = WIN_SEND_RCV_BLE(tx_dat, arg2, arg3)
				if(((temp_chk != 0xFF) and (temp_chk != 0x07) and (temp_chk != 0x06)) and ((len(temp_data) != 5 ) or temp_data[1] == 0xFF)): #error while flashing , exlude check if its dummy commmand 0xff
					status = "FAIL"
					break;
	except:
		status = "FAIL"
	return status
def DUT_ENROL_MAC(arg1, arg2, arg3):
	i = 0xF4
	while( i < 0Xf8) :
		temp_data = (b'\x02\x7F') + bytes(chr(i), 'ascii') + (b'\x00') + bytes(chr(arg1[i]), 'ascii') # WRITE 4 BYTES OF mac
		WIN_SEND_RCV_BLE(temp_data, "", "")
		i += 1
		print "MAC written"
	return "PASS"
	
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
		print "Device Not Found	 " + arg1 
		return "FAIL"
	
def WIN_SEND_BLE(arg1, arg2, arg3): # send data to connected socat, pre requisit CONNECT should go Success
	global sock
	arg1 = arg1.replace("0x",'')
	arg2 = arg2.replace(" ",'') # remove spaces
	hex_data =  HexToByte(arg1)
	sock.send(hex_data)
	e = float(arg2) #inter frame delay
	time.sleep(e)  # responce time is around 100 ms
	print ( "Sending: " + ByteToHex(hex_data))
	#print e
	return "PASS"

def WIN_SEND_RCV_BLE(arg1, arg2, arg3): # send data to connected socat, pre requisit CONNECT should go Success and wait for the responce for arg2 s
	global sock
	data = "" 
	arg3 = arg3.replace(" ",'') # remove spaces
	e = float(arg3) #inter frame delay
	sock.settimeout(e)
	#flush the data
	try:
		data = sock.recv(RCV_DATA_SIZE)
	except:
		data = "" #dummy
	WIN_SEND_BLE(arg1, arg2, arg3)
	#print e
	data = b'\xFF\xFF\xFF\xFF\xFF'
	try:
		data = sock.recv(RCV_DATA_SIZE)
		print "Received: " + ByteToHex(data) 
	except:
		print "Received: Nothing or bytes less then " + str(RCV_DATA_SIZE)
		data = b'\xFF\xFF\xFF\xFF'
	sock.settimeout(0)
	return(data)
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
			if(iterations is - 1):
				temp_str = (row['ITERATIONS'].strip())
				if (temp_str.isdigit()):
					iterations = int(temp_str,10)
					iterations_base = iterations
					if(iterations == 0):
						#print ""###"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" # command spliter
						#print ""###"Skipping :" + tmp_cmd
						pass #this is to avoid syntex error of empty if statement
					else:
						print"\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" # command spliter
						print "Executing :" + tmp_cmd + " for " + str(iterations) + " Iterations"
			while(iterations > 0) :
				###try:
				observed_out = locals()[tmp_cmd](tmp_per1, tmp_per2, tmp_per3)
				###except:
				###	print"Error : Executing command (" + tmp_cmd + ")"
				#print "OBS" + observed_out
				#print "EXP" + expected_out
				expected_out = expected_out.replace("0x","")
				if(is_hex(expected_out)): #if its hex 
					# convert to raw and compare
					if(observed_out == HexToByte(expected_out)):
						out_temp = "PASS"
					else:
						out_temp = "FAIL"
				elif(expected_out == observed_out): #its other string
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
			if(is_hex(expected_out)):
				row['OBSERVED'] = ByteToHex(observed_out)
			else:
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

