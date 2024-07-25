#Read RFID code:5200127111 Rectangle
#Read RFID code:46003BB39B White Circle
#Read RFID code:010FB3CB43 Black Circle


import urllib.request  # import the urllib.request module for making HTTP requests
import RPi.GPIO as GPIO  # import the RPi.GPIO module for accessing GPIO pins on a Raspberry Pi
import time  # import the time module for timing-related functions
import LCD1602 as LCD  # import the LCD1602 module for interfacing with a 16x2 LCD display
import DHT11  # import the DHT11 module for reading temperature and humidity from a sensor
from keypadfunc import keypad as kp  # import the keypadfunc module for interacting with a keypad
import RFIDTest  # import the RFIDTest module for interacting with RFID tags
import PCF8591 as ADC  # import the PCF8591 module for interfacing with an ADC
import random  # import the random module for generating random numbers
from picamera import PiCamera  # import the PiCamera module for capturing images with the Raspberry Pi camera
from flask import Flask  # import the Flask module for building web applications
from flask import send_file  # import the send_file function from Flask for sending files as responses
from datetime import datetime  # import the datetime module for working with dates and times

API_KEY = "ThingSpeak API Key"  # set the write API key for uploading data to ThingSpeak

ADC.setup(0x48)  # initialize the ADC with address 0x48
Mycam = PiCamera()  # create a PiCamera object for capturing images
myapp = Flask(__name__)  # create a Flask app object with the name of the module

BLED = 12  # set the BCM pin number for the blue LED
RLED = 13  # set the BCM pin number for the red LED
GLED = 5  # set the BCM pin number for the green LED
PB = 18  # set the BCM pin number for the push button
TRIG = 6  # set the BCM pin number for the ultrasonic sensor trigger
ECHO = 4  # set the BCM pin number for the ultrasonic sensor echo
MotionSensor = 16  # set the BCM pin number for the PIR motion sensor
Flag = 0  # set the Flag variable to 0

dis = 1000  # set the initial distance for the ultrasonic sensor

CH_ID= "Use your ThingSpeak Channel ID"  # set the Channel ID for downloading data from ThingSpeak (public channel)
values=[]  # create an empty list for storing downloaded data

LCD.init(0x27, 1)  # initialize the LCD display with address 0x27 and 1 row
GPIO.setwarnings(False)  # disable GPIO warnings
GPIO.setmode(GPIO.BCM)  # set the GPIO numbering mode to BCM
GPIO.setup([BLED, RLED, GLED, 17,TRIG], GPIO.OUT)  # set the blue, red, and green LEDs, ultrasonic sensor trigger, and buzzer as output pins
GPIO.setup(ECHO, GPIO.IN)  # set the ultrasonic sensor echo as an input pin
GPIO.setup(PB, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)  # set the push button as an input pin with a pull-down resistor
GPIO.setup(MotionSensor, GPIO.IN, pull_up_down = GPIO.PUD_UP)  # set the motion sensor as an input pin with a pull-up resistor

Buzzer = GPIO.PWM(17,1)  # create a PWM object for the buzzer with a frequency of 1 Hz
Buzzer.start(50)


# Define function GetCaught that takes in arguments LEDcolor and delay
def GetCaught(LEDcolor, delay):
    
    video_path = "/home/pi/Desktop/video.h264" 
    # Start preview of the camera
    Mycam.start_preview()
    # Write "Nice Try" on the first line of the LCD screen
    LCD.write(0,0, "Nice Try")
    # Write "Get Caught" on the second line of the LCD screen
    LCD.write(0,1,"Get Caught")
    # Start recording a video to the specified path
    Mycam.start_recording(video_path)
    # Set the frequency of the buzzer to 200 Hz
    Buzzer.ChangeFrequency(200)
    # Loop through range delay times
    for i in range(delay):
        # Turn on LEDcolor
        GPIO.output(LEDcolor, GPIO.HIGH)
        # Pause for 1 second
        time.sleep(1)
        # Turn off LEDcolor
        GPIO.output(LEDcolor, GPIO.LOW)
        # Pause for 1 second
        time.sleep(1)
    # Clear the LCD screen
    LCD.clear()
    # Set the frequency of the buzzer to 1 Hz
    Buzzer.ChangeFrequency(1)
    # Stop recording the video
    Mycam.stop_recording()
    # Stop preview of the camera
    Mycam.stop_preview()
    # Return the path where the video was saved
    return video_path

def action(self):                     # Define a function named 'action' that takes 'self' as a parameter
    global Flag                       # Use the 'global' keyword to access the global variable 'Flag'
    if (Flag == 1):                   # Check if the value of 'Flag' is 1
        print("Movement Detected at {}".format(time.ctime()))   # Print a message indicating movement was detected
        Vid = GetCaught(RLED, 5)      # Call the 'GetCaught' function with parameters 'RLED' and '5' and assign the return value to 'Vid'

GPIO.add_event_detect(MotionSensor, GPIO.FALLING, callback=action, bouncetime=2000)    # Add an event detection for 'MotionSensor' that triggers when it detects a falling edge, and calls the 'action' function with a bounce time of 2000ms

def distance():                       # Define a function named 'distance'
    GPIO.output(TRIG, GPIO.LOW)       # Set the output of the GPIO pin 'TRIG' to LOW
    time.sleep(0.000002)              # Sleep for 2 microseconds
    GPIO.output(TRIG,1)               # Set the output of the GPIO pin 'TRIG' to HIGH
    time.sleep(0.00001)               # Sleep for 10 microseconds
    GPIO.output(TRIG,0)               # Set the output of the GPIO pin 'TRIG' to LOW
    while GPIO.input(ECHO)== 0:       # Wait until the input of the GPIO pin 'ECHO' is LOW
        a=0                           # Do nothing
    time1 = time.time()               # Record the current time
    while GPIO.input(ECHO) == 1:      # Wait until the input of the GPIO pin 'ECHO' is HIGH
        a=0                           # Do nothing
    time2 = time.time()               # Record the current time again
    duration = time2-time1            # Calculate the time duration between the two time points
    return duration*1000000/58        # Calculate the distance in centimeters and return it

# Function to read from the keypad                    
def keypadpass():                     # Define a function named 'keypadpass'
    keyn, keys = kp()                 # Call the 'kp' function to read the keypad input and assign the values to 'keyn' and 'keys'
    if(GPIO.input(PB) == 0):          # Check if the input of the GPIO pin 'PB' is LOW
        key = keyn                    # If it is, assign the value of 'keyn' to 'key'
    else:
        key = keys                    # Otherwise, assign the value of 'keys' to 'key'
    time.sleep(1)                     # Sleep for 1 second
    return key                         # Return the value of 'key'

#Function to create a passcode using the keypad
def createpass():
    # Asks the user to input a length for the keypad passcode
    keypadpasscodelength = input("Choose a length for your keypad passcode using the keyboard: ")
    # Cast the input to an integer
    keypadpasscodelength = int(keypadpasscodelength)
    # Initializes an empty list to store the keypad passcode
    keylist = []
    # Loops through the range of the keypad passcode length and appends each key pressed to the keylist
    for i in range(keypadpasscodelength):
        x = keypadpass()
        keylist.append(str(x))
    # Joins the list of keys with a space to form the complete passcode
    passcode = ' '.join(keylist)
    # Asks the user to confirm if the passcode is correct
    decide = input("Is this your passcode ? (" + passcode + ") Y/N: ")
    # If the passcode is correct, prints a message and returns the passcode
    if decide == "Y":
        print("Passcode created")
        return passcode
    # If the passcode is incorrect, asks the user if they want to try again or not
    else:
        repeat = input("Do you want to try again ? Y/N: ")
        # If the user wants to try again, calls the createpass() function recursively
        if repeat == "Y":
            return createpass()
        # If the user does not want to try again, prints a message and returns 0
        else:
            print("Passcode not created you may continue with the program")
            return 0
# Function to use camera without annotation
def NormalCamera(cammode, delay):
    Mycam.resolution = (640, 480)  # set the resolution of the camera
    if(cammode == "I"):  # check if the mode is image
        photo_path = "/home/pi/Desktop/cameraTest.jpg"  # set the path for saving the image
        Mycam.start_preview()  # start the camera preview
        time.sleep(delay)  # wait for the specified time
        Mycam.capture(photo_path)  # take the picture and save it to the specified path
        Mycam.stop_preview()  # stop the camera preview
        return photo_path  # return the path of the image
    elif(cammode == "V"):  # check if the mode is video
        video_path = "/home/pi/Desktop/video.h264"  # set the path for saving the video
        Mycam.start_preview()  # start the camera preview
        Mycam.start_recording(video_path)  # start recording video and save it to the specified path
        time.sleep(delay)  # wait for the specified time
        Mycam.stop_recording()  # stop recording the video
        Mycam.stop_preview()  # stop the camera preview
        return video_path  # return the path of the video


# Create Additional Tags for Animals and Humans so instead of having only 3 tags now we have 9 in total 6 for animals and 3 for humans
def AdditionalTags(HumanOrAnimal):
    RFID = RFIDTest.read()  # Read the RFID card
    while(RFID == '0'):  # Wait until a valid RFID card is detected
        RFID = RFIDTest.read()
        time.sleep(1)
    if(HumanOrAnimal == "Human"):  # Check if the tag is for a human
        tags1 = str(RFID) + str(0)  # Concatenate the RFID value with "0" to create a human tag
        return tags1
    elif(HumanOrAnimal == "Animal"):  # Check if the tag is for an animal
        tags2 = str(RFID) + str(random.randint(1, 2))  # Concatenate the RFID value with a random number between 1 and 2 to create an animal tag
        return tags2

# Function to identify the tags of the animals
def AnimalTags():
    Animal = AdditionalTags("Animal")  # Create an animal tag using the AdditionalTags function
    if(Animal =='52001271111'):  # Animal tag: 52001271111 corresponds to a Dog
        return 'Dog'
    elif(Animal == '52001271112'):  # Animal tag: 52001271112 corresponds to a Horse
        return 'Horse'
    elif(Animal == '46003BB39B1'):  # Animal tag: 46003BB39B1 corresponds to a Rabbit
        return 'Rabbit'
    elif(Animal == '46003BB39B2'):  # Animal tag: 46003BB39B2 corresponds to a Cow
        return 'Cow'
    elif(Animal == '010FB3CB431'):  # Animal tag: 010FB3CB431 corresponds to a Sheep
        return 'Sheep'
    elif(Animal == '010FB3CB432'):  # Animal tag: 010FB3CB432 corresponds to a Pig
        return 'Pig'

# Function to identify the tags of the humans
def HumanTags():
    # Call the AdditionalTags function with "Human" parameter to get human's tag
    Human = AdditionalTags("Human")
    
   # Check the tag to identify the human and return their name
    if(Human =='52001271110'): # If tag matches "52001271110"
        return 'Ibrahim' # Return name "Ibrahim"
    elif(Human == '46003BB39B0'): # If tag matches "46003BB39B0"
        return 'Mohammed' # Return name "Mohammed"
    elif(Human =='010FB3CB430'): # If tag matches "010FB3CB430"
        return 'Sultan' # Return name "Sultan"


# Function to provide the sound for the animals that you feed
def AnimalSound(frequencies, delays):
    # Loop through each frequency and delay, and play the corresponding sound
    for i in range(len(frequencies)):
        Buzzer.ChangeFrequency(frequencies[i])
        time.sleep(delays[i])
        time.sleep(0.1)
        
    # Stop the buzzer by setting the frequency to 1Hz
    Buzzer.ChangeFrequency(1)

# Function to read the soil moisture from channel 0 of the ADC
def ReadSoilMoisture():
    # Read the analog value from channel 0 of the ADC
    Soil_units = ADC.read(0)
    
    # Convert the analog value to percentage based on the 390mV/% conversion factor
    ADC0_SoilMoisture = (Soil_units*100/256)
    
    # Send the soil moisture data to ThingSpeak
    x = urllib.request.urlopen("https://api.thingspeak.com/update?api_key={}&field1={}".format(API_KEY , ADC0_SoilMoisture))
    
    # Return the soil moisture percentage
    return ADC0_SoilMoisture

# Function to read the light intensity from channel 1 of the ADC
def ReadLightIntensity():
    # Read the analog value from channel 1 of the ADC
    Light_units = ADC.read(1)
    
    # Write the analog value to the DAC to provide a real experience of the light intensity
    ADC.write(Light_units)
    
    # Convert the analog value to Lux based on the 13.2mV/Lux conversion factor
    ADC1_LightIntensity = (Light_units*250/256)
    
    # Send the light intensity data to ThingSpeak
    x = urllib.request.urlopen("https://api.thingspeak.com/update?api_key={}&field2={}".format(API_KEY ,ADC1_LightIntensity))
    
    # Return the light intensity in Lux
    return ADC1_LightIntensity

# Function to read the water flow from channel 2 of the ADC
def ReadWaterFlow():
    # Read from ADC using channel 2
    Water_units = ADC.read(2)
    
    # Convert water flow reading in ADC units to L/min
    ADC2_WaterFlow = (Water_units*20/256) #20L/min ==> 165uV/L/min
    
    # Update the water flow value on ThingSpeak
    x = urllib.request.urlopen("https://api.thingspeak.com/update?api_key={}&field3={}".format(API_KEY ,ADC2_WaterFlow))
    
    # Return the water flow reading in L/min
    return ADC2_WaterFlow

# Function to read the humidity and temperature from the DHT11 sensor
def ReadHumAndTemp():
    # Read the humidity and temperature from the DHT11 sensor
    HandT = DHT11.readDht11(27)
    time.sleep(1)
    
    # If the sensor reading is successful, update the values on ThingSpeak and return the values
    if HandT:
        hum, temp = HandT
        x = urllib.request.urlopen("https://api.thingspeak.com/update?api_key={}&field4={}&field5={}".format(API_KEY ,hum, temp))
        return (HandT)
    
    # If the sensor reading fails, try again
    else:
        return ReadHumAndTemp()

#Function to read sensors values
def Readings(lp, sensor, choice):
    valueReader = None # Set valueReader to None initially
    lp = int(lp) # Set the number of times to loop through the readings for type int
    for i in range (lp): # Loop lp number of times
        # Depending on the sensor specified, call the appropriate function to read its value
        if(sensor == "SM"):  # If the sensor is for soil moisture
            valueReader = ReadSoilMoisture() # Read soil moisture and assign value to valueReader
		# Print the moisture percentage
            print("The Moisture percentage is: " + str(valueReader) + " %") 
        elif(sensor == "LI"): # If the sensor is for light intensity
            valueReader = ReadLightIntensity() # Read light intensity and assign value to valueReader
		# Print the light intesnity value in LUX
            print("The light intensity is " + str(valueReader) + " LUX")
        elif(sensor == "WF"): # If the sensor is for water flow
            valueReader = ReadWaterFlow() # Read water flow and assign value to valueReader
            # Print the water flow value in L/min
            print("The water flow is " + str(valueReader) + " L/min")
        elif(sensor == "HT"): # If the sensor is for humidity and temperature
            valueReader = ReadHumAndTemp() # Read humidity and temperature from DHT11 sensor and assign value to valueReader
            if(choice == "H"): # If choice is for humidity
		    # Print the humidity percentage
                print("The Humidity is " + str(valueReader[0]) + " %")
            elif(choice == "T"): # If choice is for temperature
		    # Print the Temperature value in C
                print("The Temperature is " + str(valueReader[1]) + " C")
                
# Define the function "stripofbrackets" that takes 4 arguments:
# Numberofreadings: the number of readings to process
# msg: a string containing the message to be processed
# readings: a list containing the readings to process
# ts: a string containing a code for the type of reading (e.g. "s" for soil moisture, "l" for light intensity)
def stripofbrackets(Numberofreadings, msg, readings, ts):
    # Convert Numberofreadings to an integer
    Numberofreadings = int(Numberofreadings)
    
    # Loop over the range of Numberofreadings
    for i in range (Numberofreadings):
        # Check the value of ts
        # If ts is "s", add the i-th reading from the list with the string "% <br>" to the msg string
        if(ts == "s"):
            msg = msg + str(readings[i]) + " % <br>"
        # If ts is "l", add the i-th reading from the list with the string "LUX <br>" to the msg string
        elif(ts == "l"):
            msg = msg + str(readings[i]) + " LUX <br>"
        # If ts is "w", add the i-th reading from the list with the string "m/L <br>" to the msg string
        elif(ts == "w"):
            msg = msg + str(readings[i]) + " m/L <br>"
        # If ts is "h", add the i-th reading from the list with the string "% <br>" to the msg string
        elif(ts == "h"):
            msg = msg + str(readings[i]) + " % <br>"
        # If ts is "t", add the i-th reading from the list with the string "C <br>" to the msg string
        elif(ts == "t"):
            msg = msg + str(readings[i]) + " C <br>"
    
    # Return the updated msg string
    return msg


# Index
@myapp.route('/')
def index():
    # Initialize the welcome message
    msg = "Welcome our Smart Farm History Web<br><br>There is many options so choose one of them: <br>" 
    # Add options for viewing the last N readings of each sensor
    msg = msg + "<br>1. See the last (Number you choose) readings of the soil moisture sensor. Copy this and do not forget to adjust the (NumberOfReadings): http://0.0.0.0:5080/sm/NumberOfReadings<br>" 
    msg = msg + "<br>2. See the last (Number you choose) readings of the light intensity sensor. Copy this and do not forget to adjust the (NumberOfReadings): http://0.0.0.0:5080/li/NumberOfReadings<br>"
    msg = msg + "<br>3. See the last (Number you choose) readings of the water flow sensor. Copy this and do not forget to adjust the (NumberOfReadings): http://0.0.0.0:5080/wf/NumberOfReadings<br>"
    msg = msg + "<br>4. See the last (Number you choose) readings of the humidity sensor. Copy this and do not forget to adjust the (NumberOfReadings): http://0.0.0.0:5080/h/NumberOfReadings<br>"
    msg = msg + "<br>5. See the last (Number you choose) readings of the temperature sensor. Copy this and do not forget to adjust the (NumberOfReadings): http://0.0.0.0:5080/t/NumberOfReadings <br>"
    # Add options for viewing the last photo and video
    msg = msg + "<br>6. See the last photo taken by copying http://0.0.0.0:5080/lastphototaken <br>"
    msg = msg + "<br>7. See the last video taken by copying http://0.0.0.0:5080/lastvidtaken <br>"
    # Return the complete message
    return msg

#Dynamic route
# This function handles the "/sm/<Numberofreadings>" route, where <Numberofreadings> is a variable parameter passed in the URL
@myapp.route('/sm/<Numberofreadings>')
def download(Numberofreadings):
    # Calls the "downlaoddata()" function with sensor ID = 1 and the Numberofreadings parameter passed in the URL
    readings = downlaoddata(1, Numberofreadings)
    # Calls the "stripofbrackets()" function with the Numberofreadings parameter passed in the URL, a message string, the readings array, and 's' (sensor type for soil moisture)
    msg = stripofbrackets(Numberofreadings, "The last " + str(Numberofreadings) + " readings of the soil moisture sensor are: <br>", readings, 's')
    # Returns the message string
    return msg

#Dynamic route
# This function handles the "/li/<Numberofreadings>" route, where <Numberofreadings> is a variable parameter passed in the URL
@myapp.route('/li/<Numberofreadings>')
def download1(Numberofreadings):
    # Calls the "downlaoddata()" function with sensor ID = 2 and the Numberofreadings parameter passed in the URL
    readings = downlaoddata(2, Numberofreadings) 
    # Calls the "stripofbrackets()" function with the Numberofreadings parameter passed in the URL, a message string, the readings array, and 'l' (sensor type for light intensity)
    msg = stripofbrackets(Numberofreadings, "The last " + str(Numberofreadings) + " readings of the light intensity sensor are: <br>", readings, 'l')
    # Returns the message string
    return msg

#Dynamic route
# This function handles the "/wf/<Numberofreadings>" route, where <Numberofreadings> is a variable parameter passed in the URL
@myapp.route('/wf/<Numberofreadings>')
def download2(Numberofreadings):
    # Calls the "downlaoddata()" function with sensor ID = 3 and the Numberofreadings parameter passed in the URL
    readings = downlaoddata(3, Numberofreadings) 
    # Calls the "stripofbrackets()" function with the Numberofreadings parameter passed in the URL, a message string, the readings array, and 'w' (sensor type for water flow)
    msg = stripofbrackets(Numberofreadings, "The last " + Numberofreadings + " readings of the water flow sensor are: <br>", readings, 'w')
    # Returns the message string
    return msg

#Dynamic route
# This function handles the "/h/<Numberofreadings>" route, where <Numberofreadings> is a variable parameter passed in the URL
@myapp.route('/h/<Numberofreadings>')
def download3(Numberofreadings):
    # Calls the "downlaoddata()" function with sensor ID = 4 and the Numberofreadings parameter passed in the URL
    readings = downlaoddata(4, Numberofreadings)
    # Calls the "stripofbrackets()" function with the Numberofreadings parameter passed in the URL, a message string, the readings array, and 'h' (sensor type for humidity)
    msg = stripofbrackets(Numberofreadings, "The last " + Numberofreadings + " readings of the humidity sensor are: <br>", readings, 'h')
    # Returns the message string
    return msg

#Dynamic route
# This function handles the "/t/<Numberofreadings>" route, where <Numberofreadings> is a variable parameter passed in the URL
@myapp.route('/t/<Numberofreadings>')
def download4(Numberofreadings):
    # Calls the "downlaoddata()" function with sensor ID = 5 and the Numberofreadings parameter passed in the URL
    readings = downlaoddata(5, Numberofreadings)
    # Calls the "stripofbrackets()" function with the Numberofreadings parameter passed in the URL, a message string, the readings array, and 't' (sensor type for temperature)
    msg = stripofbrackets(Numberofreadings, "The last " + Numberofreadings + " readings of the temperature sensor are: <br>", readings, 't')
    # Returns the message string
    return msg


# Static route for downloading the last photo taken
@myapp.route('/lastphototaken')
def download5():
    # Send the file located at the specified path with the specified mimetype
    return send_file("/home/pi/Desktop/cameraTest.jpg", mimetype="cameraTest.jpg")

# Static route for downloading the last video taken
@myapp.route('/lastvidtaken')
def download6():
    # Send the file located at the specified path with the specified mimetype
    return send_file("/home/pi/Desktop/video.h264", mimetype="video.h264")

# Function for downloading data from ThingSpeak
def downlaoddata(fieldnum, Numberofreadings):
    # Cast the string Numberofreadings to an integer
    Numberofreadings = int(Numberofreadings)
    # Open a URL connection to the specified ThingSpeak channel and read the data
    y = urllib.request.urlopen("https://api.thingspeak.com/channels/{}/fields/{}.csv?results={}".format(CH_ID,fieldnum, Numberofreadings))
    # Decode the read values to ASCII
    data = y.read().decode('ascii')
    # Convert the imported data (ASCII) to a comma separated string
    data=",".join(data.split("\n"))
    # Extract the readings from the comma separated string
    values = []
    for i in range (5, Numberofreadings*3+3,3):
        values.append(data.split(",")[i])
    return values


while True:
    # Print the welcoming statement and ask the user to set their own password and to take a picture of themselves
    choice = 0
    print("Welcome to our smart farming system\nTo begin with we would like to provide you with maximum security so you have to start by taking a photo and setting your own keypad passcode")

    # Loop to allow the user to choose between taking a photo and setting a passcode
    while(choice != '3'):
        choice = input ("Please Choose: \n1. Photo \n2. Keypad \n3. Exit \n")

        # Take a photo and get the path of the saved image
        if(choice == '1'):
             path = NormalCamera("I", 5)#This should return the path of the photo taken by the camera also not to mention that the parameters are the mode of the camera and the delay of the photo

        # Create a passcode with the keypad
        elif(choice == '2'):
            passcode = createpass() #This should return a passcode created by the user with the keypad.

        # Exit the program
        elif(choice == '3'):
            print('Goodbye!!')

    # If both a passcode and photo have been set, allow access to the system
    if((passcode != None) and (path != None)):

        print("Now you may access the system normally or you could try to be sneaky if you want")
        choice = input("Please Choose: \n1. Normal Entry \n2. Sneaky!!!! \n")

        # If normal entry is selected, allow the user to choose between farmer and visitor mode
        if(choice == '1'):#Here do the normal entry logic
            choose = input("Choose if you are a farmer or visitor (f/v): ") # Ask the user to choose whether they are a farmer or a visitor

            # If farmer mode is selected, allow access with a valid ID
            if(choose == 'f'):
                print("Use your farm ID to enter: ")
                ID = HumanTags() # Read the ID using the RFID scanner

                # Allow access to the system for valid IDs
                if((ID == 'Sultan') or (ID == 'Mohammed') or (ID == 'Ibrahim')):
                    print ("Welcome " + str(ID))  # Display welcome message with name on the LCD
                    LCD.write(0,0, "Welcome")  # Display "Welcome on the first row on the LCD
                    LCD.write(0,1, str(ID))  # Display the name of the farmer on the second row on LCD
                    # Print account validation message with the current time
                    print("Your Account is valid, you have logged in at {}".format(time.ctime()))

                    # Prompt the user to choose whether they want to perform a task or view the history
                    y = input("Choose if you want to perform a task or view the history (t/h): ")
                    # If task is selected, display the available tasks to do and prompt the user to choose the task they want to do
                    if(y == 't'):
                        x = input("PLease choose from the list of available tasks to do: \n1. Read Soil Moisture \n2. Measure & Adjust the light intensity" 
                                + "\n3. Measure the Water Flow \n4. Read Room's Humidity \n5. Measure the temperature \n") 

                        # Prompt for the number of readings to take
                        lp = input("How many readings do you want to take? ")

                       # Call Readings() function based on the task selected
                        if (x == '1'):                    # If the user selects task 1
                            Readings(lp, "SM", None)      # Call Readings() function with parameters to read Soil Moisture
                        elif (x == '2'):                  # If the user selects task 2
                            Readings(lp, "LI", None)      # Call Readings() function with parameters to measure and adjust the light intensity
                        elif (x == '3'):                  # If the user selects task 3
                            Readings(lp, "WF", None)      # Call Readings() function with parameters to measure the water flow
                        elif (x == '4' or x == '5'):      # If the user selects task 4 or task 5
                            if(x == '4'):                # If the user selects task 4
                                Readings(lp, "HT", "H")  # Call Readings() function with parameters to read the room's humidity
                            elif(x == '5'):              # If the user selects task 5
                                Readings(lp, "HT", "T")  # Call Readings() function with parameters to measure the temperature


                    # If history is selected, display it using the Flask web application
                    elif(y == 'h'):
                        if __name__ == '__main__': # Check if the module is being run as the main program
                             # If yes, start the Flask web application on the specified host and port
                            myapp.run(host='0.0.0.0',port=5080)
                else:
                    # If no, print a message indicating that the account is invalid
                    print("Account is invalid")

            elif(choose == 'v'): # If visitor mode is selected

                # Display instructions for using the animal tag
                print("Use the given tag to find out the animal you are getting close to")
                animal = AnimalTags() # Get the animal tag from the sensor
                print("You are near " + str(animal))  # Display the name of the animal that is near the visitor

                # Determine if the animal is dangerous or safe
                if((animal == 'Dog') or (animal == 'Pig') or (animal == 'Horse')):
                    # If the animal is dangerous, keep checking the distance
                     while (dis > 50):
                         if (dis != 1000):
                             # If distance is valid, display safe distance and wait for 2 seconds
                             print("This distance " + str(dis) + " from the " + animal + " is considered safe")
                             time.sleep(2)
                         dis = distance() # Get new distance measurement
   

                    # If the distance is less than or equal to 50, the distance from the animal is considered dangerous
                    print("This distance " + str(dis) + " from the " + animal + " is dangerous")
                elif((animal == 'Rabbit') or (animal == 'Cow') or (animal == 'Sheep')):
                    # If the animal is safe, display feeding instructions and play animal sound
                    print("You may feed this " + str(animal) + " as it is really safe")
                    print("You may press the button to feed the " + str(animal))

                    # Wait for button to be pressed to play animal sound
                    while(GPIO.input(PB) == 0):
                        a = 0
                    # While the push button is pressed
                    while(GPIO.input(PB) == 1):
                        if(animal == "Cow"): # If animal is a cow, play cow sound
                            print(str(animal) + ": Mooooooooooooo") # Print cow sound
                            AnimalSound([261, 311, 330, 349, 392, 415, 466, 523], [0.5, 0.1, 0.1, 0.5, 0.5, 0.1, 0.1, 0.5]) # Play cow sound using the buzzer
                        elif(animal == "Rabbit"): # If animal is a rabbit, play rabbit sound
                            print(str(animal) + ": sususususususu") # Print rabbit sound
                            AnimalSound([329, 659, 587, 523], [0.2, 0.2, 0.2, 0.6]) # Play rabbit sound
                        elif(animal == "Sheep"): # If animal is a sheep, play sheep sound
                            print(str(animal) + ": Maaaaa' Maaaa'") # Print sheep sound
                            AnimalSound([330, 349, 392, 349], [0.3, 0.3, 0.3, 0.7]) # Play sheep sound
                                        
        elif(choice == '2'): #Here do the sneaky entry logic
            #Here in this part we will have a motion sensor that will detect movement and will trigger the alarm which is the buzzer and also the red led

            # Set the flag to 1 to trigger the interrupt and wait for 5 seconds
            Flag = 1
            time.sleep(5)

            # Set the flag to 0 to stop the interrupt and display a message
            Flag = 0
            print("You got caught better luck next time Bye Bye")
            
            # Exit the program
            exit
    else:
        # Display an error message if the user does not provide the correct input
        print("Error you are either missing a photo or keypad passcode \nTrying again...")
