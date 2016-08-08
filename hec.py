# Demo Python Class for HTTP Event Collector of Splunk Enterprise 6.4.x
# Version 0.9.01
# Support JSON, RAW data inputs and Indexer acknowledgment
# Reference: http://docs.splunk.com/Documentation/Splunk/6.4.2/Data/UsetheHTTPEventCollector
# Disclaimer: This is not a official Splunk solution and with no liability. Use at your own risk.
# For feedback and bug report, please send to jyung@splunk.com

import time
import urllib2, urllib, httplib
import json
import ssl
import socket
import logging

class hec(object):

    def __init__(self, indexer, port, token):
        self.indexer = indexer
        self.port = port
        self.token = token
        self.host = socket.gethostname()
        self.guid = "666a7b4b-a5b5-42b0-bf0f-3c86fa0a1b85"
        self.http = "http"

    def __submit(self, eventData):
        try:
            req=urllib2.Request(self.url,data=eventData,headers={'Authorization':'Splunk %s' %self.token,'X-Splunk-Request-Channel':'%s' %self.guid})
            if self.http == "https":
                dcontext = ssl.create_default_context()
                dcontext.check_hostname = False
                dcontext.verify_mode = ssl.CERT_NONE
                resp=urllib2.urlopen(req,context=dcontext).read()
            else:
                resp=urllib2.urlopen(req).read()
            try:
                respJ = json.loads(resp);
                return True, respJ["ackId"]
            except KeyError, e:
                return True, -1
        except urllib2.HTTPError, e:
            logging.error(str(int(time.time())) + ' HTTPError = ' + str(e.code))
            return False, -1
        except urllib2.URLError, e:
            logging.error(str(int(time.time())) + ' URLError = ' + str(e.reason))
            return False, -1
        except httplib.HTTPException, e:
            logging.error(str(int(time.time())) + ' HTTPException')
            return False, -1
        except Exception:
            import traceback
            logging.error(str(int(time.time())) + ' Generic exception: ' + traceback.format_exc())
            return False, -1

    def __queryAck(self, ackId):
        urlAck = self.http+"://"+self.indexer+":"+self.port+"/services/collector/ack?channel="+self.guid
        try:
            req=urllib2.Request(urlAck,data=json.dumps(ackId),headers={'Authorization':'Splunk %s' %self.token,'X-Splunk-Request-Channel':'%s' %self.guid,'Content-Type':'application/json'})
            if self.http == "https":
                dcontext = ssl.create_default_context()
                dcontext.check_hostname = False
                dcontext.verify_mode = ssl.CERT_NONE
                resp=urllib2.urlopen(req,context=dcontext).read()
            else:
                resp=urllib2.urlopen(req).read()
            return True, resp
        except urllib2.HTTPError, e:
            logging.error(str(int(time.time())) + ' HTTPError = ' + str(e.code))
            return False, -1
        except urllib2.URLError, e:
            logging.error(str(int(time.time())) + ' URLError = ' + str(e.reason))
            return False, -1
        except httplib.HTTPException, e:
            logging.error(str(int(time.time())) + ' HTTPException')
            return False, -1
        except Exception:
            import traceback
            logging.error(str(int(time.time())) + ' Generic exception: ' + traceback.format_exc())
            return False, -1

    def setIndexer(self, indexer):
        self.indexer = indexer

    def setIndexerPort(self, port):
        self.port = port

    def setToken(self, token):
        self.token = token

    def setHost(self, host):
        self.host = host

    def setGUID(self, guid):
        self.guid = guid

    def setHTTPS(self, enabled):
        if enabled == True:
            self.http = "https"
        else:
            self.http = "http"

    def queryAck(self, ackId):
        return self.__queryAck(ackId)

class hecJson(hec):
    def __init__(self, indexer, port, token):
        hec.__init__(self, indexer, port, token)

    def submit(self, sourcetype, source, eventData):
        self.url = self.http+"://"+self.indexer+":"+self.port+"/services/collector"
        event={}
        event["time"]=int(time.time())
        event["host"]=self.host
        event["source"]=source
        event["sourcetype"]=sourcetype
        event["event"]=eventData
        return super(hecJson,self)._hec__submit(json.dumps(event))

class hecRaw(hec):

    def __init__(self, indexer, port, token):
        hec.__init__(self, indexer, port, token)

    def submit(self, eventData):
        self.url = self.http+"://"+self.indexer+":"+self.port+"/services/collector/raw"
        return super(hecRaw,self)._hec__submit(str(int(time.time()))+" "+eventData)
