#!/usr/bin/env python
#coding:utf-8
"""
  Author:  lianjun.yao --<>
  Purpose: 
  Created: 2016/5/26
"""

import telnetlib,logging
logger_telnet = logging.getLogger('main.telnet')

########################################################################
class telnet(object):
    
    def __init__(self, host, usr, psw):
        self.host = host
        self.usr = str(usr)
        self.psw = str(psw)
        self.tn = telnetlib.Telnet()
        self.connected = False
        
    def telnet_connect(self, debuglevel = 0):
        try:
            print "read to login:",self.usr,self.psw
            self.tn.set_debuglevel(debuglevel) #Set debug level, it can recv info from remote machine.
            self.tn.open(self.host)
            self.tn.read_until('login:')
            self.tn.write(self.usr + '\n')
            self.tn.read_until('Password:')
            self.tn.write(self.psw + '\n')
            self.readuntil('>')
            logger_telnet.info('Login done!')
            self.connected = True
            return True
        except Exception as e:
            logger_telnet.error('Maybe your username or password is incorrect %s'%e)
            return  False
            
    
    #must use this method to check return value, if you dont do this...
    #the cmd line will not work!
    def readuntil(self, con, to = None):
        return self.tn.read_until(con, to)
    
    def readsome(self):
        '''This method must excute after every cmd method.
        telnet must read sth. otherwise the next cmd will not excute.'''
        return self.tn.read_some()
        
    def cmd(self, cmd):
        '''input cmd : the cmd line remote machine will excute.'''
        ret = ''
        try:
            self.tn.write(cmd + '\n')
            logger_telnet.info(cmd)
            if "copy" in cmd:
                a =  self.readuntil('file(s).',20)
                self.readuntil('>.',1)
            else:
                a = self.readuntil('>',10)

            logger_telnet.info("return :%s"%a)
            #print "TIME OUT:  ",self.readsome()
            #ret =  self.tn.read_some()
        except Exception,e:
            logger_telnet.error('Failed to commit: %s'%cmd)
            logger_telnet.error(str(e))
            
        return ret
    
    def mkDir(self,pathname):
        cmd =  'mkdir %s'%pathname
        self.cmd(cmd)

    #复制文件夹
    def copyFiles(self,souseDir,targetDir):
        cd = r"cd %s"%targetDir
        ret = self.cmd(cd)
        if 'not found' in ret:
            self.mkDir(targetDir)
        else:
            self.cmd('cd \\')
        cmd = r'copy %s\\*.* %s'%(souseDir,targetDir)
        self.cmd(cmd)

    #复制单文件
    def copyFile(self,souseFile,targetDir):
        cmd = r'copy %s %s'%(souseFile,targetDir)
        self.cmd(cmd)


    def delFiles(self,pathName):
        cmd =  'RMDIR /S /Q %s'%pathName
        logger_telnet.info(cmd)
        self.cmd(cmd)



    def movePath(self,pathName,targetPath):
        cmd = 'move %s %s'%(pathName,targetPath)
        self.cmd(cmd)
        return True


    def close(self):
        self.tn.close()
        self.connected = False

        
    def __del__(self):
        #self.tn.read_until(finish)

        print('Disconnect telnet')
        try:
            if self.tn != None:
                if self.connected == True:
                    self.tn.close()
                self.tn = None
        except Exception,e:
            logger_telnet.exception(str(e))
    
    

if __name__ == '__main__':
    tel = telnet('172.16.43.169','guest','1')
    tel.telnet_connect()
    #tel.cmd('copy "Hard Disk"\\CplusApplication\\*.* "Hard Disk2"\\Data\\bootbackup\\CplusApplication')
    souseDir = '"Hard Disk"\\Boot'
    targe = ' "Hard Disk2"\\Data\\bootbackup\Boot'
    tel.delFiles(targe)

