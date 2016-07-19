# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
import os
########################################################################
CON_PING = 0
class  cmdThread(QThread):
    """"""
    sinOut1 = pyqtSignal(str)
    sinOut2 = pyqtSignal(int)
    #----------------------------------------------------------------------
    def __init__(self,parent=None):
        """用于CMD通讯并返回屏幕打印数据"""        
        super(cmdThread, self).__init__(parent)
    
    def cmd(self,strcmd):
        self.strcmd = strcmd
        self.start()

    def run(self):
        ret = os.popen(self.strcmd).read()
        self.sinOut1.emit(ret)
        self.sinOut2.emit(CON_PING)
        return 