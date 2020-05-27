
import sys, os, subprocess, platform, pty, time, threading, glob, serial, io, codecs, shlex, threading, glob, json, atexit
from colored import fg, bg, attr

from trunk import *

###First time running?:
# sudo apt-get install openjdk-14-jre
# then install requiered/en.stm32cubeprog_v2-4-0
# sudo ./SetupSTM32CubeProgrammer-2.4.0.linux
# sudo apt install python3-pip 
#sudo pip3 install serial, colored, 
#sudo adduser $USER dialout
#If you are getting an error with permissions try:
#sudo chmod 666 /dev/bus/usb/001/008


IO_test = 0
num_success = 0
min_success = 9
init_cmd = "/usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI"
board_select = "Control Zero"
default_port = "/dev/ttyACM1"

close_everything = 0

########################################################################

def t1():
	os.system('gnome-terminal -- python3 testserial.py')
	
########################################################################

def board():
	global board_select
	
	if board_select == "Control Zero":
		board_select = "Control Zero OEM"
		print("  Selected: Control Zero OEM")
		min_success = 8
	elif board_select ==  "Control Zero OEM":
		board_select = "Control Zero PixRacer"
		print("  Selected: Control Zero PixRacer")
		min_success = 8
	else:
		board_select == "Control Zero"
		print("  Selected: Control Zero")
		min_success = 9
		
		
	
########################################################################	

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    #print(sys.platform)
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        #ports = glob.glob('/dev/tty[A-Za-z]*')
        ports = glob.glob('/dev/ttyA*')
    elif sys.platform.startswith('darwin'):
        #ports = glob.glob('/dev/tty.*')
        ports = glob.glob('/dev/cu*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            #print("reading ports", port)
            #s1 = serial.Serial(port)
            #s1.close()
            result.append(port)
            time.sleep(1)
        except (OSError, serial.SerialException):
            pass
    return result

########################################################################
########################################################################
def flashTest():
	print(" ")
	print("------------------------------")
	print("Flashing Testing code:")
	print(" ")
	#cmd = "./st-flash --flash=1024k write ctrl0_textv1.bin 0x8000000"
	#cmd = "sudo /usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI -c port=SWD freq=8000 --skipErase -w ctrl0_textv1.bin 0x08000000"
	#cmd = "sudo /usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI -c port=SWD freq=8000 -w ctrl0_textv1.bin 0x08000000"
	#CTRL_Zero_777_mfg.hex
	cmd = " -c port=SWD freq=16000 -w CTRL_Zero_777_mfg.hex -v -hardRst"
	#p = subprocess.Popen((cmd), shell=True, bufsize=0, stdout=subprocess.PIPE)
	#p.wait()
	os.system(init_cmd+cmd)
	time.sleep(3)
	print(" ")

########################################################################
########################################################################
	
def erase():
	
	cmd = " -c port=SWD freq=16000 -e all"
	os.system(init_cmd + cmd)
	
########################################################################
def testBoard():
	global IO_test
	global num_success
	global min_success
	global default_port
	
	print("------------------------------")
	print("Starting...")
	print(" ")
	time.sleep(1)
	print("Waiting for port.... ")
	
	try:
		s = serial.Serial(tryPort,9600)
		time.sleep(1)
		s.close()
	except:
		pass
	
	try:
		tryPort = default_port
		#succss = 0
		
		
		print("Will try to connect: ", tryPort)

		while 1:
			try:
				s = serial.Serial(tryPort,9600)
				while(s.inWaiting() == 0):
					pass
				time.sleep(.5)
				while 1:
					if s.inWaiting() > 0:
						read_line = s.readline()
						print(read_line.decode("utf-8"))
						if read_line.decode("utf-8").find("->Ready") > 0:
							print("Found")
							#s.reset_input_buffer()
							#s.flush
							s.write(b'7')
							break
				break
			except: 
				time.sleep(.1)
				#s = serial.Serial(tryPort,9600)
				#print("\r\n Unexpected error:", sys.exc_info()[0])
				#print("\r.")
		
		while 1:
			read_line = s.readline()
			print("Afer:"+read_line.decode("utf-8"))
			if read_line.decode("utf-8").find("->F777: Init") > 0:
				print("Registered")
				break
		
		if 1 == 1:
			
			
			num_success = 0 #resetting num. 
			SD_Card_Success = 0 #SD testing success flag. 
			Baro_test_counter  = 0 #Counter of baro testing. 
			timer1= time.time()
			
			while (time.time() - timer1) < 15:
				if s.inWaiting() > 0:
					read_line = s.readline()
					print(read_line.decode("utf-8"))
					#----------------------------------#
					if read_line.decode("utf-8").find("->IO Test: OK!!!!") > 0:
						print("IO test OK!")
						IO_test = 1
						num_success = num_success + 1
					#if read_line.decode("utf-8").find("->IO Test:") > 0:
						##if read_line.decode("utf-8").find("OK!!!!") > 0:
							#print("IO test OK!")
							##IO_test = 1
						##else: 
							#IO_test = 0
							#print("IO test failed")		
							#print('%s IO test failed! %s' % (fg(1), attr(0)))			
					#----------------------------------#
					#->SD Card Write&Read Test:
					if read_line.decode("utf-8").find("->SD Card Write&Read Test:") > 0:
						if read_line.decode("utf-8").find("OK!!!") > 0:
							#print("SD Card Success!")
							SD_Card_Success = 1
							#pass
					elif read_line.decode("utf-8").find("Error: SD card cannot be initialized.") > 0:
						print("SD Card Error!")
						SD_Card_Success = 0
					#----------------------------------#
					if read_line.decode("utf-8").find("->BMI088: Starting Accel...") > 0:
						if read_line.decode("utf-8").find("Success!") > 0:
							#print("BMI088 Accel Success!")
							num_success = num_success + 1
							pass
						else:
							print("BMI088 Accel Failed!")
					#----------------------------------#
					if read_line.decode("utf-8").find("->BMI088: Starting Gyros...") > 0:
						if read_line.decode("utf-8").find("Success!") > 0:
							#print("BMI088 Gyros Success!")
							num_success = num_success + 1
						else:
							print("BMI088 Gyros Failed!")
					#----------------------------------#
					if read_line.decode("utf-8").find("->ICM20948:") > 0:
						if read_line.decode("utf-8").find("Success!") > 0:
							#print("ICM20948 Success!")
							num_success = num_success + 1
						else:
							print("ICM20948 Failed!")
					#----------------------------------#
					if read_line.decode("utf-8").find("->ICM20602:") > 0:
						if read_line.decode("utf-8").find("Success!") > 0:
							#print("ICM20602 Success!")
							num_success = num_success + 1
						else:
							print("ICM20602 Failed!")		
					#----------------------------------#
					if read_line.decode("utf-8").find("->DPS310:") > 0:
						if read_line.decode("utf-8").find("Success!") > 0:
							#print("->DPS310: Success!")
							num_success = num_success + 1
						else:
							print("->DPS310: Failed!")		
					#----------------------------------#
					if read_line.decode("utf-8").find("--->Writing 0x00's...") > 0:
						if read_line.decode("utf-8").find("Success!") > 0:
							#print("Writing 0x00's Success!")
							num_success = num_success + 1
						else:
							print("Writing 0x00's Failed!")									
					#----------------------------------#
					if read_line.decode("utf-8").find("--->Writing 0xFF's...") > 0:
						if read_line.decode("utf-8").find("Success!") > 0:
							#print("Writing 0xFF's Success!")
							num_success = num_success + 1
						else:
							print("Writing 0xFF's Failed!")	
					#----------------------------------#
					if read_line.decode("utf-8").find("Temp RAW") > 0:
						press=read_line.decode("utf-8").split()
						#print(press[2])
						if (int(press[2]) > 800) and (int(press[2]) < 1050):
							pass
							Baro_test_counter = Baro_test_counter + 1
							#print('%s Baro reading looks good! %s' % (fg('white'),bg('red'), attr('reset')))
						else: 
							print('%s Baro reading off limits %s' % (fg(1), attr(0)))
							
						if Baro_test_counter >= 4:
							num_success = num_success + 1
							s.flush()
							break
																															
			s.close()
			num_success = num_success + SD_Card_Success
			print("Test results:", num_success)
			print("Min needed:", min_success)
			if num_success >= min_success :
				print('%s Test Succesful! %s' % (fg(2), attr(0)))
			else:
				print('%s Test Failed! %s' % (fg(1), attr(0)))
		else: 
			print("no port found")
	except:
		print("Error")
########################################################################	
def flashBootloader():
	
		print("------------------------------")
		print("Flashing Bootloader... ")
		print(" ")
		f = open("current_firmware.txt", "r")
		current = f.read()
		print("Flasing Firmware: " + current)
		#cmd = "./st-flash --format ihex write arduplane_with_bl.hex"
		cmd = " -c port=SWD freq=16000 -w arduplane_with_bl.hex -v -rst"
		#p = subprocess.Popen((cmd), shell=True, stdout=subprocess.PIPE)
		#p.wait()
		os.system(init_cmd+cmd)
		print("------------------------------")
		
########################################################################	

def resetBoard():
	print(" ")
	print("Resetting board... ")
	#cmd = "./st-flash reset"
	cmd = " -c port=SWD freq=8000 -hardRst"
	p = subprocess.Popen((init_cmd+cmd), shell=True, stdout=subprocess.PIPE)
	p.wait()
	#time.sleep(2.5)
	#os.system(cmd)

########################################################################	

def autoDetect():
	print(" ")
	print(" Auto ")
	print(" ")
	cmd = " -l"
	#p = subprocess.Popen((cmd), shell=True, stdout=subprocess.PIPE)
	#p.wait()
	#time.sleep(2.5)
	os.system(init_cmd+cmd)
	#print("Done!")

########################################################################	

def connectToBoard():
	print(" ")
	print(" Auto ")
	print(" ")
	cmd = " -c port=SWD freq=8000"
	os.system(init_cmd+cmd)


########################################################################	
def runMavlink():
	try:
		cmd = "gnome-terminal -- python3 mavlink_test.py"
		os.system(cmd)
	except:
		print("Unable to launch")
########################################################################
def updateFirmware():
	try:
		cmd = "gnome-terminal -- python3 firmware_downloader.py"
		os.system(cmd)
	except:
		print("Unable to launch")
########################################################################
########################################################################	
def changePort():
	global default_port
	
	if default_port == "/dev/ttyACM1":
		default_port = "/dev/ttyACM0"
		print("-->Port set /dev/ttyACM0")
	else:
		default_port = "/dev/ttyACM1"
		print("-->Port set /dev/ttyACM1")
	time.sleep(1.5)
########################################################################
########################################################################	
def terminal():
	global default_port
	cmd = "python3 -m serial.tools.miniterm " 
	os.system(cmd+default_port)
########################################################################

def printMenu():
		print("------------------------------")
		print("1: Flash Test firmware")
		print("2: Run Test")
		print("3: Flash Bootloader")
		print("4: Flash & Test")
		print("5: Test & Flash Bootloader")
		print("6: Flash & Test & Bootloader")
		print("7: Reset Board")
		print("9: Erase Board")
		print("0: Exit")
		print("b: Change board")
		print("c: Connect/Test ST Programmer")
		print("h: Help")
		print("m: MavLink Monitor")
		print("p: Change USB Port ACM1 <-> ACM0")
		print("t: Terminal")

########################################################################
########################################################################
def mainLoop():
	atexit.register(exit_handler)
	while(1):
		
		print(" ")
		answer = input('%s Select Option (Press h for Help): %s' % (fg(3), attr(0))) #print('%s Test Succesful! %s' % (fg(2), attr(0)))
		
		if answer == "1":
			flashTest()
			time.sleep(2)
			printMenu()

		elif answer == "2":
			testBoard()
			time.sleep(2)
			printMenu()

		elif answer == "3":
			flashBootloader()
			resetBoard()
			time.sleep(2)
			printMenu()		
			
		elif answer == "4":
			flashTest()
			resetBoard()
			time.sleep(6)
			testBoard()
			time.sleep(4)
			printMenu()			
		elif answer == "5":
			testBoard()
			if IO_test == 1:
				flashBootloader()
			else:
				print("Error IO test failed")
			time.sleep(2)
			printMenu()
				
		elif answer == "6":
			flashTest()
			time.sleep(5)
			testBoard()
			if num_success >= min_success:
				flashBootloader()
				#resetBoard()
				print('%s Testing & Bootloading Successful! %s' % (fg(2), attr(0)))
				#connectToBoard()
				stringy = ''
				while stringy != default_port:
					try:
						stringy = glob.glob(default_port)[0]
					except:
						print("Trying again")
						time.sleep(1)
						
				stringy = ''		
				while stringy == default_port:
					try:
						stringy = glob.glob(default_port)[0]
					except:
						pass
						#print("trying again2")
						#time.sleep(1)
						
				print("Port found! Waiting for reconnection...")
				time.sleep(10)
				runMavlink()
			else:
				print('%s Error! %s' % (fg(1), attr(0)))
			time.sleep(2)
			printMenu()
		elif answer == "7":
			resetBoard()
		elif answer == "9":
			erase()
			time.sleep(2)
			printMenu()					
		elif answer == "0":
			break
		elif answer == "a":
			autoDetect()
		elif answer == "b":
			board()
		elif answer == "c":
			connectToBoard()
		elif answer == "h":
			printMenu()
		elif answer == "m":
			runMavlink()
		elif answer == "p":
			changePort()
		elif answer == "t":
			terminal()
			time.sleep(3)
			printMenu()
		elif answer == 'u':
			updateFirmware()
		else:
			print("nel, Try again:")
			printMenu()	

########################################################################
def exit_handler():
	print('My application is ending!')
	set_Setting('mainLoopStatus', 'closed', 'status.json', 1)
  
########################################################################
print("mRo Control Zero Testing Software 1.3")
cmd = "sudo /usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI -c port=SWD freq=8000"
#os.system(cmd)

printMenu()
print("------------------------------")

set_Setting('mainLoopStatus', 'open', 'status.json', 0)

thrd0 = threading.Thread(target=mainLoop)
thrd0.start()


thrd1 = threading.Thread(target=t1)
#thrd1.daemon = True
thrd1.start()

thrd0.join()

print("   Bye!!!")

