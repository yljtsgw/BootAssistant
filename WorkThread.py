#!/usr/bin/env python
# coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2016/5/26
"""

from telnet import telnet
from ftp import ftpTool
from PyQt4.QtCore import QThread, pyqtSignal
import os
import config

import logging

logger_working = logging.getLogger('main.working')


########################################################################
class workThread(QThread):
    """下载线程"""
    sinOut1 = pyqtSignal(str)
    sinOut2 = pyqtSignal(int)
    # ----------------------------------------------------------------------
    def __init__(self, parent=None):
        """输入对应IP 用户名及密码"""
        super(workThread, self).__init__(parent)
        self.funcType = 1
        self.lock = False
        self.tel = None
        self.ftp = None

    def setup(self, host, usr, psw):
        self.ftp = ftpTool(host, usr, psw)
        self.tel = telnet(host, usr, psw)

    def downloadFiles(self, remotedir, localdir):
        if self.lock:
            self.sinOut1.emit(u'有未完成任务正在进行，请稍后...' )
            return
        self.localdir = localdir
        self.remotedir = remotedir
        self.funcType = config.CON_DOWNLOAD
        self.lock = True
        self.start()
        
    def uploadFiles(self,localdir,backupEnable):
        self.backupEnable = backupEnable
        if self.lock:
            self.sinOut1.emit(u'有未完成任务正在进行，请稍后...' )
            return        
        self.localdir = localdir
        self.funcType = config.CON_UPLOAD
        self.lock = True
        self.start()
        #self.run()

    def updatePlc(self,parambackupDelete):
        if self.lock:
            self.sinOut1.emit(u'有未完成任务正在进行，请稍后...' )
            return
        self.parambackupDelete = parambackupDelete
        self.funcType = config.CON_UPDATE
        self.lock = True
        self.start()        

    def restartPlc(self):
        if self.lock:
            self.sinOut1.emit(u'有未完成任务正在进行，请稍后...' )
            return
        self.funcType = config.CON_RESTARTPLC
        self.lock = True
        self.start()

    def cleanData(self):
        print "print self.lock:", self.lock
        if self.lock:
            self.sinOut1.emit(u'有未完成任务正在进行，请稍后...' )
            return
        self.funcType = config.CON_CLEANDISK2
        self.lock = True
        self.start()
        #self.run()
    
    def run(self):
        try:
            if self.funcType == config.CON_DOWNLOAD:
                self.download()
            elif self.funcType == config.CON_UPLOAD:
                self.upload()
            elif self.funcType == config.CON_UPDATE:
                self.update()
            elif self.funcType == config.CON_RESTARTPLC:
                cmd = 'cxsuspend'
                self.sinOut1.emit(u'下发重启命令...' )
                self.runTelnetCmd(cmd)
                self.sinOut1.emit(u'已下发重启命令，请等待PLC重启...' )
            elif self.funcType == config.CON_KILLCERHOST:
                pass
            elif self.funcType == config.CON_CLEANDISK2:
                self.clean()

        except Exception,e:
            logger_working.exception(str(e))
        finally:
            self.lock = False
            self.sinOut2.emit(self.funcType)
            
            
    def runTelnetCmd(self,cmd):
        if self.telnetConnect():
            self.tel.cmd(cmd)


    def clean(self):
        try:
            ret =  self.ftpConnect()
            if not  ret:
                return False
            nlist = ['celogger_data','SC','StatusCode','Tracelog']
            filelist = self.ftp.nlst()
            print filelist
            for files in nlist:
                logger_working.info("file: %s"%files)
                if files in filelist:
                    logger_working.info("%s in  %s"%(files,str(filelist)))
                    self.sinOut1.emit(u'正在删除%s..'%files )
                    self.ftp.clearDir(files)
                else:
                    self.sinOut1.emit(u'正在重新创建%s..'%files )
                    self.ftp.mkd(files)
            self.sinOut1.emit(u'清理Hard Disk2完成' )
        except Exception,e:
            logger_working.exception(str(e))

    def download(self):
        try:
            # telnet 将boot里的文件移至bootrm
            ret =   self.telnetConnect()
            if not  ret:
                return False
            self.sinOut1.emit(u'在目标机删除临时目录下的文件')
            self.tel.delFiles(config.TEMPDIR)
            self.sinOut1.emit(u'在目标机创建临时目录')
            self.tel.mkDir(config.TEMPDIR)

            self.sinOut1.emit(u'将%s复制至%s' % (config.TARGETDIR, config.TEMPDIR))
            self.tel.copyFiles(config.TARGETDIR, config.TEMPDIR)

            if not self.ftpConnect():
                return
            # self.ftp.cwd(self.remotedir)
            # self.sinOut1.emit(u'转到目录: %s' % self.remotedir)
            remotedir = os.path.split(self.remotedir)[1]
            localdir = os.path.join(self.localdir, remotedir)
            if not os.path.isdir(localdir):
                self.sinOut1.emit(u'创建本地路径: %s' % localdir)
                os.makedirs(localdir)
            remotenames = self.ftp.getfileList(self.remotedir)
            self.sinOut1.emit(u'获取目标机文件列表')
            for item in remotenames:
                filesize = int(item[0])
                filename = item[1]
                local = os.path.join(localdir, filename)
                local = local.replace('\\', '/')
                self.sinOut1.emit(u'>>>>正在下载文件:%s ....' % filename)
                ret = self.ftp.download_file(local, filename, filesize)
                if len(ret) > 0 :
                    self.sinOut1.emit(ret)
                self.sinOut1.emit(u'%s 下载完成' % (filename))
            self.sinOut1.emit(u'全部文件下载完成，下载至:\n%s' % (localdir))
            self.ftp.cwd('..')
        except Exception, e:            
            logger_working.exception(str(e))
        finally:

            self.lock = False


    def upload(self):
        try:
            bootlist = ['Boot','CplusApplication','EventAnalyze','Parameter','Parameter_backup','ReportApplication']

            if not self.telnetConnect():
                return
            if self.backupEnable:
                self.sinOut1.emit(u'在目标机删除备份目录下的文件')
                self.tel.delFiles(config.BACKUPDIR)
        
                self.sinOut1.emit(u'在目标机创建备份目录')
                self.tel.mkDir(config.BACKUPDIR)
                self.tel.delFiles(config.BACKUPDIR)
                for filename in bootlist:
                    self.sinOut1.emit(u'在目标机创建备份目录%s文件夹'%filename)
                    tfilename = '%s\\\\%s'%(config.BACKUPDIR,filename)
                    print tfilename
                    self.tel.mkDir(tfilename)
                    sfilename = r'%s\\%s'%(config.ROOTDIR,filename)
                    self.sinOut1.emit(u'将%s复制至%s'%(sfilename,tfilename) )
                    self.tel.copyFiles(sfilename, tfilename)

            self.tel.delFiles(config.UPDATEDIR)
            self.tel.mkDir(config.UPDATEDIR)
            self.sinOut1.emit(u'在目标机创建升级目录')
            updateDir = os.path.split(config.UPDATEDIR)[1]
            #self.ftp.cwd(updateDir)
            #self.sinOut1.emit(u'转到目录: %s'%updateDir)
            self.sinOut1.emit(u'正在上传本地文件夹：%s'%self.localdir)
            if not self.ftpConnect():
                return
            self.uploadDir(self.localdir,updateDir)
            self.sinOut1.emit(u'全部文件上传完成，上传至%s'%(updateDir))

        except Exception ,e:
            logger_working.exception(str(e))
        finally:
            self.lock = False
            return

    def uploadDir(self,localdir,remotedir):
        try:
            if not os.path.isdir(localdir):
                return
            self.ftp.cwd(remotedir)
            for file in os.listdir(localdir):
                src = os.path.join(localdir, file)
                if os.path.isfile(src):
                    #file = unicode(file,'gbk')
                    logger_working.info(u'>>>>>>>正在上传文件:%s ...'%file)
                    self.ftp.uploadFile(src, file)
                elif os.path.isdir(src):
                    try:
                        self.sinOut1.emit(u'>>>>正在上传文件夹:%s ....' % file)
                        self.ftp.mkd(file)
                    except:
                        logger_working.info('the dir is exists %s' % file)

                    self.uploadDir(src, file)

            logger_working.info( 'current ftp pwd:'+self.ftp.pwd())
            self.ftp.cwd('../')
        except Exception,e:
            logger_working.exception(str(e))
            logger_working.error(self.ftp.pwd())
            return

    def update(self):
        try:
            if not self.telnetConnect():
                return
            if not self.ftpConnect():
                return
            updatedirList = self.ftp.nlst('update')
            self.sinOut1.emit(u'创建临时文件存放原BOOT文件')
            self.tel.delFiles(config.TEMPBDIR)
            self.tel.mkDir(config.TEMPBDIR)
            if  self.parambackupDelete:
                pathDir = os.path.join(config.ROOTDIR, 'Parameter_backup')
                if self.tel.movePath(pathDir,config.TEMPBDIR):
                    self.sinOut1.emit(u'移动： %s 至%s'%(pathDir,config.TEMPBDIR))
            for pathName in updatedirList:
                isFile = False
                if '.' in pathName:
                    isFile = True
                    pathDir = config.ROOTDIR
                else:
                    pathDir = os.path.join(config.ROOTDIR,pathName)
                    if self.tel.movePath(pathDir,config.TEMPBDIR):
                        self.sinOut1.emit(u'移动： %s 至%s'%(pathDir,config.TEMPBDIR))
                    self.tel.mkDir(pathDir)
                souseDir = os.path.join(config.UPDATEDIR,pathName)
                self.sinOut1.emit(u'复制： %s 至%s'%(souseDir,pathDir))
                if isFile:
                    self.tel.copyFile(souseDir,pathDir)
                else:
                    self.tel.copyFiles(souseDir,pathDir)
            self.sinOut1.emit(u'复制完成，请需启用BOOT，请重启PLC')
        except Exception,e:
            logger_working.exception(str(e))


    def telnetConnect(self):
        self.sinOut1.emit(u'正在telnet连接：%s'%self.tel.host)
        if not self.tel.telnet_connect():
            self.sinOut1.emit(u'启动TELNET连接失败，请确认配置文件中用户名密码正确')
            return False
        self.sinOut1.emit(u'启动TELNET连接成功')
        return  True

    def ftpConnect(self):
        self.sinOut1.emit(u'ftp连接：%s'%self.ftp.host )
        if not self.ftp.connect():
            self.sinOut1.emit(u'ftp连接失败，请确认配置文件中用户名密码正确')
            return False
        self.sinOut1.emit(u'ftp连接成功')
        return  True

    def __del__(self):
        print '__del__ for thread'
        if self.tel != None:
            try:
                self.tel.close()
            except Exception,e:
                print e
            self.tel = None
        if self.ftp != None:
            try:
                self.ftp.quit()
            except Exception,e:
                print e
            self.ftp = None


if __name__ == '__main__':
    host = '172.16.43.189'
    usr = 'guest'
    psw = '1'
    