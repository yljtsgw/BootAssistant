# -*- coding: gbk -*-
import ConfigParser,re

cf = ConfigParser.ConfigParser()
configFile = 'config.ini'



def getTemp(option):
    data = ''
    try:
        cf.read(configFile)
        data = cf.get('TEMP', option)
        data = unicode(data,'gbk')
    except:
        data = ''
    return data

def saveTemp(option,value):
    cf.read(configFile)
    section = 'TEMP'
    try:
        cf.set(section, option,unicode(value).encode('gbk'))
        cf.write(open(configFile,'w')) 
    except Exception,e:
        print e

def getConfig(option):
    data = ''
    try:
        cf.read(configFile)
        data = cf.get('CONFIG', option)
        data = unicode(data,'gbk')
    except:
        data = ''
    return data    

GETFILENAME = getConfig('downloadPathName')
USER = getConfig('user')
PSW = getConfig('password')
TARGETDIR = str(getConfig('targetdir'))
TEMPDIR = str(getConfig('tempdir'))
BACKUPDIR = str(getConfig('backupDir'))
ROOTDIR = str(getConfig('rootDir'))
UPDATEDIR = str(getConfig('updateDir'))
TEMPBDIR = str(getConfig('tempbdir'))

#功能常量
CON_PING = 0
CON_DOWNLOAD = 1
CON_UPLOAD = 2
CON_UPDATE = 3
CON_RESTARTPLC = 4
CON_KILLCERHOST = 5
CON_CLEANDISK2 = 6
CON_MOTIFY = 7
