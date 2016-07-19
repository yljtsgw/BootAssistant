#!/usr/bin/env python
# coding:utf-8
import xml.etree.ElementTree as ET
from PyQt4.QtCore import QThread,pyqtSignal
import logging
CON_MOTIFY = 7
logger_xml = logging.getLogger('main.xml')    # 获取名为tst的logger


########################################################################
class xmlThread(QThread):
    """"""
    sinOut1 = pyqtSignal(str)
    sinOut2 = pyqtSignal(int)

    #----------------------------------------------------------------------
    def __init__(self,parent=None):
        """Constructor"""
        super(xmlThread, self).__init__(parent)

    
    def setup(self,souseXML,targetXML):
        self.souseXML = souseXML
        self.targetXML = targetXML

        logger_xml.info("souseXML:%s"%self.souseXML)
        logger_xml.info("targetXML:%s"%self.targetXML)


    def run(self):   
        try:
            parDic = self.getParDic(self.souseXML)
            if len(parDic) == 0:
                self.sinOut1.emit(u'xml中无需要修改的参数')
                self.sinOut2.emit()
                return 
            tree = ET.parse(self.targetXML)
            device = tree.getroot()[0]
            count = 0
            self.sinOut1.emit(u'准备开始修改参数')
            self.sinOut1.emit(u'源文件地址：%s'%self.souseXML)
            self.sinOut1.emit(u'目标文件地址：%s'%self.targetXML)
            for name in parDic:
                ret = self.alertByName(device, name, parDic[name])
                if ret:
                    count += 1
            backupFilename = "%s_%s"%(self.targetXML,u"_backup")
            print backupFilename
            self.backupFile(self.targetXML, backupFilename)
            self.write_xml(tree, self.targetXML)
            self.sinOut1.emit(u'所有参数修改完成,共%d个参数，修改%d个参数'%(len(parDic),count))
            self.sinOut2.emit(CON_MOTIFY)
        except Exception,e:
            self.sinOut1.emit(u'修改过程发生异常，详细请查看log文件')
            self.sinOut2.emit(CON_MOTIFY)
            logger_xml.exception(str(e))
            self.excel = None
            
    def backupFile(self,sourceFile,targetFile):  
        open(targetFile, "wb").write(open(sourceFile, "rb").read())        

    def write_xml(self,tree, out_path):
        '''将xml文件写出
          tree: xml树
          out_path: 写出路径'''
        tree.write(out_path, encoding="utf-8",xml_declaration=True)
        
    def alertByName(self,device,name,value):
        value = str(value)    
        key = device.find(name)
        if key == None:
            logger_xml.info("%s did not in target XML file"%name)
            return False
        print "before: ",key.tag, key.text
        if value == key.text:
            logger_xml.info("无需修改：  %s : %s "%(name, str(key.text)))
        else:
            logger_xml.info("修改：  %s : %s  --> %s"%(name, str(key.text), value))
            key.text = value        
            print "after: ",key.text
        return True
    
    def getParDic(self,XMLpath):
        try:
            dic = {}
            tree = ET.parse(XMLpath)
            root = tree.getroot()
            device = root[0]       
            parlist = device.getchildren()
            for i in parlist:
                print i.tag,i.text 
                dic[i.tag] = i.text
        except Exception,e:
            logger_xml.exception(str(e))
        return dic