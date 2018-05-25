#!/usr/bin/python
import Adafruit_DHT
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import random
import lcd
from time import sleep

ten_cam_bien = Adafruit_DHT.DHT11
pir = 23
led = 22
pin_sensor = 25
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # chon kieu danh so chan GPIO la BCM
GPIO.setup(pir, GPIO.IN)#khai bao chan pir la input
GPIO.setup(led, GPIO.OUT) 
lcd.lcd_init()
i = ''
def on_connect(mqttc, obj, flags, rc):
    pass
 
def on_message(mqttc, obj, msg):
    global i
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    i = str(msg.payload.decode())
    print(i)
    
        
 
def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))
 
def on_subscribe(mqttc, obj, mid, granted_qos):
    pass
 
def on_log(mqttc, obj, level, string):
    pass
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.connect("192.168.43.6", 1883, 60) #dien IP cua Pi, vd: 192.168.1.77
mqttc.subscribe("khoi/demo/app", 0)
mqttc.loop_start()
while True:
    humid, temp= Adafruit_DHT.read_retry(ten_cam_bien, pin_sensor)
    detect = 'NO'
    if GPIO.input(pir):                            #Check whether pir is HIGH
        detect = 'YES'
        print ("DETECTED")
    if (i == 'LAMPON'):
         GPIO.output(led, 1)
         print('led on')
    if (i == 'LAMPOFF'):
         GPIO.output(led, 0)
         print('led offf')
    dong_1 = "Nhiet do:" + str(temp) 
    dong_2 = "Do am:" + str(humid) +"%"
    lcd.lcd_string(dong_1,0x80)
    lcd.lcd_string(dong_2,0xC0)
    data_sensor= str(temp) + "," + str(humid) + "," + detect
    publish.single('khoi/demo/data', data_sensor, hostname="192.168.43.6")
    sleep(1)
