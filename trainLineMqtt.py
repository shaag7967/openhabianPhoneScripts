'''
Created on 21.11.2017

@author: seven
'''

#!/usr/bin/python
import sys
import paho.mqtt.client as mqtt
import requests
from bs4 import BeautifulSoup


mqttServer = "phone"
mqttTopic = "train/{0:s}/countdown"
mqttUserId = "openhabian"
mqttPassword = "7017slg"



def createUrl(stationId):
    url = 'http://www2.vvs.de/vvs/widget/XML_DM_REQUEST?'
    url += '&stateless=%d' % 1
    url += '&language=%s' % 'de'
    url += '&limit=%d' % 10
    url += '&depArr=%s' % 'dep'
    url += '&type_dm=%s' % 'any'
    url += '&anyObjFilter_dm=%d' % 2
    url += '&deleteAssignedStops=%d' % 1
    url += '&name_dm=%s' % stationId
    url += '&mode=%s' % 'direct'
    url += '&dmLineSelectionAll=%d' % 1
    url += '&useRealtime=%d' % 1

    return url

def main():
    url = createUrl(5000080)
#     print url
    content = requests.get(url).content
#     print content
    
    soup = BeautifulSoup(content)
#     print soup.prettify()
    
    depList = soup.find_all('itddeparture')
    
#     print len(depList)

    countdowns = {}
    # find next trains
    for dep in depList:
        if dep.itdservingline.motdivaparams['direction'] == 'H':
            lineName = dep.itdservingline['symbol']
            
            if countdowns.has_key(lineName):
                if int(countdowns[lineName]) > int(dep['countdown']):
                    countdowns[lineName] = dep['countdown']
            else:
                countdowns[lineName] = dep['countdown']

#     print countdowns
    
    
    mqttc = mqtt.Client()
    mqttc.username_pw_set(mqttUserId, mqttPassword)
    mqttc.connect(mqttServer, 1883)
    mqttc.loop_start()

    for line in countdowns:
        print line,countdowns[line]
        mqttc.publish(mqttTopic.format(line), countdowns[line])
        
    mqttc.loop_stop()
    mqttc.disconnect()
  
  
if __name__ == '__main__':
    main()
    sys.exit(0)
    
    



