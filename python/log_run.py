#import required libraries
import obd
import sqlite3
import library
from datetime import datetime

#make local references to relevant display properties, tools, and buttons,
#	commands as defined in library.py
disp = library.disp
width = disp.width
height = disp.height
image = library.image
draw = library.draw
font = library.font
button_B = library.button_B
cmd_book = library.cmd_book

#clear the display
disp.fill(0)

#connect to the ECU
car_connection = obd.OBD()

#connect to the SQLite database
connection = sqlite3.connect('/home/pi/ice.db')
link = connection.cursor()

#create session timestamp
session = datetime.now().strftime('%H:%M:%S.%f')
timestamp = session

#initialize helper variable to keep track of program position
active = 1

#give confirmation to the user that logging will proceed
draw.text((5, 10), "Logging...", font=font, fill=255)
disp.image(image)
disp.show()

#while loop runs on initialization until user presses B
while(active):
	
	#create a new timestamp at each round of readings
	timestamp = datetime.now().strftime('%H:%M:%S.%f')
	
	#enumerate returns each command and its index
	#the command's position in the book doubles as an identifying code in the database
	for n, cmd in enumerate(cmd_book):
		
		#query the ECU for each command
		response = float(round(car_connection.query(cmd).value.magnitude, 3))
		
		#create a package of parameters to supply to the SQLite connection
		package = [session, timestamp, n, library.transform(response, n)]
		
		#push a new record to the SQLite database with the new unique parameters 
		link.execute('INSERT INTO car_data VALUES (?, ?, ?, ?);', package)
		
	#exit the program when user presses B
	if(not button_B.value):
		active = 0

#commit new changes to the SQLite database and close the connection
connection.commit()
connection.close()

#for program speed, the confirmation message is only rendered at initialization and cleared at exit
disp.fill(0)
disp.image(image)
disp.show()







#link.execute('DROP TABLE car_data;')

#link.execute('CREATE TABLE car_session (startMs text PRIMARY KEY);')

#link.execute('INSERT INTO car_session VALUES (?);', [session])

#link.execute('CREATE TABLE car_data (car_session text, timeMs text, query_code int, query_value real, FOREIGN KEY(car_session) REFERENCES car_session(startMs));')

#link.execute('INSERT INTO car_data VALUES (123456789, 987654322, 64, 100.8);')

#response = connection.query(intake_pressure).value.magnitude

#response = [session, datetime.now().strftime('%H:%M:%S.%f'), float(car_connection.query(intake_pressure).value.magnitude)]
#link.execute('INSERT INTO car_data VALUES (?, ?, 3, ?);', response)

#response = [session, datetime.now().strftime('%H:%M:%S.%f'), float(car_connection.query(rpm).value.magnitude)]
#link.execute('INSERT INTO car_data VALUES (?, ?, 4, ?);', response)

#link.execute('SELECT * FROM car_data WHERE car_session = ?;', [session])

#os.system("sudo node /home/pi/index.js")

#for c in link.fetchall():
	#print(c)
