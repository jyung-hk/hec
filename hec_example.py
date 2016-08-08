# Two examples of Json and RAW data ingestion
# HTTPS of HTTP Event Collector is disabled

import time
import os
import hec

myHEC = hec.hecJson("192.168.10.8","8089","75475867-EE4F-4357-BBA3-03F1D66F3697")
fanId = 1    # dummy sensor data
rpm1 = 3000  # dummy sensor data
eventData = {}
eventData["id"]="hk:splunk:fan"+str(fanId)
eventData["rpm"]=rpm1
myHEC.setIndexerPort("8088")
myHEC.setGUID("666a7b4b-a5b5-42b1-bf0f-3c86fa0a1b85")
resp, ackId = myHEC.submit("fan:pwm",os.path.basename(__file__),eventData)
if resp == True:
    print "Successfully submitted"
    if ackId != -1:
        ackIds = []
        ackIds.append(ackId)
        ackEvent = {}
        ackEvent["acks"]=ackIds
        time.sleep(2)
        respRack = myHEC.queryAck(ackEvent)
        print respRack
elif resp == False:
    print "Failed"

rawEvent = str(int(time.time()))+" Testing Raw Event"
myRawHEC = hec.hecRaw("192.168.10.7","8089","75475867-EE4F-4357-BBA3-03F1D66F3697")
myRawHEC.setIndexer("192.168.10.8")
myRawHEC.setIndexerPort("8088")
resp, ackId = myRawHEC.submit(rawEvent)
if resp == True:
    print "Successfully submitted"
    if ackId != -1:
        ackIds = []
        ackIds.append(ackId)
        ackEvent = {}
        ackEvent["acks"]=ackIds
        time.sleep(2)
        respRack = myRawHEC.queryAck(ackEvent)
        print respRack
elif resp == False:
    print "Failed"
