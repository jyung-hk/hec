# Demo Python Class for HTTP Event Collector of Splunk Enterprise 6.4.x
- Support JSON, RAW data inputs and Indexer acknowledgment
- Reference: http://docs.splunk.com/Documentation/Splunk/6.4.2/Data/UsetheHTTPEventCollector
- Disclaimer: This is not an official Splunk solution and with no liability. Use at your own risk.
- For feedback and bug report, please send to jyung@splunk.com


# Usage
**First step**. Import the Class
```python
  import hec
```

**Option 1**. JSON Data payload
```python
  hec.hecJson(String: indexer ip address,String: port,String: token)
  hec.submit(String: sourcetype,String: source,Json: event)
```
e.g.
```python
  myHEC = hec.hecJson("192.168.10.8","8088","75475867-EE4F-4357-BBA3-03F1D66F3697")
  myHEC.submit("10dof","sensorData.py",eventData)
```

**Option 2**. RAW Data payload
```python
  hec.hecRaw(String: index ip address,String: port,String: token)
  hec.submit(String: raw event)
```
e.g.
```python
  myHEC = hec.hecRaw("192.168.10.8","8088","75475867-EE4F-4357-BBA3-03F1D66F3697")
  myHec.submit("Raw event data example")
````

**Optional Indexer Acknowledgment**: support both hecRaw and hecJson
```python
  resp, ackId = myHEC.submit("10dof","sensorData.py",eventData)
```
- resp: True/False of the transfer
- ackId: -1 indicates Indexer Acknowledgment is disabled on the indexer. Number > 0 is the acknowledgment number of the transfer

To query if the payload of a specific acknowledgment number is indexed
```python
  respRack = myHEC.queryAck(ackEvent)
```
- ackEvent: a json object containing an array of acknowledgment number
- respRack: a json object containing the result of the acknowledgment number status

For details, please refer to [Splunk Documentation](http://dev.splunk.com/view/event-collector/SP-CAAAE8X)

* *Note: Event timestamp is the time when the event is submitted, not the time it is received by Indexer.*

**Other supporting methods**
```python
  setHTTPS(Boolean: True/False)  
```
* *Note: it should match the server-side setting, certification verification is disabled.*
```python
  setIndexer(String: indexer ip address)
```

```python
  setIndexerPort(String: indexer port)
```

```python
  setGUID(String: guid)
```
* *Note: the class come with a fixed, default GUID. It's recommended to assign new GUID for a dedicated data channel*
```python
  setHost(String: Value of the meta field 'host')
```
* *Note: default is the hostname of the socket*
```python
  setToken(String: Token of the HEC channel)
```
