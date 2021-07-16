import time
import os
import RPi.GPIO as GPIO
import numpy as np
GPIO.setmode(GPIO.BCM)

#Weckzeit einstellbar machen durch Eingabe von Aussen!!!!!
weckzeit_stunde = 14
weckzeit_minute = 00


#6x4 Matrix [m x n]

GPIO.setup(21, GPIO.OUT) #[1.1] STUNDE10
GPIO.setup(20, GPIO.OUT) #[1.2]
GPIO.setup(4, GPIO.OUT) #[1.3]
GPIO.setup(17, GPIO.OUT) #[1.4]

GPIO.setup(27, GPIO.OUT) #[2.1] STUNDE1
GPIO.setup(22, GPIO.OUT) #[2.2]
GPIO.setup(14, GPIO.OUT) #[2.3]
GPIO.setup(15, GPIO.OUT) #[2.4]

GPIO.setup(18, GPIO.OUT) #[3.1] MINUTE10
GPIO.setup(23, GPIO.OUT) #[3.2]
GPIO.setup(24, GPIO.OUT) #[3.3]
GPIO.setup(25, GPIO.OUT) #[3.4]

GPIO.setup(8, GPIO.OUT) #[4.1] MINUTE1
GPIO.setup(7, GPIO.OUT) #[4.2]
GPIO.setup(12, GPIO.OUT) #[4.3]
GPIO.setup(16, GPIO.OUT) #[4.4]

GPIO.setup(10, GPIO.OUT) #[5.1] SEKUNDE10
GPIO.setup(9, GPIO.OUT) #[5.2]
GPIO.setup(11, GPIO.OUT) #[5.3]
GPIO.setup(5, GPIO.OUT) #[5.4]

GPIO.setup(6, GPIO.OUT) #[6.1] SEKUNDE1
GPIO.setup(13, GPIO.OUT) #[6.2]
GPIO.setup(19, GPIO.OUT) #[6.3]
GPIO.setup(26, GPIO.OUT) #[6.4]


A = np.array([[0,0,0,0,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,0,0]])

B = np.array([[26,5,16,25,15,17], #PINs eintragen!!!!!
              [19,11,12,24,14,4],
              [13,9,7,23,22,20],
              [6,10,8,18,27,21]])

def format(j,x):
    if x == 0:
        bin_1 = 0
        bin_2 = 0
        bin_4 = 0
        bin_8 = 0
    if x == 1:
        bin_1 = 1
        bin_2 = 0
        bin_4 = 0
        bin_8 = 0
    if x == 2:
        bin_1 = 0
        bin_2 = 1
        bin_4 = 0
        bin_8 = 0
    if x == 3:
        bin_1 = 1
        bin_2 = 1
        bin_4 = 0
        bin_8 = 0
    if x == 4:
        bin_1 = 0
        bin_2 = 0
        bin_4 = 1
        bin_8 = 0
    if x == 5:
        bin_1 = 1
        bin_2 = 0
        bin_4 = 1
        bin_8 = 0
    if x == 6:
        bin_1 = 0
        bin_2 = 1
        bin_4 = 1
        bin_8 = 0
    if x == 7:
        bin_1 = 1
        bin_2 = 1
        bin_4 = 1
        bin_8 = 0
    if x == 8:
        bin_1 = 0
        bin_2 = 0
        bin_4 = 0
        bin_8 = 1
    if x == 9:
        bin_1 = 1
        bin_2 = 0
        bin_4 = 0
        bin_8 = 1
    
    A[0][j] = bin_8
    A[1][j] = bin_4
    A[2][j] = bin_2
    A[3][j] = bin_1
        
def LED_Schalter(h10,h1):
    #zeit = time.strftime("%H", time.localtime())
    zeit = (h10*10)+h1
    #if int(zeit[0]) == 0:
    #    zeit = int(zeit[1])
    stellen = 4              #UEBERGANGSMODUS ohne SEKUNDEN
    
    if 8 <= zeit < 22:  #TAGMODUS von 8Uhr bis 22Uhr
        stellen = 6
        
    if zeit == 22:
        GPIO.output(15, GPIO.LOW)
        GPIO.output(14, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
        
        GPIO.output(17, GPIO.LOW)
        GPIO.output(4, GPIO.LOW)
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
        
    if 1 <= zeit < 7:   #NACHTMODUS von 1Uhr bis 6Uhr
        
        GPIO.output(15, GPIO.LOW)
        GPIO.output(14, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
        
        GPIO.output(17, GPIO.LOW)
        GPIO.output(4, GPIO.LOW)
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
        
        GPIO.output(25, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)
        
        GPIO.output(16, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(7, GPIO.LOW)
        GPIO.output(8, GPIO.LOW)
        
        GPIO.output(5, GPIO.LOW)
        GPIO.output(11, GPIO.LOW)
        GPIO.output(9, GPIO.LOW)
        GPIO.output(10, GPIO.LOW)
        
        GPIO.output(26, GPIO.LOW)
        GPIO.output(19, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        #GPIO.cleanup()
        return
   
    for n in range(stellen):
        for m in range(4):
            #if n == 5 or n == 4:        #NUR Sekunde1 und Sekunde10
            PIN = B[m][n]
            
            if A[m][n] == 1:
                GPIO.output(int(PIN), GPIO.HIGH)
            else:
                GPIO.output(int(PIN), GPIO.LOW)
                
def wecker():
    stunde = time.strftime("%H", time.localtime())
    minute = time.strftime("%M", time.localtime())
    
    if int(stunde) == weckzeit_stunde:
        if int(minute) == weckzeit_minute:
            print("Hier koennte Ihr Wecker klingeln")
            #Musik abspielen/ Buzzer/ Piepsen ... ueber GPIO
            #Musik ueber raspotify moeglich?
            
            os.system('python /home/pi/Documents/Python/AlarmClock/MusikWecker.py&')
            

def get_time_array():
    l = []
    for i in time.localtime()[3:6]:
        for j in "%02i" % i:
            l.append(int(j))
    print(l)
    for j in range(6):
        x = l[j]
        format(j,x)
    return l   

def tick():
    t = get_time_array()

def Test():
    for h10 in range(4):
        
        for h1 in range(10):
            
            for m10 in range(6):
                for m1 in range(10):
                    
                    for s10 in range(6):
                        for s1 in range(10):
                            
                            uhrzeit = [h10,h1,m10,m1,s10,s1]
                            #print(uhrzeit)
                            
                            for j in range(6):
                                x = uhrzeit[j]
                                format(j,x)
                                #return uhrzeit
                            #print(A)
                            LED_Schalter(h10,h1)
                            
                            if h10 == 2 and h1 == 3 and m10 == 5 and m1 == 9 and s10 == 5 and s1 == 9:
                                
                                GPIO.output(15, GPIO.LOW)
                                GPIO.output(14, GPIO.LOW)
                                GPIO.output(22, GPIO.LOW)
                                GPIO.output(27, GPIO.LOW)
                                
                                GPIO.output(17, GPIO.LOW)
                                GPIO.output(4, GPIO.LOW)
                                GPIO.output(20, GPIO.LOW)
                                GPIO.output(21, GPIO.LOW)
                                
                                GPIO.output(25, GPIO.LOW)
                                GPIO.output(24, GPIO.LOW)
                                GPIO.output(23, GPIO.LOW)
                                GPIO.output(18, GPIO.LOW)
                                
                                GPIO.output(16, GPIO.LOW)
                                GPIO.output(12, GPIO.LOW)
                                GPIO.output(7, GPIO.LOW)
                                GPIO.output(8, GPIO.LOW)
                                
                                GPIO.output(5, GPIO.LOW)
                                GPIO.output(11, GPIO.LOW)
                                GPIO.output(9, GPIO.LOW)
                                GPIO.output(10, GPIO.LOW)
                                
                                GPIO.output(26, GPIO.LOW)
                                GPIO.output(19, GPIO.LOW)
                                GPIO.output(13, GPIO.LOW)
                                GPIO.output(6, GPIO.LOW)
                                
                                return
                                
                            
                            time.sleep(0.000000001)


try: 
    while 1:
        
        
        Test()
        
        #tick()
        #print(A)
        #LED_Schalter()
        #wecker()
        #print("__________________")
        #time.sleep(1)

except KeyboardInterrupt:
    GPIO.output(21, GPIO.LOW) #anpassen!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    GPIO.output(20, GPIO.LOW)
    GPIO.output(4, GPIO.LOW)
    GPIO.output(17, GPIO.LOW)
    
    GPIO.output(27, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(14, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)
    
    GPIO.output(18, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)
    GPIO.output(24, GPIO.LOW)
    GPIO.output(25, GPIO.LOW)
    
    GPIO.output(8, GPIO.LOW)
    GPIO.output(7, GPIO.LOW)
    GPIO.output(12, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)
    
    GPIO.output(10, GPIO.LOW)
    GPIO.output(9, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(5, GPIO.LOW)
    
    GPIO.output(6, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(26, GPIO.LOW)
        
finally:
    GPIO.cleanup()