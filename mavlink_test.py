#!/usr/bin/env python3
import time
from pymavlink import mavutil
from trunk import *
#from colored import fg, bg, attr
from colored import fg, bg, attr

#if get_Setting('mainLoopStatus', 'status.json', 0) == "closed":
#	print("Warning: Manual override enabled")
#	set_Setting('mainLoopStatus', 'manual', 'status.json', 1)


print("Hello, Launching MavLink viewer...")
timer1 = time.time()

# Start a connection listening to a UDP port
#the_connection = mavutil.mavlink_connection('udpin:localhost:14540')

time.sleep(1)
print("--->Looking for ports, please wait... Can take up to a minute...")
print("")

port1 = '/dev/ttyACM1'
port2 = '/dev/ttyACM2'
current = port1

while 1:
	try:
		the_connection = mavutil.mavlink_connection(current)
		time.sleep(1)
		the_connection.wait_heartbeat()
		break
	except:
		pass
		if current == port1:
			current = port2
		elif current == port2:
			current = port1
		time.sleep(1)

print("Connected to port: " + current)
print("Heartbeat from System %u, Component %u" % (the_connection.target_system, the_connection.target_system))
time.sleep(4)
#https://mavlink.io/en/messages/common.html#MAV_DATA_STREAM_EXTENDED_STATUS
for i in range(0, 3):
	the_connection.mav.request_data_stream_send(the_connection.target_system, the_connection.target_component, mavutil.mavlink.MAV_DATA_STREAM_ALL, 4, 1)
	
pevent = mavutil.periodic_event(5)
                                        
while(1):
	the_connection.recv_msg()
	if pevent.trigger():
		try:		
			IMU = the_connection.messages['RAW_IMU']
			IMU2= the_connection.messages['SCALED_IMU2']
			try:
				IMU3= the_connection.messages['SCALED_IMU3']
			except:
				pass
			PR1= the_connection.messages['SCALED_PRESSURE']
			GPS_RAW= the_connection.messages['GPS_RAW_INT']
			#print(IMU)
			print("\tAx\tAy\tAz\t|Gx\tGy\tGz\t|Mx\tMy\tMz")
			print(f"0|\t{IMU.xacc:.0f}\t{IMU.yacc:.0f}\t{IMU.zacc:.0f}\t|{IMU.xgyro:.0f}\t{IMU.ygyro:.0f}\t{IMU.zgyro:.0f}\t|{IMU.xmag:.0f}\t{IMU.ymag:.0f}\t{IMU.zmag:.0f}")
			print(f"1|\t{IMU2.xacc:.0f}\t{IMU2.yacc:.0f}\t{IMU2.zacc:.0f}\t|{IMU2.xgyro:.0f}\t{IMU2.ygyro:.0f}\t{IMU2.zgyro:.0f}\t|{IMU2.xmag:.0f}\t{IMU2.ymag:.0f}\t{IMU2.zmag:.0f}")
			print(f"2|\t{IMU3.xacc:.0f}\t{IMU3.yacc:.0f}\t{IMU3.zacc:.0f}\t|{IMU3.xgyro:.0f}\t{IMU3.ygyro:.0f}\t{IMU3.zgyro:.0f}\t|{IMU3.xmag:.0f}\t{IMU3.ymag:.0f}\t{IMU3.zmag:.0f}")
			print(f"Pressure1 Abs: {PR1.press_abs:.2f} \tDif: {PR1.press_diff:.1f} \tTemp: {PR1.temperature:.0f}" + "\tSats in View: " + str(GPS_RAW.satellites_visible))
			#print("Sats in View: " + str(GPS_RAW.satellites_visible))
			
		except:
			print("Error")
						
		try:
			PR2= the_connection.messages['SCALED_PRESSURE2']
			print(f"Pressure2 Abs: {PR2.press_abs:.2f} \tDif: {PR2.press_diff:.1f} \tTemp: {PR2.temperature:.0f}")
			#print(" ")
		except:
			print(f"Pressure2 Abs: INOP \tDif: INOP \tTemp: INOP")
			
			
		#print("...Press ctrl+c to exit...")
		print('%s ...Press ctrl+c to exit... %s' % (fg(3), attr(0)))
		print(" ")
			
	time.sleep(.005)

	#ALL = the_connection.recv_match(blocking=True)
	#print(ALL)

                                                
