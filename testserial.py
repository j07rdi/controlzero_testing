import glob, time

from trunk import *

result = ''
last_result = ''

result2 = ''
last_result2 = ''

start = time.time()
end = 0

start2 = time.time()
end2 = 0

if get_Setting('mainLoopStatus', 'status.json', 0) == "closed":
	print("Warning: Manual override enabled")
	set_Setting('mainLoopStatus', 'manual', 'status.json', 1)

while 1 :
	result = glob.glob('/dev/ttyA*')
	#print(len(result))
	#print(result.find("/dev/ttyACM1"))
	found_ACM1 = 0
	found_ACM2 = 0
	
	for x in result:
		if x.find("/dev/ttyACM1") >= 0:
			found_ACM1 = 1
		elif x.find("/dev/ttyACM2") >= 0:
			found_ACM2 = 1
	
	if found_ACM1 == 1 :
		#print("/dev/ttyACM1")
		result = "/dev/ttyACM1 Connected"
	else:
		#print("Disconnected")
		result = "/dev/ttyACM1 Disconnected"
		
	
	if found_ACM2 == 1 :
		#print("/dev/ttyACM1")
		result2 = "/dev/ttyACM2 Connected"
	else:
		#print("Disconnected")
		result2 = "/dev/ttyACM2 Disconnected"
		
	if last_result != result :
		end = time.time() 
		print("[" + str(round(end - start,2)) + "] " + result)
		last_result = result
		start = time.time()
		
	if last_result2 != result2 :
		end = time.time() 
		print("[" + str(round(end - start,0)) + "] " + result2)
		last_result2 = result2
		start = time.time()
		
	time.sleep(.1)
	
	if get_Setting('mainLoopStatus', 'status.json', 0) == "closed":
		break
