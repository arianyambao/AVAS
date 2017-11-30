import serial
import requests,json
import RPi.GPIO as GPIO      
import os
import re
import time
import subprocess
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
geolocator=Nominatim()
timee=time.strftime("%H:%M:%S")
from pymongo import MongoClient
month=time.strftime("%B")
date=time.strftime("%d")
year=time.strftime("%Y")
day=time.strftime("%A")
success="no"
myfile=open('/home/pi/Desktop/data', 'r')
data=myfile.readlines()
for line in data:
    words=line.split()
    print (words)
    fname=line.split()[0]
    mname=line.split()[1]
    lname=line.split()[2]
    plate_number=line.split()[3]
    vehicle_type=line.split()[4]
myfile.close()
location=" "
location_splitter=" "
my_number="+639158861700"

from time import sleep
GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(12, GPIO.IN)
GPIO.setup(26, GPIO.IN)
# Enable Serial Communication
port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=1) #port = san naka connect yung Serial TTL CABLE converted to Serial Port (GSM/GPS CABLE)
 

port.write('AT'+'\r\n')
rcv = port.read(10)
print rcv
sleep(1)

port.write('AT+CGPS=1'+'\r\n')
rcv = port.read(100)
print rcv
sleep(1)

counter=1
while True:
    sensor=GPIO.input(14)
    sensor2=GPIO.input(15)
    sensor3=GPIO.input(12)
    sensor4=GPIO.input(26)


    def call():
        checker="+CGPSINFO:,,,,,,,,"
        
   # Transmitting AT Commands to the Modem
            # '\r\n' indicates the Enter key
# GPS
        

        while(checker=="+CGPSINFO:,,,,,,,,"):
            port.write('AT+CGPSINFO'+'\r\n')
            rcv = port.read(100)
            print rcv
            global counter
            
            checker=re.findall(r"(\+CGPSINFO:,,,,,,,,)",rcv)
            try:
                checker=checker[0]
                sleep(2)
                
                
            except:
                checker='null'
        if(checker=="null"):
            print("\n\n\nHELLOOOO")
        
            new=re.findall(r"(\d+.{0,1}\d*)",rcv)
            Lat=new[0]
            Lon=new[1]

            Lat=float(Lat)
            Lon=float(Lon)
#getting the gps
            def dm(Lat):
                degrees=int(Lat) // 100
                minutes=Lat - 100*degrees
                return degrees, minutes
            def decimal_degrees(degrees, minutes):
                return degrees + minutes/60
            Lat=(decimal_degrees(*dm(Lat)))
            print ("Latitude: "+str(Lat))


            def dm(Lon):
                degrees=int(Lon) // 100
                minutes=Lon - 100*degrees
                return degrees, minutes
            def decimal_degrees(degrees,minutes):
                return degrees+minutes/60
            Lon=(decimal_degrees(*dm(Lon)))
            print ("Longitude: "+str(Lon))

            port.write('AT+CGPS=0'+'\r\n')
            rcv = port.read(100)
            print rcv
            sleep(1)
            
        
            
            
                        
        tlat=str(Lat)
        tlon=str(Lon)
        print(tlat)
        print(tlon)
        def connect():
            print("Establishing Connection")
            subprocess.call(['sudo' , 'pon', 'rnet'])
           
            counter=0
            while(counter!=10):
                sleep(1)
                counter+=1
            #For getting the zip code
            print("Getting Location Name")
            location = geolocator.reverse(tlat+", "+tlon)    
            location_splitter=(location.address)
            location1=(location.address)
	    print(location_splitter)
            location_splitter=location_splitter.split(",")
            print location_splitter
           
            if(len(location_splitter)>7):
                for i in location_splitter:
                    i=i.strip(" ")
                    print i
                    if (i=="Angeles"):
                        zipp="2009"
                        connect.zipp=zipp
                        break
                    else:
                        news=re.findall(r"^([0-9]{4})$",i)
                        if(len(news)>0):
                            zipp=news[0]
                            connect.zipp=zipp
                        
                print(zipp)
                street=(location_splitter)[1]
                connect.brgy=(location_splitter)[0]
                print street
		
            else:
                for i in location_splitter:
                    i=i.strip(" ")
                    print i
                    if (i=="Angeles"):
                        zipp="2009"
                        connect.zipp=zipp
                        break
                    else:
                        news=re.findall(r"^([0-9]{4})$",i)
                        if(len(news)>0):
                            zipp=news[0]
                            connect.zipp=zipp  
                      
                print(zipp)
                street=(location_splitter)[1]
                connect.brgy=(location_splitter)[0]
                print street
                    
               
            #else: Guide For Background Location 
                #zipp=(location_splitter)[5]
                #zipp=zipp.strip(" ")
                #print(zipp)
                #street=(location_splitter)[2]
                #connect.brgy=(location_splitter)[0]
            
                
                #print(street)
           
            
                

            
            
            tempcounter=0
            print("Establishing Database")
            Client = MongoClient('Secret')#Connect to database
            db = Client['ahartest']#database name
            collection = db["logs"]#collection 
            users = db["users"]
            
            print("Database Zipcode")

            hanap = users.find_one({"zipcode":zipp})
            connect.primary=("0"+str(hanap['contact']))
            print("OK")
            print(hanap['city'])
            print ("Getting The Arrays")    
            connect.street=street.strip(" ")
            connect.counter=0
            sleep(2)
            connect.phone=[]
            admin=[]
            tempzipp=[]
            currentlocation=(Lat, Lon)
            ccty=[]

            test= users.find({"province":hanap['province']})
            print (hanap['province']+" Province")
            for city in test: #for getting the distance
                print city['city']
                ccty=(city['city'] +" "+city['province'])
                print ccty
                print (city['zipcode'])
                location=geolocator.geocode(city['city'] +" "+city['province'])
                locationlat = geolocator.geocode(city['city'] +" "+city['province']).latitude
                locationlon = geolocator.geocode(city['city'] +" "+city['province']).longitude
                locationfinal = (locationlat, locationlon)
                print (vincenty(currentlocation, locationfinal).kilometers)
                if((vincenty(currentlocation, locationfinal).kilometers)<20):
                    
                    tempzipp.append(city['zipcode'])
                    connect.counter+=1
                    
                    sleep(1)
            print("SCHEMA DESU")
            while(tempcounter<connect.counter):
                hanap = users.find_one({"zipcode":tempzipp[tempcounter]})
                print (hanap)
            
                connect.phone.append(str( ("0"+str(hanap['contact']))))
                admin.append(str(hanap['username']))
                tempcounter+=1
                sleep(1)
            
            
            
            print("SCHEMA DESU2")
            schema = {
              "name": {"fname":fname,"mdname":mname,"lname":lname},
              "platenumber": plate_number,
              "vehicletype":vehicle_type,
              "location" : 
                 { "street": location1, "city": zipp, "cc": 'Philippines' },
              
                "date":{
                        "month":month,
                        "dayN":date,
                        "year":year,
                        "dayS":day
                        },
                "time":timee,
             "to":[i for i in admin],
             "from":my_number,
             "coordinates":[tlat,tlon],
             "seen":"false"
                      
            }

            collection.insert(schema)#inserts schema a.k.a doc
            
            
            

            counter=0
            while(counter!=5):
                sleep(1)
                counter+=1
            connect.success="yes"
            print ("Closing Connection")
            subprocess.call(['sudo' , 'poff', 'rnet'])
    
            while(counter!=12):
                sleep(1)
                counter+=1
        connect.success="no"
        while(connect.success=="no"):
            try:
                connect()
            except:
                print ("Closing Connection")
                subprocess.call(['sudo' , 'poff', 'rnet'])
        
                while(counter!=5):
                    sleep(1)
                    counter+=1
                
                 
                 
        port2 = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=1)
        port2.write('AT'+'\r\n')
        rcv = port2.read(100)
        print rcv
        sleep(1)

        port2.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode
        rcv = port2.read(100)
        print rcv
        sleep(1)

                 # Sending a message to a particular Number
           
            
            
        to_send=re.findall(r"([0-9]{11})",connect.primary)
        to_send=to_send[0]
        port2.write('AT+CMGS="'+to_send+'"\r\n')
        rcv = port2.read(100)
        print rcv
        sleep(1)
           
        port2.write('Plate Number: '+plate_number+'\nDriver: '+lname+', '+fname+'\nVehicle Type: '+vehicle_type+'\nTime: '+timee+'\nLocation: '+connect.brgy+', '+connect.street+'\r\n')  # Message
        rcv = port2.read(1000)
        print rcv
     
        port2.write("\x1A") # Enable to send SMS
        rcv = port2.read(1000)
        print rcv
        sleep(3)

        port2.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode
        rcv = port2.read(100)
        print rcv
        sleep(3)

                 # Sending a message to a particular Number
           
            
            
        to_send=re.findall(r"([0-9]{11})",connect.primary)
        to_send=to_send[0]
        port2.write('AT+CMGS="'+to_send+'"\r\n')
        rcv = port2.read(100)
        print rcv
        sleep(3)
           
        port2.write(plate_number+'\nLink: \nhttps://www.openstreetmap.org/?mlat='+str(Lat)+'&mlon='+str(Lon)+'&zoom=18'+'\r\n')  # Message
        rcv = port2.read(1000)
        print rcv
     
        port2.write("\x1A") # Enable to send SMS
        rcv = port2.read(1000)
        print rcv
        sleep(1)
        
        sleep(3)

        
        check2=0
        while(check2!=connect.counter):
            port2.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode
            rcv = port2.read(100)
            print rcv
            sleep(1)

                 # Sending a message to a particular Number
           
            
            
            to_send=re.findall(r"([0-9]{11})",connect.phone[check2])
            to_send=to_send[0]
            port2.write('AT+CMGS="'+to_send+'"\r\n')
            rcv = port2.read(100)
            print rcv
            sleep(3)
                
            port2.write('Zip Code: '+connect.zipp+'\nPlate Number: '+plate_number+'\nDriver: '+lname+', '+fname+'\nVehicle Type: '+vehicle_type+'\nTime: '+timee+'\nLocation: '+connect.brgy+', '+connect.street+'\r\n')  # Message
            rcv = port2.read(1000)
            print rcv
     
            port2.write("\x1A") # Enable to send SMS
            rcv = port2.read(1000)
            print rcv
            sleep(3)

            port2.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode
            rcv = port2.read(100)
            print rcv
            sleep(3)

                 # Sending a message to a particular Number
           
            
            
            to_send=re.findall(r"([0-9]{11})",connect.phone[check2])
            to_send=to_send[0]
            port2.write('AT+CMGS="'+to_send+'"\r\n')
            rcv = port2.read(100)
            print rcv
            sleep(1)
           
            port2.write('Zip Code: '+connect.zipp+'\nPlate Number: '+plate_number+'\nLink: \nhttps://www.openstreetmap.org/?mlat='+str(Lat)+'&mlon='+str(Lon)+'&zoom=18'+'\r\n')  # Message
            rcv = port2.read(1000)
            print rcv
     
            port2.write("\x1A") # Enable to send SMS
            rcv = port2.read(1000)
            print rcv
            sleep(3)
            check2+=1
            sleep(5)
        fcount=0
	while (fcount<1200):
		print fcount
		fcount+=1
		sleep(1)
		if(fcount==1199):
			subprocess.call(['sudo','reboot'])
    if(sensor==1):
    	call()
    #if(sensor2==1):
        #call()
    #if(sensor3==1):
        #call()
    #if(sensor4==1):
        #call()
    

 

GPIO.cleanup()

