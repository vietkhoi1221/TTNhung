#!/usr/bin/python
import Adafruit_DHT
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import random
import lcd
from time import sleep

ten_cam_bien = Adafruit_DHT.DHT11
pin_sensor = 25 
GPIO.setmode(GPIO.BCM) # chon kieu danh so chan GPIO la BCM
#lcd.lcd_init() 
def on_connect(mqttc, obj, flags, rc):
    pass
 
def on_message(mqttc, obj, msg): 
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

 
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
mqttc.connect("192.168.0.107", 1883, 60) #dien IP cua Pi, vd: 192.168.1.77
mqttc.subscribe("khoi/demo/app", 0)
mqttc.loop_start()
while True:
    humid, temp= Adafruit_DHT.read_retry(ten_cam_bien, pin_sensor)
    dong_1 = "Nhiet do:" + str(temp) 
    dong_2 = "Do am:" + str(humid) +"%"
    #lcd.lcd_string(dong_1,0x80)
    #lcd.lcd_byte(0xDF,0)
    #lcd.lcd_string(dong_2,0xC0)
    data_sensor= str(temp) + "," + str(humid)
    publish.single('khoi/demo/data', data_sensor, hostname="192.168.0.107")
    sleep(1)
