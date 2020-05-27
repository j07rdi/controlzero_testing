import wget, os, time
print('')
print('Welcome to the mRo firmware updater for Control Zero')
print('')
print('Getting the lastest stable version from Ardupilot.com:')
time.sleep(1)
try:
	os.remove("firmware-version.txt")
except:
	pass
finally:
	url = 'https://firmware.ardupilot.org/Plane/stable/mRoControlZeroF7/firmware-version.txt'
	wget.download(url, os.getcwd()+'/firmware-version.txt')

print('')
print('')

current = ''
#Finding out current version installed in the system.
try:
	f = open("current_firmware.txt", "r")
	current = f.read()
	print("Current Firmware: " + current)
except:
	print("Current version data not available, creating a file")
	f = open("current_firmware.txt", "w")
	f.write("Unknown")
	f.close()

#Finding out latest version available online.
fd = open("firmware-version.txt", "r")
latest = str(fd.read())
print('Lastest Firmware: ' + latest)

if current != latest:
	print("--->Seems like there is a newer version available.")
else:
	print("--->You already have the latest version.")

print('')
answer = input('Do you want to download and update? y or n: ')
if answer == 'yes' or answer == 'y':
	try:
		os.remove("arduplane_with_bl.hex")
	except:
		pass

	try:
		url = 'https://firmware.ardupilot.org/Plane/stable/mRoControlZeroF7/arduplane_with_bl.hex'
		wget.download(url, os.getcwd()+'/arduplane_with_bl.hex')
		
		#After downloading latest firmware, we save the version to known it later. 
		f = open("current_firmware.txt", "w")
		f.write(latest)
		f.close()
		
	except:
		print("Unable to update, try again later")

	print('')
	print('')
	
	try:
		f = open("current_firmware.txt", "r")
		print("Your new Firmware version is: " + f.read()) 
	except:
		print("Unable to verify your latest version... error")
else:
	print("Not updating... bye!!")
