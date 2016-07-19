# -*- coding: utf-8 -*-

"""
Module implementing BootAssistant.
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Ui_BootAssistant import Ui_BootAssistant

import os,shutil
from os.path import getsize,join
from cmdThread import cmdThread
from config import *
from WorkThread import workThread
from xmlthread import  xmlThread
import logging 
import logging.config



LOG_FILE = 'tst.log'
#输出到屏幕   
ch = logging.StreamHandler() 
#写入文件实例化
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler 
fmt = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter
logger_main = logging.getLogger('main')    # 获取名为tst的logger
logger_main.addHandler(handler)           # 为logger添加handler
#logger_main.addHandler(ch)
logger_main.setLevel(logging.DEBUG)


class BootAssistant(QMainWindow, Ui_BootAssistant):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QTextCodec.setCodecForCStrings(QTextCodec.codecForName('gbk'))
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.cmd = cmdThread()
        self.cmd.sinOut1.connect(self.printToTextEdit)
        self.cmd.sinOut2.connect(self.enableBotton)

        self.ip = getTemp('ip')
        self.lineEdit_ip.setText(self.ip)
        downloadDir = getTemp('downloadDir')
        self.lineEdit_getDir.setText(downloadDir)
        BootDir = getTemp('BootDir')
        self.lineEdit_localBootDir.setText(BootDir)
        
        self.work = workThread()
        self.work.sinOut1.connect(self.printToTextEdit)
        self.work.sinOut2.connect(self.enableBotton)

        self.xmlwork = xmlThread()
        self.xmlwork.sinOut1.connect(self.printToTextEdit)
        self.xmlwork.sinOut2.connect(self.enableBotton)

        self.uploadCheckDic = {'Boot':0,\
                          'CplusApplication':0,\
                          'EventAnalyze':0,\
                          'Parameter':0,\
                          'ReportApplication':0}



            
    @pyqtSignature("")
    def on_pushButton_GetBoot_clicked(self):
        """
        下载BOOT到指定文件夹内
        """
        IP = str(self.lineEdit_ip.text())
        self.work.setup(IP,USER, PSW)
        fileDir = GETFILENAME
        getDir = self.lineEdit_getDir.text()
        targetDir = unicode(getDir,'gbk')
        localdir = os.path.join(targetDir,fileDir)
        if os.path.isdir(localdir):
            ret = QMessageBox.warning(self, 'WARNING', u'本地文件夹内已存在同名下载文件夹，确认是否重新下载\n确认则删除原有文件并下载，取消则终止下载,忽略则继续下载', QMessageBox.Yes, QMessageBox.No,QMessageBox.Ignore)
            if ret == QMessageBox.No:
                return
            elif ret == QMessageBox.Yes:
                shutil.rmtree(localdir)
        self.pushButton_GetBoot.setEnabled(False)
        self.work.downloadFiles(fileDir, targetDir)
    
    @pyqtSignature("")
    def on_pushButton_openBootDir_clicked(self):
        """
        打开选择保存BOOT的路径
        """
        BootDir = self.lineEdit_getDir.text()
        BootDir = unicode(BootDir,'gbk')
        print BootDir
        if not os.path.exists(BootDir):
            os.makedirs(BootDir)
        os.startfile(BootDir)        
    
    @pyqtSignature("")
    def on_toolButton_getDir_clicked(self):
        """
        选择保存BOOT路径
        """
        getDir = self.lineEdit_getDir.text()
        getDir = unicode(getDir,'gbk')
        if getDir.strip() == '':
            lastDir = QString()
        else:
            lastDir = getDir
        fileDir = QFileDialog.getExistingDirectory(self, self.tr('Get Boot to..'), lastDir) 
        if fileDir =="" :
            return
        self.lineEdit_getDir.setText(fileDir)
        saveTemp("downloadDir",fileDir)

    @pyqtSignature("")
    def on_toolButton_localBootDir_clicked(self):
        """
        选择文件夹
        """
        getDir = self.lineEdit_localBootDir.text()
        getDir = unicode(getDir,'gbk')
        if getDir.strip() == '':
            lastDir = QString()
        else:
            lastDir = getDir
        fileDir = QFileDialog.getExistingDirectory(self, self.tr('Get Boot Direction..'), lastDir) 
        if fileDir =="" :
            return        
        self.lineEdit_localBootDir.setText(fileDir)
        saveTemp("BootDir",fileDir)


    
    
    @pyqtSignature("")
    def on_pushButton_upload_clicked(self):
        """
        上传选中的文件夹内的所有文件，上传前确认大小
        """
        fileDir = self.lineEdit_localBootDir.text()
        fileDir = unicode(fileDir,'gbk')
        filesize =  self.getdirsize(fileDir)
        sfilesize = self.converterSize(filesize)
        backupEnable = True
        ret = QMessageBox.warning(self, 'WARNING', u'文件夹大小为%s,确认是否上传'%sfilesize, QMessageBox.Yes, QMessageBox.No)
        if ret == QMessageBox.No:
            return
        ret = QMessageBox.warning(self, 'WARNING', u'是否备份文件', QMessageBox.Yes, QMessageBox.No)
        if ret == QMessageBox.No:
            backupEnable = False
        self.printToTextEdit(u'准备上传文件夹内文件，路径：%s\n总大小为%s'%(fileDir,sfilesize))
        IP = str(self.lineEdit_ip.text())
        self.work.setup(IP,USER, PSW)
        self.pushButton_upload.setEnabled(False)
        self.work.uploadFiles(fileDir,backupEnable)
        
    @pyqtSignature("")
    def on_pushButton_updateBoot_clicked(self):
        ret = QMessageBox.warning(self, 'WARNING', u'是否删除参数备份文件夹', QMessageBox.Yes, QMessageBox.No,QMessageBox.Cancel)
        parambackupDelete = True
        if ret == QMessageBox.No:
            print 'NO'
            parambackupDelete = False
        elif ret == QMessageBox.Cancel:
            return False
        IP = str(self.lineEdit_ip.text())
        self.work.setup(IP,USER,PSW)
        self.pushButton_updateBoot.setEnabled(False)
        self.work.updatePlc(parambackupDelete)

        

    @pyqtSignature("")
    def on_pushButton_resetPLC_clicked(self):
        ret = QMessageBox.warning(self, 'WARNING', u'即将发送重启PLC命令，请确认是否重启', QMessageBox.Yes, QMessageBox.No)
        print QMessageBox.Cancel,ret,QMessageBox.No
        if ret == QMessageBox.No:
            return False
        IP = str(self.lineEdit_ip.text())
        self.work.setup(IP,USER,PSW)
        self.pushButton_resetPLC.setEnabled(False)
        self.work.restartPlc()

    
    @pyqtSignature("")
    def on_pushButton_cleanData_clicked(self):
        IP = str(self.lineEdit_ip.text())
        self.work.setup(IP,USER,PSW)
        self.pushButton_cleanData.setEnabled(False)
        self.work.cleanData()
    
    @pyqtSignature("")
    def on_pushButton_clean_clicked(self):
        self.textEdit.clear()
    
    @pyqtSignature("")
    def on_pushButton_ping_clicked(self):
        ip = str(self.lineEdit_ip.text()).strip()
        if ip == "":
            return 
        strcmd = 'ping %s'%ip
        self.printToTextEdit(strcmd + u"\n请稍等...")
        self.pushButton_ping.setEnabled(False)
        self.cmd.cmd(strcmd)
        saveTemp('ip',ip)


    @pyqtSignature("QString")
    def on_lineEdit_localBootDir_textChanged(self, p0):
        """
        Slot documentation goes here.
        """
        getDir = self.lineEdit_localBootDir.text()
        getDir = unicode(getDir,'gbk')
        filelist = os.listdir(getDir)
        if "Parameter" not in filelist:
            self.printToTextEdit(u'本地发布包文件夹路径中未包含Parameter')
            self.pushButton_MotifyXML.setEnabled(False)
        else:
            self.pushButton_MotifyXML.setEnabled(True)



    @pyqtSignature("")
    def on_pushButton_MotifyXML_clicked(self):
        """
        将需要修改的参数自动写入发布包中的unique文件中.
        """
        fileDir = self.lineEdit_localBootDir.text()
        fileDir = unicode(fileDir,'gbk')
        paraPath = os.path.join(fileDir,'Parameter')
        parapathlist = os.listdir(paraPath)
        uniquefilename = ''
        for filename in parapathlist:
            if 'Unique' in filename:
                if '.xml' in filename:
                    uniquefilename = filename
        if uniquefilename == '':
            self.printToTextEdit(u"未在发布包文件夹中找到Unique参数文件")
            return
        sousePath = QFileDialog.getOpenFileName(self, self.tr('Open xml'), fileDir,
                                                   self.tr("xml Files(*.xml)"))
        if sousePath == "":
            return

        self.printToTextEdit(u"加载参数修改文件：%s"%sousePath)
        sousePath = unicode(sousePath,'gbk')
        uniquefilePath = os.path.join(paraPath,uniquefilename)
        self.xmlwork.setup(sousePath,uniquefilePath)
        self.xmlwork.start()


    def printToTextEdit(self,strWords):
        #print type(strWords)
        try:
            strWords = unicode(strWords)
        except:
            pass 
        #strWords = strWords.encode('utf-8')
        self.textEdit.append(strWords)
        logger_main.info(strWords)

    def getdirsize(self, dir):  
        """
        计算文件夹内文件大小
        """        
        size = 0L  
        for root, dirs, files in os.walk(dir):  
            size += sum([getsize(join(root, name)) for name in files])  
        return size

    def enableBotton(self,funcType):
        if funcType == CON_DOWNLOAD:
            self.pushButton_GetBoot.setEnabled(True)
        elif funcType == CON_UPLOAD:
            self.pushButton_upload.setEnabled(True)
        elif funcType == CON_UPDATE:
            self.pushButton_updateBoot.setEnabled(True)
        elif funcType == CON_RESTARTPLC:
            self.pushButton_resetPLC.setEnabled(True)
        # elif funcType == CON_KILLCERHOST:
        #     pass
        elif funcType == CON_CLEANDISK2:
            self.pushButton_cleanData.setEnabled(True)
        elif funcType == CON_PING:
            self.pushButton_ping.setEnabled(True)
        elif funcType == CON_MOTIFY:
            self.pushButton_MotifyXML.setEnabled(True)

 
    def converterSize(self,size):
        """
        转换文件大小格式
        """
        if size >= 1048576.0:
            strsize = '%.2f Mb'%(size /1048576.0)
        elif size >= 1024.0:
            strsize = '%.2f KB'%(size/1024.0)
        else:
            strsize = '%.2f B'%size     
        return strsize

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    BootAssistant = BootAssistant()
    BootAssistant.show()
    sys.exit(app.exec_())
    

