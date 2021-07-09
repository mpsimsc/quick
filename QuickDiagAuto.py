import subprocess
import datetime
import commands
import logging
import MySQLdb
import threading
import logging
import os
import time
import serial
import threading
from threading import Thread
from threading import Timer
from time import sleep
import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
import __DS4__
import lcd_i2c
version='PS5\PS4-6.0.4'
centre ='MPSI'
print version
print ':) Hello MPSI :) \n'
print 'DS4 sequence in Quick Diag version'
lcd_i2c.lcd_init()# Initialise display
lcd_i2c.lcd_string("V: "+version,lcd_i2c.LCD_LINE_1)
lcd_i2c.lcd_string("Quick Diag auto",lcd_i2c.LCD_LINE_2)

os.system("sudo setxkbmap fr")
#______________Config mahcine___________________
with open(".config/MACHINE.ini","r") as fd:
	global ini
	ini=fd.read().splitlines()
#*****base1***PS4***
nbMachine=ini[0][15:]
HostIp=ini[1][5:]
User=ini[2][5:]
Password=ini[3][9:]
DataBaseName=ini[4][14:]
#*****base2***PS5***
"""
HostIp1=ini[9][5:]
User1=ini[10][5:]
Password1=ini[11][9:]
DataBaseName1=ini[12][14:]
"""
HostIp1='192.168.252.42'
User1='root'
Password1='$mpsi$'
DataBaseName1='ps5suivi'


if len(nbMachine)==1:
	snMachine="QD"+"0"+nbMachine
	lcd_Nmachine="0"+nbMachine
else:
	snMachine="QD"+nbMachine
	lcd_Nmachine=nbMachine
#reporting = ini[5][13:]
reporting =''
fd.close()
host=snMachine

#__________________________________________________

bootTime=150
#mpsi panne Id code
global H090_id_code, V010_id_code, P010_id_code, D090_id_code, A010_id_code, A020_id_code, N000_id_code,A040_id_code, D010_id_code


H090_id_code="796"
V010_id_code="756"
P010_id_code="289"
D090_id_code="791"
A010_id_code="751"
A020_id_code="2881"
N000_id_code="727"
A040_id_code="796"
D010_id_code="791"


"""
if reporting =='mpsi':
        print" --->> mpsi config"
        lcd_i2c.lcd_string("V: "+version +" MPSI" + lcd_Nmachine,lcd_i2c.LCD_LINE_1)

        H090_id_code="796"
        V010_id_code="756"
        P010_id_code="289"
        D090_id_code="791"
        A010_id_code="751"
        A020_id_code="2881"
        N000_id_code="727"
elif reporting =='nwt':
        print" --->> NWT config"
        lcd_i2c.lcd_string("V : "+version +" NWT"+ lcd_Nmachine,lcd_i2c.LCD_LINE_1)
        H090_id_code="2192"
        V010_id_code="1383"
        P010_id_code="984"
        D090_id_code="954"
        A010_id_code="941"
        A020_id_code="942"
        N000_id_code="983"
elif reporting =='PS5mpsi':
        
        print" --->> PS5 config"
        lcd_i2c.lcd_string("V: "+version +" MPSI" + lcd_Nmachine,lcd_i2c.LCD_LINE_1)
        bootTime = bootTime -30
        nbMachine=ini[8][15:]
        HostIp=ini[9][5:]
        User=ini[10][5:]
        Password=ini[11][9:]
        DataBaseName=ini[12][14:]
        H090_id_code="796"
        V010_id_code="756"
        P010_id_code="289"
        D090_id_code="791"
        A010_id_code="751"
        A020_id_code="2881"
        N000_id_code="727"
        
else:
        print " --->> No config"
        lcd_i2c.lcd_string("V:"+version +" NoConfig",lcd_i2c.LCD_LINE_1)

"""
#__________________________________________________
                    
#HDDButton=3#26#19
CEButton=16#23
OKButton=37#22#22
#AffButton=3
#GPIO.setup(HDDButton, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(CEButton, GPIO.IN, GPIO.PUD_UP)
#GPIO.setup(AffButton, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(OKButton, GPIO.IN, GPIO.PUD_UP)


LedPassButtonG=23#26#40
LedPassButtonR=22#37#22#5#38
LedPassButtonB=19#26#16#36



GPIO.setup(LedPassButtonG,GPIO.OUT)
GPIO.setup(LedPassButtonR,GPIO.OUT)
GPIO.setup(LedPassButtonB,GPIO.OUT)



ButtonOff=True
CEC_HDMI=40#3
HDMI_5V=38#5
USB_5V=21#23
HDMI_GND=26 #5 #HDMI USB
GPIO.setup(CEC_HDMI,GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(HDMI_5V,GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(USB_5V,GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(HDMI_GND,GPIO.IN, GPIO.PUD_UP)




def checkConnection():
        global HostIp
        global User
        global Password
        global DataBaseName
        time.sleep(1)
        global lossconx
        while True:
                        
                if "reporting"=="reporting":
                        try:
                                db_2=MySQLdb.connect(HostIp,User,Password,DataBaseName)#CONNECT TO SERVER
                        
                                lossconx=True
                                
                                #print "CONNECTION SUCCESSFULL"
                                

                        except Exception as e:
                                print str(e)
                                #print "CAN'T CONNNECT TO DATABASE"
                                lossconx=False
                                led('LedPassButtonOFF')
                                sleep(1)
                                led ('LedPassButtonRON')
                                sleep(1)
                                led('LedPassButtonOFF')
                                sleep(1)
                                led ('LedPassButtonRON')
                                sleep(1)
                                led('LedPassButtonOFF')
                                sleep(1)
                                led ('LedPassButtonRON')
                                sleep(1)
                time.sleep(5)
                        

#_______________timeOut_________________

def stm():
    global startTime
    startTime=time.time()
def stConsole():
    global startTimeconsole
    startTimeconsole=time.time()
    
def timeout(tOut):
    if GPIO.input(CEC_HDMI):
        elapsed=int(time.time()-startTime)
        if elapsed>tOut:
            return False
        else:
            #if elapsed > 100:
            #        file2 = "/home/pi/PleaseCheckConsol.mp3"
            #        os.system("mpg123 " + file2)
            #        sleep(1)
            return True
    else : return False
def timeoutWithoutControl(tOut):
    
    elapsed=int(time.time()-startTime)
    if elapsed>tOut:
        return False
    else:
        return True

def led(x):
        
       
        
       
        if x=='LedPassButtonGON':
                GPIO.output(LedPassButtonG,GPIO.HIGH)
                GPIO.output(LedPassButtonR,GPIO.LOW)
                GPIO.output(LedPassButtonB,GPIO.LOW)

        elif x=='LedPassButtonBON':
                GPIO.output(LedPassButtonG,GPIO.LOW)
                GPIO.output(LedPassButtonR,GPIO.LOW)
                GPIO.output(LedPassButtonB,GPIO.HIGH)
        elif x=='LedPassButtonRON':
                GPIO.output(LedPassButtonG,GPIO.LOW)
                GPIO.output(LedPassButtonR,GPIO.HIGH)
                GPIO.output(LedPassButtonB,GPIO.LOW)
        elif x=='LedPassButtonOFF':
                GPIO.output(LedPassButtonG,GPIO.LOW)
                GPIO.output(LedPassButtonR,GPIO.LOW)
                GPIO.output(LedPassButtonB,GPIO.LOW)
        
       
                
        
def ledBlueBlink():
    global blink
    blink ='0'
    while True:
        
        if blink=='1':
                GPIO.output(LedPassButtonG,GPIO.LOW)
                GPIO.output(LedPassButtonR,GPIO.LOW)
                GPIO.output(LedPassButtonB,GPIO.LOW)
                sleep(0.5)
                GPIO.output(LedPassButtonG,GPIO.LOW)
                GPIO.output(LedPassButtonR,GPIO.LOW)
                GPIO.output(LedPassButtonB,GPIO.HIGH)
                sleep(0.5)
                
        else:
            sleep(1)
t = threading.Thread(target=ledBlueBlink, args=())
t.start()

led('LedPassButtonOFF')
led ('LedPassButtonGON')
sleep(2)
led ('LedPassButtonRON')
sleep(2)
led ('LedPassButtonBON')
sleep(2)
led('LedPassButtonOFF')
#led('LedPowerGON')
#sleep(4)

def Test_HDMI_USB():
        global state
        state =''
        if 1 ==1 :#not GPIO.input(HDMI_GND):
                sleep (2)
                for i in [1,2,3]:
                    sleep(0.5)
                    led ('LedPassButtonBON')
                    sleep(0.5)
                    led('LedPassButtonOFF')
                t=0
                tt=0
                ttt=0
                while GPIO.input(CEC_HDMI):
                    if GPIO.input(CEC_HDMI):
                            # in test boucle
                            print 'sleep 3s'
                            
                            log_file.write( 'Console In test boucle : sleep 3s')
                            #sleep(3) #test after 3s
                            while(ttt<4):
                                sleep(0.5)
                                led ('LedPassButtonBON')
                                sleep(0.5)
                                led('LedPassButtonOFF')
                                ttt=ttt+1

                            if GPIO.input(CEC_HDMI) and GPIO.input(HDMI_5V):
                            
                                    print 'sleep 20s'
                                    while(timeoutWithoutControl(30)):
                                        sleep(0.5)
                                        led ('LedPassButtonBON')
                                        sleep(0.5)
                                        led('LedPassButtonOFF')
                                        
                            
                                    #sleep(20) #test after 20s
                                    for i in [1,2,3,4,5,6,7,8]:
                                            if GPIO.input(CEC_HDMI) and GPIO.input(HDMI_5V) and GPIO.input(USB_5V):
                                                    print ' All test OK'
                                                    log_file.write(' All test voltage  == OK')
                                                    return (True,'All test OK')
                                            else:
                                                    sleep(2)
                                                    print " All test number:",i
                                                    if i==8 and not GPIO.input(HDMI_5V):
                                                            print "Copure Alim after boot 5V HDMI"
                                                            log_file.write("Copure Alim after boot 5V HDMI")
                                                            return (False,'CoupureAfterBOOT')
                                    
                                    if (GPIO.input(CEC_HDMI) and ((not GPIO.input(HDMI_5V) and GPIO.input(USB_5V)) or (  GPIO.input(HDMI_5V) and not GPIO.input(USB_5V))or (not GPIO.input(HDMI_5V) and not GPIO.input(USB_5V)))):
                                            # MCB NOK & BA G
                                            dbCEC=GPIO.input(CEC_HDMI)
                                            dbUSB_5V=GPIO.input(USB_5V)
                                            dbHDMI_5V=GPIO.input(HDMI_5V)
                                            print'----------   CEC',GPIO.input(CEC_HDMI)
                                            
                                            print'----------   5V',GPIO.input(HDMI_5V)
                                            
                                            print '.......   USB',GPIO.input(USB_5V)
                                            
                                            print ' MCB NOK & BA G'
                                            return (False,' MCB NOK & BA G')
                                    else:
                                            print ' Copure TEST after 20s'
                                            return (False,' Copure TEST after 20s')
                                            

                            elif GPIO.input(CEC_HDMI) and not GPIO.input(HDMI_5V):
                                    #MCB NG  &  BA  OK
                                    ttt=0
                                    print 'MCB NG  &  BA  OK  ---  ',t
                                    log_file.write('MCB NG  &  BA  OK  ---  %s'+str(t))
                                    t=t+1
                                    if t == 5:return (False,'MCB NG  &  BA  OK')
                            else:
                                    print ' Copure TEST after 3s'
                                    log_file.write('Copure TEST after 3s')
                    elif not GPIO.input(CEC_HDMI):
                            #BA   NG
                            print 'BA NG'
                            state = "pb block alim"
                            return (None,'BA NG')
                            
                while(tt<5):      
                    if not GPIO.input(CEC_HDMI) and GPIO.input(HDMI_5V) and GPIO.input(USB_5V):
                    
                            print " BA OK  ,   MCB OK,    pb port HDMI"
                            log_file.write("BA OK  ,   MCB OK,    pb port HDMI")
                            if tt==4:return (False," BA OK  ,   MCB OK,    pb port HDMI")
                            sleep(3)
                            tt=tt+1
                    else:
                            tt=tt+1
                            print 'CEC_HDMI HDMI_5V USB_5V ---- ---  ',tt
                            log_file.write('CEC_HDMI HDMI_5V USB_5V ---- ---  %s'+str(tt))
                            sleep(3)
        else:
                sleep(1)
                print 'no console'
        return (None,'None')

def getSN():
        global state
        global snkeyboard
        global idsym
        #_______________________
        global HostIp
        global User
        global Password
        global DataBaseName
        global reporting
        global HostIp1
        global User1
        global Password1
        global DataBaseName1
        #_______________________
        global idsn
        global id_sn
        global sn
        global snOld
        global sn_Old
        global mvt
        global statut
        global Model
        global ModelNumber
        global Colour
        global nextJob
        global snpalette_in
        global mvt_in
        #_______________________

        #_______________________
        global log_file
        global filename
        #_______________________
        global verrou
        #_______________________
        global H090_id_code, V010_id_code, P010_id_code, D090_id_code, A010_id_code, A020_id_code, N000_id_code, A040_id_code, D010_id_code

        try:
                a=""
                a = raw_input('get SN consol ')
                
                for j in ['V010','A020','N000','H090','X050','A010','D090','P010','1111','A040','D010']:
                        
                      
                        if a in j and a=='H090':
                                idsym=H090_id_code
                                print "------------> Problem HDD"
                                log_file.write( " getSN ------------> Problem HDD")
                                lcd_i2c.lcd_string("--> HDD" ,lcd_i2c.LCD_LINE_1)
                                led('LedPassButtonRON')
                                return a
                        elif a in j and a=='V010':
                                idsym=V010_id_code
                                print " ------------> Problem CEB"
                                log_file.write( "getSN ------------> Problem CEB")
                                lcd_i2c.lcd_string("clignote en bleu" ,lcd_i2c.LCD_LINE_1)
                                led('LedPassButtonRON')
                                return a
                        elif a in j and a=='P010':
                                idsym=P010_id_code
                                print "------------> Aff"
                                log_file.write("getSN ------------> Aff")
                                lcd_i2c.lcd_string("--> Affichage" ,lcd_i2c.LCD_LINE_1)
                                led('LedPassButtonRON')
                                return a
                        elif a in j and a=='D090':
                                idsym=D090_id_code
                                print "------------> BD"
                                log_file.write(" getSN ------------> BD")
                                lcd_i2c.lcd_string("--> Blue-Ray" ,lcd_i2c.LCD_LINE_1)
                                led('LedPassButtonRON')
                                return a
                        elif a in j and a=='A040':
                                idsym=H090_id_code
                                print "------------> Problem HDD"
                                log_file.write( " getSN ------------> Problem HDD")
                                lcd_i2c.lcd_string("--> HDD" ,lcd_i2c.LCD_LINE_1)
                                led('LedPassButtonRON')
                                return a
                        elif a in j and a=='D010':
                                idsym=D090_id_code
                                print "------------> BD"
                                log_file.write(" getSN ------------> BD")
                                lcd_i2c.lcd_string("--> Blue-Ray" ,lcd_i2c.LCD_LINE_1)
                                led('LedPassButtonRON')
                                return a
                        elif a in j and a=='N000':
                                idsym=N000_id_code
                                print "------------> console OK"
                                log_file.write("getSN ------------> console OK")
                                lcd_i2c.lcd_string("--> NFF" ,lcd_i2c.LCD_LINE_1)
                                led('LedPassButtonGON')
                                
                                Real_sn_consol=sn_consol
                                return a
                        
                        
                str(a)

                sleep(1)


                
                try:
                        if (len(a)==17) and (a[0] in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ')):
                                print 'SN ps5  : ',a
                                #---------------------------------------------
                                lcd_i2c.lcd_init()# Initialise display
                                lcd_i2c.lcd_string( a[1:18],lcd_i2c.LCD_LINE_1)
                                #---------------------------------------------
                                reporting ='PS5'
                                #_________________________________________________________
                                filename='Downloads/'+a+"__"+time.asctime()+'.txt'
                                log_file = open(filename,"w")
                                #_________________________________________________________
                        elif(len(a)==17):
                                print 'SN ps4  : ',a
                                #---------------------------------------------
                                lcd_i2c.lcd_init()# Initialise display
                                lcd_i2c.lcd_string( a[1:18],lcd_i2c.LCD_LINE_1)
                                #---------------------------------------------
                                reporting ='PS4'
                                #_________________________________________________________
                                filename='Downloads/'+a+"__"+time.asctime()+'.txt'
                                log_file = open(filename,"w")
                                #_________________________________________________________

                        if reporting == "PS4":
                                _mvtidnextjob=''
                                #blink led bleu
                                led ('LedPassButtonBON')
                                sleep(0.7)
                                led('LedPassButtonOFF')
                                try:
                                        db_2=MySQLdb.connect(HostIp,User,Password,DataBaseName,connect_timeout=4)#CONNECT TO SERVER
                                        cursor_2=db_2.cursor()

                                        cursor_2.execute("SELECT sn.idsn, sn.sn,sn.snOld,sn.mvt,sn.statut,sn.Model,sn.ModelNumber,sn.Colour,sn.nextJob,snpalette_in,mvt_in FROM ps3suivi.sn sn WHERE (sn.snOld = %s)",[a])
                                        snInfo= cursor_2.fetchone()
                                        print snInfo
                                        log_file.write('\n ------------------------------------------------------------------------------------------ \n \n \n')
                                        log_file.write('#####________HELLO WORLD : Quick Diag________###### \n')
                                        log_file.write("sn.idsn, sn.sn,sn.snOld,sn.mvt,sn.statut,sn.Model,sn.ModelNumber,sn.Colour,sn.nextJob,snpalette_in,mvt_in \n")
                                        log_file.write(str(snInfo))
                                        idsn=snInfo[0]
                                        sn=snInfo[1]
                                        snOld=snInfo[2]
                                        mvt=snInfo[3]
                                        statut=snInfo[4]
                                        Model=snInfo[5]
                                        ModelNumber=snInfo[6]
                                        Colour=snInfo[7]
                                        nextJob=snInfo[8]
                                        snpalette_in=snInfo[9]
                                        mvt_in=snInfo[10]
                                        db_2.commit()
                                        sleep(0.5)
                                        if snpalette_in== None and  mvt_in== None:
                                                print "snpalette_in,mvt_in ok"
                                                if (nextJob=='Reception' or  nextJob=='PreDiag') and  statut=='VALIDE':
                                                        print "verrou OK"
                                                        verrou = True
                                                else :
                                                        print "verrou NNNOK"
                                                        log_file.write(" Consol Not in the corect post \n ")
                                                        for i in [1,2,3,4,5]:
                                                                file = "/home/pi/pleaseCheckNextJob.mp3"
                                                                os.system("mpg123 " + file +"&")
                                                                led ('LedPassButtonRON')
                                                                lcd_i2c.lcd_string("Error NextJob" ,lcd_i2c.LCD_LINE_2)
                                                                sleep(0.7)
                                                                led('LedPassButtonOFF')
                                                                lcd_i2c.lcd_string("" ,lcd_i2c.LCD_LINE_2)
                                                                sleep(0.7)
                                                                
                                                                lcd_i2c.lcd_string("Error NextJob" ,lcd_i2c.LCD_LINE_2)
                                                        verrou = False
                                        else:
                                                print "snpalette_in,mvt_in NNNok"
                                                log_file.write(" Consol Not in the corect post/n ")
                                                for i in [1,2,3,4,5]:
                                                        file = "/home/pi/pleaseCheckNextJob.mp3"
                                                        os.system("mpg123 " + file +"&")
                                                        led ('LedPassButtonRON')
                                                        lcd_i2c.lcd_string("Error NextJob" ,lcd_i2c.LCD_LINE_2)
                                                        sleep(0.7)
                                                        led('LedPassButtonOFF')
                                                        lcd_i2c.lcd_string("" ,lcd_i2c.LCD_LINE_2)
                                                        sleep(0.7)
                                                verrou = False
                                
                                except Exception as e:
                                        print str(e)
                                        try:
                                                db.rollback()
                                                print "CAN't CONNECT TO DATABASE"
                                                db.close()#DISCONNECT FROM SERVER
                                                lcd_i2c.lcd_string("Sn Not found" ,lcd_i2c.LCD_LINE_2)
                                                sleep(1)
                                                return False
                                        except:
                                                print 'db.connect pb db !E'
                                                lcd_i2c.lcd_string("Sn Not found" ,lcd_i2c.LCD_LINE_2)
                                                sleep(1)
                                                return False
                        
                        elif reporting == "PS5":
                                led ('LedPassButtonBON')
                                sleep(0.7)
                                led('LedPassButtonOFF')
                                #print " Insert PS5 db"
                                #print "verrou PS5 OK"
                                #verrou = True

                                try:
                                        db=MySQLdb.connect(HostIp1,User1,Password1,DataBaseName1,connect_timeout=4)#CONNECT TO SERVER
                                        cursor=db.cursor()
                                        cursor.execute("SELECT id_sn, sn,snold,(SELECT cl_movement.Mvt FROM  cl_movement WHERE  cl_movement.id_mvt = sn.id_movement)AS Mvt,cl_statut.Statut,(SELECT cl_movement.Mvt FROM cl_movement WHERE cl_movement.id_mvt = sn.id_nextjob) AS NextJob,cl_model_console.model FROM sn LEFT JOIN cl_statut ON sn.id_statut = cl_statut.id_statut LEFT JOIN cl_model_console ON sn.id_model = cl_model_console.id_model_consol WHERE snold=%s",[a])
                                        snInfo= cursor.fetchone()
                                        print snInfo
                                        log_file.write('\n ------------------------------------------------------------------------------------------ \n \n \n')
                                        log_file.write('#####________HELLO WORLD : Quick Diag________###### \n')
                                        log_file.write("sn.idsn, sn.sn,sn.snOld,sn.mvt,sn.statut,sn.Model,sn.ModelNumber,sn.Colour,sn.nextJob,snpalette_in,mvt_in \n")
                                        log_file.write(str(snInfo))
                                        id_sn=snInfo[0]
                                        sn=snInfo[1]
                                        sn_Old=snInfo[2]
                                        mvt=snInfo[3]
                                        statut=snInfo[4]
                                        nextJob=snInfo[5]
                                        Model=snInfo[6]
                                        db.commit()

                                        sleep(0.5)

                                        if (nextJob=='Quick-Diag' or nextJob=='Reception') and  statut=='VALIDE':
                                                print "verrou OK"
                                                verrou = True
                                        else :
                                                print "verrou NNNOK"
                                                log_file.write(" Consol Not in the corect post \n ")
                                                for i in [1,2,3,4,5]:
                                                        file = "/home/pi/pleaseCheckNextJob.mp3"
                                                        os.system("mpg123 " + file +"&")
                                                        led ('LedPassButtonRON')
                                                        lcd_i2c.lcd_string("Error NextJob" ,lcd_i2c.LCD_LINE_2)
                                                        sleep(0.7)
                                                        led('LedPassButtonOFF')
                                                        lcd_i2c.lcd_string("" ,lcd_i2c.LCD_LINE_2)
                                                        sleep(0.7)       
                                                        lcd_i2c.lcd_string("Error NextJob" ,lcd_i2c.LCD_LINE_2)
                                                verrou = False

                                except Exception as e:
                                        print str(e)
                                        try:
                                                db.rollback()
                                                print "CAN't CONNECT TO DATABASE"
                                                db.close()#DISCONNECT FROM SERVER
                                                lcd_i2c.lcd_string("Sn Not found" ,lcd_i2c.LCD_LINE_2)
                                                sleep(1)
                                                return False
                                        except:
                                                print 'db.connect pb db !E'
                                                lcd_i2c.lcd_string("Sn Not found" ,lcd_i2c.LCD_LINE_2)
                                                sleep(1)
                                                return False
                                
                        return a
                except AssertionError:
                        print 'FAIL : lenght error'
                        return "Consol"
                except ValueError:
                        try:
                                int(a)
                                return a
                        except ValueError:
                                print "FAIL SN "
                                return False
                except Exception as e:
                        print 'other error'
                        print e
                        return False
        except :
                os.system("sudo setxkbmap fr")
                print "pb read SN switch FR or EN"
                return "Consol"
        
def thsn():
	global sn_consol
	sn_consol="Consol"
	while True:
             sn_consol=getSN()   
		
th=Thread(target=thsn)

def stConsole():
    global startTimeconsole
    startTimeconsole=time.time()


global blink
global state
#-------------------------------------
third_thread=threading.Thread(target=checkConnection)
third_thread.start()


#_______________________________ DS4 Sequence __________________________________
#_SH=37
_L1=35
_R=33
_UP=32
_LL=31
_DN=29
_PS=24
_XX=18
_O=15
#_tri=16
_R1=13
_car=12
_OP=11
#GND
AP=7

def My_sleep_for_this_prog(tOut1):
    global idsym
    startTime_=time.time()
    while(__DS4__.powerDetect() and idsym ==" "):
        elapsed=int(time.time()-startTime_)
        sleep(1)
        if (elapsed>tOut1):
            #print " console ON" 
            break

def DS4_sequence():
        global idsym
        global reporting
        #print __DS4__.__DS4_pairing_()
        #if reporting == "mpsi" or reporting == "nwt":
        if reporting == "PS4" :
                print "ps4 sequence"
                if not __DS4__.powerDetect() or idsym !=" " : return False
                else :
                    __DS4__.buttonPressLOW(_XX)
                    __DS4__.buttonPressLOW(_XX)
                if not __DS4__.powerDetect() or idsym !=" " : return False
                else :__DS4__.buttonPressLOW(_XX)
                if not __DS4__.powerDetect() and idsym ==" "  : return None  # consol with HDD pb turn off
                elif not __DS4__.powerDetect() or idsym !=" " : return False
                else :__DS4__.buttonPressLOW(_XX)
                My_sleep_for_this_prog(3)
                if not __DS4__.powerDetect() and idsym ==" "  : return None  # consol with HDD pb turn off
                elif not __DS4__.powerDetect() or idsym !=" " : return False
                else :__DS4__.buttonPressLOW(_LL)
                if not __DS4__.powerDetect() and idsym ==" "  : return None  # consol with HDD pb turn off
                elif not __DS4__.powerDetect() or idsym !=" " : return False
                else :__DS4__.buttonPressLOW(_LL)
                if not __DS4__.powerDetect() or idsym !=" " : return False
                else :__DS4__.buttonPressLOW(_XX)
                My_sleep_for_this_prog(3)
                if not __DS4__.powerDetect() or idsym !=" " : return False
                else :__DS4__.buttonPressLOW(_O)   
                if not __DS4__.powerDetect() or idsym !=" " : return False
                else :__DS4__.buttonPressLOW(_O)
                if not __DS4__.powerDetect() or idsym !=" " : return False
                else :__DS4__.buttonPressLOW(_PS)
                if not __DS4__.powerDetect() or idsym !=" " : return False
                else :__DS4__.buttonPressLOW(_XX)
                if not __DS4__.powerDetect() or idsym !=" " : return False
                else :__DS4__.buttonPressLOW(_O)
                return True
        elif reporting == "PS5":
                print "ps5 sequence"
                if not __DS4__.powerDetect() or idsym !=" " : return False
                else :
                        __DS4__.buttonPressLOW(_XX)
                        __DS4__.buttonPressLOW(_XX)
                        My_sleep_for_this_prog(6)
                        __DS4__.buttonPressLOW(_XX)
                        __DS4__.buttonPressLOW(_XX)
                
                if not __DS4__.powerDetect() or idsym !=" " : return False
                else :
                        __DS4__.buttonPressLOW(_O)
                        __DS4__.buttonPressLOW(_O)
                return True

#______________ main ___________

    
if __name__=='__main__':
    global idsn
    global id_sn
    global sn
    global snOld
    global sn_Old
    global mvt
    global statut
    global Model
    global ModelNumber
    global Colour
    global nextJob
    global snpalette_in
    global mvt_in
    #logging.info('Nano power OK')
    #logging.warning('Nano power FAIL')

    th.start()
    
    start_Test=True
    dbHDDButton=0
    dbCEButton=0
    dbAffButton=0
    dbOKButton=0
    dbPowerOff=0
    dbCEBButton=0
    global idsym
    idsym=" "
    QuickAuto='' #29/01/2021
    global log_file

    global verrou
    verrou = False 
    while True: 
        sleep(3)

        a=0
       
        if not GPIO.input(HDMI_GND) and start_Test and a==0 and (("Consol" not in sn_consol) and ("Problem" not in sn_consol) )and verrou == True:

            Real_sn_consol=sn_consol
            print "Console UP"
            
            stConsole() # start time console var: startTimeconsole
            print "\n ~~~~  :D     :)     ;)  ~~~~ \n"
            log_file.write("\n ~~~~  :D     :)     ;)  ~~~~ \n")
            print 'console is up',time.asctime()
            log_file.write('SN ::  '+Real_sn_consol +' is UP \n')
            
            idsym=" "
            
            lcd_i2c.lcd_string("Test Start ..." ,lcd_i2c.LCD_LINE_2)
            
            led('AllLedOFF')
            
            stm()  # start time
            led ('LedPassButtonBON')
            sleep(6)
            while(timeoutWithoutControl(5)):
                sleep(0.5)
                led ('LedPassButtonBON')
                sleep(0.5)
                led('LedPassButtonOFF')
            start_Test=False
            _Test_HDMI_USB_=None
            panne=''
            
            (_Test_HDMI_USB_,panne)=Test_HDMI_USB()
            print (_Test_HDMI_USB_,panne)
            log_file.write('result Test (_Test_HDMI_USB_,panne) =('+ str(_Test_HDMI_USB_)+ str(panne) +')\n')
            if _Test_HDMI_USB_ ==True: print "_Test_HDMI_USB_   ===   OK "#led('LedMCBGON')
            elif _Test_HDMI_USB_ ==False: led('LedPassButtonRON')
            elif _Test_HDMI_USB_ ==None: led('LedPassButtonBON')
            _AffiButton_= None
            a = False

            if GPIO.input(CEC_HDMI) and _Test_HDMI_USB_==True:
                
                print "Wait boot console"
                led('LedPassButtonGON')
                breakwhile=True
                while(timeoutWithoutControl(bootTime) and breakwhile) :
                    sleep(0.5)
                    led ('LedPassButtonBON')
                    sleep(0.5)
                    led('LedPassButtonOFF')
                    for j in ['V010','A020','N000','H090','X050','A010','D090','P010','1111','A040','D010']:
                        if sn_consol in j and sn_consol=='N000':
                                led('LedPassButtonGON')
                                breakwhile=False
                                log_file.write('While boocle break NOOO \n')
                                
                        elif sn_consol in j and sn_consol!='N000':
                                led('LedPassButtonRON')
                                breakwhile=False      
                                log_file.write('While boocle break NOT NOOO \n')
                

                ButtonOff_1=True
                PassAuto=False
                print "----------------- BOOT OK ---------------"
                log_file.write("----------------- BOOT OK --------------- \n")
                idsym=" "
                
                if 'H090' in sn_consol:
                        
                        idsym=H090_id_code
                        dbHDDButton=1
                        print "------------> Problem HDD"
                        log_file.write("------------> Problem HDD  \n")
                        led ('LedPassButtonRON')
                        ButtonOff_2=False
                elif 'A040' in sn_consol:
                        
                        idsym=H090_id_code
                        dbHDDButton=1
                        print "------------> Problem HDD"
                        log_file.write("------------> Problem HDD  \n")
                        led ('LedPassButtonRON')
                        ButtonOff_2=False
                elif 'V010' in sn_consol:
                        idsym=V010_id_code
                        dbCEBButton=1
                        print "------------> CEB"
                        log_file.write("------------> CEB \n")
                        led ('LedPassButtonRON') 
                        ButtonOff_2=False
                elif 'X050' in sn_consol :
                        idsym="1023"
                        dbCEButton=1
                        print "------------> Problem CE"
                        log_file.write("------------> Problem CE \n")
                        led ('LedPassButtonRON')
                        ButtonOff_2=False
                elif 'P010' in sn_consol:
                        idsym=P010_id_code
                        dbAffButton=1
                        print "------------> Aff"
                        log_file.write("------------> Aff \n")
                        led ('LedPassButtonRON')
                        ButtonOff_2=False
                elif 'D090' in sn_consol:
                        idsym=D090_id_code
                        dbAffButton=1
                        print "------------> BD"
                        log_file.write("------------> BD \n")
                        led ('LedPassButtonRON')
                        ButtonOff_2=False
                elif 'D010' in sn_consol:
                        idsym=D090_id_code
                        dbAffButton=1
                        print "------------> BD"
                        log_file.write("------------> BD \n")
                        led ('LedPassButtonRON')
                        ButtonOff_2=False

                elif 'N000' in sn_consol:
                        idsym=N000_id_code
                        dbOKButton=1
                        print "------------> console OK"
                        log_file.write("------------> console OK \n")
                        led ('LedPassButtonGON')
                        ButtonOff_2=False
                elif not GPIO.input(CEC_HDMI):
                        sleep(1)
                        if not GPIO.input(CEC_HDMI):
                                sleep(1)
                                if not GPIO.input(CEC_HDMI):
                                        idsym=A020_id_code
                                        panne='consol POWER OFF'
                                        dbPowerOff=1
                                        print "------------> console POWER OFF "
                                        lcd_i2c.lcd_string("Coupure d'Alim" ,lcd_i2c.LCD_LINE_1)
                                        log_file.write("------------> console POWER OFF \n")
                                        led ('LedPassButtonRON')
                                        ButtonOff_2=False
                                

                    
                PassAuto=True
                sleep(1)
                if (PassAuto==True and breakwhile):
                      
                        blink='1'
                        log_file.write("------------> START sequence __DS4__.__modePS_go_to_ErrorHistory_QS \n")
                        print __DS4__.__DS4_pairing_()
                        if DS4_sequence() == None :
                                sn_consol = 'H090'  # forcer panne HDD : case consol with turn off
                                QuickAuto='H090' #29/01/2021
                        log_file.write("------------>  sequence __DS4__.__modePS_go_to_ErrorHistory_QS --> DONE \n")
                        blink='0'
                        led ('LedPassButtonBON')
                        
                        ButtonOff_2=True
                        while (ButtonOff_2):
                            #______________________________________________________
                            lcd_i2c.lcd_string("CheckConsolState",lcd_i2c.LCD_LINE_2)
                            sleep(1.5)
                            lcd_i2c.lcd_string("Scan Code ...",lcd_i2c.LCD_LINE_2)
                            sleep(1.5)   
                            #______________________________________________________  
                            if 'H090' in sn_consol:
                                idsym=H090_id_code
                                dbHDDButton=1
                                print "------------> Problem HDD"
                                log_file.write("------------> Problem HDD\n")
                                lcd_i2c.lcd_string("--> HDD" ,lcd_i2c.LCD_LINE_1)# forcer panne HDD : case consol with turn off
                                led ('LedPassButtonRON')
                                ButtonOff_2=False
                            elif 'A040' in sn_consol:
                                idsym=H090_id_code
                                dbHDDButton=1
                                print "------------> Problem HDD"
                                log_file.write("------------> Problem HDD\n")
                                lcd_i2c.lcd_string("--> HDD" ,lcd_i2c.LCD_LINE_1)# forcer panne HDD : case consol with turn off
                                led ('LedPassButtonRON')
                                ButtonOff_2=False
                            elif 'V010' in sn_consol:
                                idsym=V010_id_code
                                dbCEBButton=1
                                print "------------> CEB"
                                log_file.write("------------> CEB \n")
                                led ('LedPassButtonRON') 
                                ButtonOff_2=False
                            elif 'X050' in sn_consol :
                                idsym="1023"
                                dbCEButton=1
                                print "------------> Problem CE"
                                log_file.write("------------> Problem CE \n")
                                led ('LedPassButtonRON')
                                ButtonOff_2=False
                            elif 'P010' in sn_consol:
                                idsym=P010_id_code
                                dbAffButton=1
                                print "------------> Aff"
                                log_file.write("------------> Aff \n")
                                led ('LedPassButtonRON')
                                ButtonOff_2=False
                            elif 'D010' in sn_consol:
                                idsym=D090_id_code
                                dbAffButton=1
                                print "------------> BD"
                                log_file.write("------------> BD \n")
                                led ('LedPassButtonRON')
                                ButtonOff_2=False
                            elif 'D090' in sn_consol:
                                idsym=D090_id_code
                                dbAffButton=1
                                print "------------> BD"
                                log_file.write("------------> BD \n")
                                led ('LedPassButtonRON')
                                ButtonOff_2=False
                            elif 'N000' in sn_consol:
                                idsym=N000_id_code
                                dbOKButton=1
                                print "------------> console OK"
                                log_file.write("------------> console OK \n")
                                led ('LedPassButtonGON')
                                ButtonOff_2=False
                            elif not GPIO.input(CEC_HDMI):
                                sleep(1)
                                if not GPIO.input(CEC_HDMI):
                                        sleep(1)
                                        if not GPIO.input(CEC_HDMI):
                                                idsym=A020_id_code
                                                panne='consol POWER OFF'
                                                dbPowerOff=1
                                                print "------------> console POWER OFF "
                                                lcd_i2c.lcd_string("Coupure d'Alim" ,lcd_i2c.LCD_LINE_1)
                                                log_file.write("------------> console POWER OFF \n")
                                                led ('LedPassButtonRON')
                                                ButtonOff_2=False
                                
                            
            
            elif idsym == " " and _Test_HDMI_USB_==False and not GPIO.input(USB_5V) and ('CoupureAfterBOOT'in panne or 'MCB NG  &  BA  OK' in panne) :
                
                idsym=A020_id_code
                panne='consol POWER OFF'
                print "------------> console POWER OFF "
                lcd_i2c.lcd_string("Coupure d'Alim" ,lcd_i2c.LCD_LINE_1)
                led ('LedPassButtonRON')
                log_file.write("------------> console POWER OFF ,idsym=2881 \n")
                log_file.write(" ==> Test result  _Test_HDMI_USB_ NG  CoupureAfterBOOT OR MCB NG  &  BA  OK \n")
                
            elif idsym == " " and  not GPIO.input(CEC_HDMI) and GPIO.input(HDMI_5V) and GPIO.input(USB_5V):
                idsym=P010_id_code
                panne='CEC not found'
                led('LedPassButtonRON')
                log_file.write(" CEC_HDMI=0,  HDMI_5V=1, USB_5V=1")
                log_file.write("------------> Aff")
                lcd_i2c.lcd_string("--> Affichage" ,lcd_i2c.LCD_LINE_1)
                QuickAuto='T020' #29/01/2021
                code='T020'
                
            elif idsym == " " and not GPIO.input(CEC_HDMI) and not GPIO.input(HDMI_5V) and GPIO.input(USB_5V):
                idsym=P010_id_code
                print 'CEC not found & 5v hdmi not found'
                panne='CEC not found & 5v hdmi not found'
                led('LedPassButtonRON')
                log_file.write(" CEC_HDMI=0,  HDMI_5V=0, USB_5V=1")
                log_file.write("------------> Aff \n")
                lcd_i2c.lcd_string("--> Affichage" ,lcd_i2c.LCD_LINE_1)
                QuickAuto='T020' #29/01/2021
                code='T020'
                
            elif idsym == " " and GPIO.input(CEC_HDMI) and not GPIO.input(HDMI_5V) and GPIO.input(USB_5V):
                idsym=P010_id_code
                print 'CEC exist & 5v hdmi not found & 5v usb exist'
                panne='CEC exist & 5v hdmi not found & 5v usb exist'
                led('LedPassButtonRON')
                log_file.write(" CEC_HDMI=0,  HDMI_5V=0, USB_5V=1")
                log_file.write("------------> Aff \n")
                lcd_i2c.lcd_string("--> Affichage" ,lcd_i2c.LCD_LINE_1)
                QuickAuto='T020' #29/01/2021
                code='T020'
                
            elif idsym == " " and  GPIO.input(CEC_HDMI) and GPIO.input(HDMI_5V) and not GPIO.input(USB_5V):
                    
                
                #idsym="999"#1204"

                breakwhile2=True
                while(breakwhile2 ) :
                    print "CEC exist 5v hdmi exist and usb 5 v not found"
                    #sleep(2)
                    led ('LedPassButtonBON')
                    #______________________________________________________
                    lcd_i2c.lcd_string("CheckConsolState",lcd_i2c.LCD_LINE_2)
                    sleep(1.5)
                    lcd_i2c.lcd_string("Scan Code ...",lcd_i2c.LCD_LINE_2)
                    sleep(1.5)   
                    #______________________________________________________ 

                    for j in ['V010','A020','N000','H090','X050','A010','D090','P010','1111','A040','D010']:
                        if sn_consol in j and sn_consol=='N000':
                                led('LedPassButtonRON')
                                breakwhile2=False
                                idsym=V010_id_code #forcer le resulta CEB
                                lcd_i2c.lcd_string("Clignote en bleu" ,lcd_i2c.LCD_LINE_1)
                                QuickAuto='V010' #29/01/2021
                        elif sn_consol in j and sn_consol!='N000':
                                led('LedPassButtonRON')
                                breakwhile2=False

                    if not GPIO.input(CEC_HDMI):
                            breakwhile2=False
                            idsym=A020_id_code
                            panne='consol POWER OFF'
                            dbPowerOff=1
                            print "------------> console POWER OFF "
                            lcd_i2c.lcd_string("Coupure d'Alim" ,lcd_i2c.LCD_LINE_1)
                            led ('LedPassButtonRON')
                            
                log_file.write(" CEC_HDMI=1,  HDMI_5V=1, USB_5V=0 \n")
                log_file.write("------------> "+ sn_consol +'\n')
            elif idsym == " " and not GPIO.input(CEC_HDMI) and not GPIO.input(HDMI_5V) and not GPIO.input(USB_5V):
                print "------------- pas d Alim"
                idsym=A010_id_code
                led('LedPassButtonRON')
                log_file.write(" CEC_HDMI=0,  HDMI_5V=0, USB_5V=0 \n")
                log_file.write("------------> No power \n")
                lcd_i2c.lcd_string("--> pas d'Alim" ,lcd_i2c.LCD_LINE_1)





        #reporting
        elif GPIO.input(HDMI_GND) and not start_Test:
            print "Console Done"
            print 'console is down',time.asctime()
            log_file.write('console is down ' +time.asctime() +'\n')
            connTime=(time.time()-startTimeconsole)/60
            print "Console connection time :",connTime
            log_file.write('Console connection time : '+str(connTime) +'\n')
            print "idsym :::::::::::::::::::::  ",idsym
            log_file.write("Insertion db Done  with idsym = "+idsym+ '\n \n')

            uid=snMachine
            host=snMachine

            idcode=idsym
            
            if idcode== H090_id_code:
                    code="H090"
                    mcbstatut='PANNE' #'VALIDE'
            elif idcode== A040_id_code:
                    code="H090"
                    mcbstatut='PANNE' #'VALIDE'
            elif idcode== V010_id_code:
                    code="V010"
                    mcbstatut='PANNE'
            elif idcode== P010_id_code:
                    code="P010"
                    mcbstatut='PANNE'
            elif idcode== D090_id_code:
                    code="D090"
                    mcbstatut='PANNE'
            elif idcode== D010_id_code:
                    code="D090"
                    mcbstatut='PANNE'
            elif idcode== A010_id_code:
                    code="A010"
                    mcbstatut='PANNE'
            elif idcode== A020_id_code:
                    code="A020"
                    mcbstatut='PANNE'
            elif idcode==N000_id_code:
                    code="N000"
                    mcbstatut='PANNE'#VALIDE'
                    
            #___________________________________________________________________
            if  code =="P010" or code =="A020" or code=="V010":
                    if QuickAuto =="T020":
                            lcd_i2c.lcd_string('--> '+QuickAuto + '  MCB',lcd_i2c.LCD_LINE_2)
                            print "LCD  : T020 "
                    else:
                            lcd_i2c.lcd_string('--> '+code + '  MCB',lcd_i2c.LCD_LINE_2)
            else:
                    
                    lcd_i2c.lcd_string('--> '+code ,lcd_i2c.LCD_LINE_2)

            #__________________________________________________________________
                    
            print " /n --- idcode:   ",idcode
            print "/n --- code  :   ",code
            print "/n"
            log_file.write("  --- idcode:   , "+idcode +'\n')
            log_file.write("  --- code  :  ,  "+code+ '\n  \n \n')

            if reporting == 'PS4':
                    try:
                            statut = 'VALIDE'
                            if(code == 'A040'):

                                    code=''
                                    code='H090'

                            if(code == 'D010'):

                                    code=''
                                    code='D090'


                            if nextJob == 'Reception':
                                    db_2=MySQLdb.connect(HostIp,User,Password,DataBaseName,connect_timeout=4)#CONNECT TO SERVER
                                    cursor_2=db_2.cursor()
                                    cursor_2.execute("INSERT INTO ps3suivi.sn_mvt (idsn, sn,snOld,mvt,statut,dtmvt,nextJob, uid,ip,host,version,position)VALUES(%s,%s,%s,%s,%s,NOW(), %s, 'UserId', '10.10.10.10', %s,%s,'QUickTester')",( idsn, sn,snOld,'Reception',statut,'PreDiag',host,version))	                            
                                    db_2.commit()
                                    
                            
                            nextJob='Dismount'
                            mvt='PreDiag'
                            db_2=MySQLdb.connect(HostIp,User,Password,DataBaseName,connect_timeout=4)#CONNECT TO SERVER
                            cursor_2=db_2.cursor()
                            cursor_2.execute("UPDATE ps3suivi.sn  SET mcbstatut= %s ,mvt = %s, dtmvt =now() , idcode=%s,code = %s,nextJob= %s,position=%s,snPalette_in=%s,mvt_in=%s,nextJob_in=%s  WHERE sn.idsn=%s",(mcbstatut,mvt,idcode,code,nextJob,'Kram_Atel',None,None,None,idsn))

                            db_2.commit()

                            
                            
                            cursor_2.execute("INSERT INTO ps3suivi.sn_mvt (idsn, sn,snOld,mvt,statut,mcbstatut,dtmvt,nextJob, uid,ip,host,version,position)VALUES(%s,%s,%s,%s,%s,%s,NOW(), %s, 'UserId', '10.10.10.10', %s,%s,'QUickTester')",( idsn, sn,snOld,mvt,statut,mcbstatut,nextJob,host,version))	                                                                        
                            db_2.commit()

                            cursor_2.execute("SELECT idmvt FROM sn_mvt WHERE (snOld = %s ) order by idmvt desc limit 1",[Real_sn_consol])
                            idmvt= cursor_2.fetchone()
                            print "id mvt :::::::::::::  ", idmvt        
                            db_2.commit()

                            cursor_2.execute("INSERT INTO ps3suivi.cl_mvt_code(idsn, idmvt, type, sn, code, mvt, dtmvt, user) VALUES (%s , %s, 'CL', %s , %s, %s, NOW(), %s)",(idsn , idmvt, sn , idcode , mvt, host))
                            db_2.commit()
                            
                            print "         INSERT   db  OKK  /n  "
                            log_file.write("INSERT   db  OKK  /n  ")
                            log_file_R = open(filename, 'r') 
                            db_log_file =log_file_R.read()
                            print db_log_file
                            cursor_2.execute("INSERT INTO ps3suivi.desc (id, idmvt, mvt, CL_BD_MCB, serial, dtmvt, user, `desc`, statut ) VALUES (%s,%s,'PreDiag','CL',%s, NOW(),%s, %s, 'SY')",(idsn,idmvt,sn,host,db_log_file))
                            db_2.commit()

                            cursor_2.execute("SELECT sn.idsn, sn.sn,sn.snOld,sn.mvt,sn.statut,sn.Model,sn.ModelNumber,sn.Colour,sn.nextJob,snpalette_in,mvt_in FROM ps3suivi.sn sn WHERE (sn.snOld = %s)",[Real_sn_consol])
                            snInfo= cursor_2.fetchone()
                            print snInfo

                            nextJob=snInfo[8]
                            if nextJob=='Dismount':
                                    print "======>>>>   INSERT OK  "
                                    lcd_i2c.lcd_string("Insert au bd ok",lcd_i2c.LCD_LINE_2)
                                    sleep(1)
                            else:
                                    print "======>>>>   INSERT NNNNNNNOK  "
                                    lcd_i2c.lcd_string("ERROR INSERT db",lcd_i2c.LCD_LINE_2)
                                    sleep(1)  
                            log_file_R.close()
                    except:
                            print "======>>>>   Conx db Error   "
                            lcd_i2c.lcd_string("Conx db Error",lcd_i2c.LCD_LINE_2)
                            sleep(1)  

            elif reporting =='PS5':

                    if code in ['A020','A010']:
                            QuickAuto=code #29/01/2021
                    print "Insert db"
                    if (code == 'N000'):
                    #if (code == 'N000' or code == 'A040' or code == 'H090'):
                            ret = '1' 
                    else:
                            ret = '2'

                    if(code == 'H090'):
                            code=''
                            code='A040'

                    if(code == 'D090'):
                            code=''
                            code='D010'


                    
                    db=MySQLdb.connect(HostIp1,User1,Password1,DataBaseName1,connect_timeout=4)#CONNECT TO SERVER
                    cursor=db.cursor()

                    cursor.execute("SELECT code, id_code, panne_tech.Panne FROM panne_tech LEFT JOIN symptom_code ON panne_tech.id_panne = symptom_code.id_Panne WHERE Code = %s AND symptom_code.id_host = 3",[code])
                    codeInfo= cursor.fetchone()
                    code1=codeInfo[0]
                    id_code=codeInfo[1]
                    panne=codeInfo[2]    
                    db.commit()        

                    if nextJob == 'Reception':
                        if ret == '1':
                            cursor.execute("update ps5suivi.sn set  id_mcbstatut=%s, id_movement= 16,id_nextjob= 3 ,dtmvt=NOW(), id_code=%s  where  id_sn=%s",(ret,id_code,id_sn))
                            db.commit()  

                            cursor.execute("INSERT INTO ps5suivi.sn_mvt ( id_sn,  snold , id_movement , id_statut , dtmvt, id_nexthost, ip, host )  VALUES (%s,%s, 2, 1 ,NOW(),16,NULL,%s)",(id_sn,[sn_Old],host))
                            db.commit()
                        
                            cursor.execute("INSERT INTO ps5suivi.sn_mvt ( id_sn,  snold , id_movement , id_statut , dtmvt, id_nexthost, ip, host )  VALUES (%s,%s, 16, 1 ,NOW(),3,NULL,%s)",(id_sn,[sn_Old],host))
                            db.commit()
                        else:
                            cursor.execute("update ps5suivi.sn set  id_mcbstatut=%s, id_movement= 16,id_nextjob= 4 ,dtmvt=NOW(), id_code=%s  where  id_sn=%s",(ret,id_code,id_sn))
                            db.commit()

                            cursor.execute("INSERT INTO ps5suivi.sn_mvt ( id_sn,  snold , id_movement , id_statut , dtmvt, id_nexthost, ip, host )  VALUES (%s,%s, 2, 1 ,NOW(),16,NULL,%s)",(id_sn,[sn_Old],host))
                            db.commit()
                        
                            cursor.execute("INSERT INTO ps5suivi.sn_mvt ( id_sn,  snold , id_movement , id_statut , dtmvt, id_nexthost, ip, host )  VALUES (%s,%s, 16, 1 ,NOW(),4,NULL,%s)",(id_sn,[sn_Old],host))
                            db.commit()
                    else:

                        if ret == '1':
                            cursor.execute("update ps5suivi.sn set  id_mcbstatut=%s, id_movement= 16,id_nextjob= 3 ,dtmvt=NOW(), id_code=%s  where  id_sn=%s",(ret,id_code,id_sn))
                            db.commit()    

                            cursor.execute("INSERT INTO ps5suivi.sn_mvt ( id_sn,  snold , id_movement , id_statut , dtmvt, id_nexthost, ip, host )  VALUES (%s,%s, 16, 1 ,NOW(),3,NULL,%s)",(id_sn,[sn_Old],host))
                            db.commit()
                        else:
                            cursor.execute("update ps5suivi.sn set  id_mcbstatut=%s, id_movement= 16,id_nextjob= 4 ,dtmvt=NOW(), id_code=%s  where  id_sn=%s",(ret,id_code,id_sn))
                            db.commit()    

                            cursor.execute("INSERT INTO ps5suivi.sn_mvt ( id_sn,  snold , id_movement , id_statut , dtmvt, id_nexthost, ip, host )  VALUES (%s,%s, 16, 1 ,NOW(),4,NULL,%s)",(id_sn,[sn_Old],host))
                            db.commit()

                    cursor.execute("SELECT id_snmvt from sn_mvt where snold=%s order by id_snmvt desc limit 1",[sn_Old])
                    id_mvt= cursor.fetchone()
                    db.commit()


                    cursor.execute("INSERT INTO ps5suivi.cl_mvt_code ( idmvt,  idcode ) VALUES (%s,%s)",(id_mvt,id_code))
                    db.commit()


                    cursor.execute("INSERT INTO ps5suivi.sn_desc ( idmvt,  `desc`  )   VALUES (%s,%s)",(id_mvt,panne))
                    db.commit()
                                
                    db_2=MySQLdb.connect(HostIp,User,Password,DataBaseName,connect_timeout=4)#CONNECT TO SERVER
                    cursor_2=db_2.cursor()

                    db=MySQLdb.connect(HostIp1,User1,Password1,DataBaseName1,connect_timeout=4)#CONNECT TO SERVER
                    cursor=db.cursor()
                    cursor.execute("SELECT id_sn, sn,snold,(SELECT cl_movement.Mvt FROM  cl_movement WHERE  cl_movement.id_mvt = sn.id_movement)AS Mvt,cl_statut.Statut,(SELECT cl_movement.Mvt FROM cl_movement WHERE cl_movement.id_mvt = sn.id_nextjob) AS NextJob,cl_model_console.model FROM sn LEFT JOIN cl_statut ON sn.id_statut = cl_statut.id_statut LEFT JOIN cl_model_console ON sn.id_model = cl_model_console.id_model_consol WHERE snold=%s",[sn_Old])
                    snInfo= cursor.fetchone()
                    print snInfo
                    nextJob=snInfo[5]
                    db.commit()
                    if nextJob=='PreDiag':
                            print "======>>>>   INSERT OK  "
                            lcd_i2c.lcd_string("Insert au bd ok",lcd_i2c.LCD_LINE_2)
                            sleep(1)
                    else:
                            print "======>>>>   INSERT NNNNNNNOK  "
                            lcd_i2c.lcd_string("ERROR INSERT db",lcd_i2c.LCD_LINE_2)
                            sleep(1)  
                    #_________________________________
                    log_file_R = open(filename, 'r')
                    db_log_file =log_file_R.read()
                    print db_log_file
                    log_file_R.close()
                    #_________________________________
            
            sn_consol = "Consol"
            idsym=''
            start_Test=True
            dbHDDButton=0
            dbCEButton=0
            dbAffButton=0
            dbOKButton=0
            dbPowerOff=0
            dbCEBButton=0
            
            log_file.write('\n \n  ------------------------------------------------------------------------------------------ \n')
            log_file.close()

            #___________________________ 29/01/2021
            QuickAuto=''
            reporting=''
                
            
            
            #___________________________
            
        elif not GPIO.input(HDMI_GND) and not start_Test:
            print "---consol in tester"
            #______________________________________________________
            lcd_i2c.lcd_string("CheckConsolState",lcd_i2c.LCD_LINE_2)
            sleep(1.5)
            lcd_i2c.lcd_string("",lcd_i2c.LCD_LINE_2)
            sleep(0.5)   
            #______________________________________________________   
        else:
            print '......................   ...................... \n'
            print'.......   CEC',GPIO.input(CEC_HDMI)
            
            print'.......   5V',GPIO.input(HDMI_5V)

            print '.......   USB',GPIO.input(USB_5V)
        
            print '.......   USB GND',GPIO.input(HDMI_GND)
          
            print '.......   DS4',__DS4__.powerDetect()
          

            sleep(1)

            
            

        


