import sys
import time
import json, csv
import paho.mqtt.client as mqtt
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))




# MQTT parameters
org='????????' # org id
host= org + '.messaging.internetofthings.ibmcloud.com'
clientid='d:'+ org +':TempSensor:Device01'
username='????????'
password='????????' # Replace this with the device token 
topic = "iot-2/evt/temperature/fmt/json"
#Defaults to {mqttDevice.topic.prefix}id/{mqttDevice.id}/evt/{EVENTID}/fmt/json
#The pattern must include {EVENTID} and must end with "/fmt/json"

client = mqtt.Client(clientid)
client.username_pw_set(username, password)
#client.on_connect = on_connect
#client.on_message = on_message
client.connect(host, 1883 , 60)

csvFilePath=r'datasensors.csv'

with open(csvFilePath, mode='r') as csvFile:
	csv_reader = csv.reader(csvFile, delimiter=',')
	for csvRow in csv_reader:
		client.publish(topic,json.dumps({"temp": str(csvRow)}))
		print(csvRow)
		time.sleep(1)
#		client.loop_forever()
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.