#!/usr/bin/env python
# coding:utf-8

from ftplib import FTP
import sys, logging, os

# DEBUG = True
logger_ftp = logging.getLogger('main.ftp')


########################################################################
class ftpTool():
    """ftp通讯"""

    # ----------------------------------------------------------------------
    def __init__(self, host, usr, psw):
        """ftp 初始化，输入IP ,用户名及密码"""

        self.host = host
        self.usr = usr
        self.psw = psw
        self.ftp = FTP()
        self.connected = False

    def connect(self, debuglevel=3):
        '''Connect ftp remote target machine.'''
        try:
            self.ftp.set_debuglevel(debuglevel)
            self.ftp.connect(self.host)
            self.ftp.login(self.usr, self.psw)
            print "login"
            self.connected = True
            return True
        except Exception as e:
            msg = 'Maybe your username or password is incorrect %s' % e
            logger_ftp.error(msg)
            return False

    def download_files(self, localdir='./', remotedir='./'):
        try:
            self.ftp.cwd(remotedir)
        except:
            logger_ftp.info(u'目录%s不存在，继续...' % remotedir)
            return
        if not os.path.isdir(localdir):
            os.makedirs(localdir)
        logger_ftp.info(u'切换至目录 %s' % self.ftp.pwd())
        self.file_list = []
        self.ftp.dir(self.get_file_list)
        remotenames = self.file_list

        for item in remotenames:
            filesize = item[0]
            filename = item[1]
            local = os.path.join(localdir, filename)
            self.download_file(local, filename, filesize)
        self.ftp.cwd('..')
        logger_ftp.info(u'返回上层目录 %s' % self.ftp.pwd())

    def download_file(self, localfile, remotefile, remotefile_size=-2):
        msg = ''
        if remotefile != -2:
            if self.is_same_size(localfile,  remotefile_size):
                msg = u'与本地文件大小相同，无需下载'
                return msg
        logger_ftp.info(u'>>>>>>>>>>>>下载文件 %s ... ...' % remotefile)

        file_handler = open(localfile, 'wb')
        self.ftp.retrbinary(u'RETR %s' % (remotefile), file_handler.write)
        file_handler.close()
        return msg

    def is_same_size(self, localfile,  remotefile_size):
        try:
            localfile_size = os.path.getsize(localfile)
        except:
            localfile_size = -1
        logger_ftp.info('localfile_size:%d  remotefile_size:%d' % (localfile_size, remotefile_size), )
        if remotefile_size == localfile_size:
            return 1
        else:
            return 0

    def uploadDir(self, localdir='./', remotedir='./'):
        try:
            if not os.path.isdir(localdir):
                return
            self.cwd(remotedir)
            for file in os.listdir(localdir):
                src = os.path.join(localdir, file)
                if os.path.isfile(src):
                    # file = unicode(file,'gbk')
                    self.uploadFile(src, file)
                elif os.path.isdir(src):
                    try:
                        self.ftp.mkd(file)
                    except:
                        logger_ftp.info('the dir is exists %s' % file)

                    self.uploadDir(src, file)

            logger_ftp.info('current ftp pwd:' + self.ftp.pwd())
            self.cwd('../')
        except Exception, e:
            logger_ftp.error(file)
            logger_ftp.exception(str(e))
            logger_ftp.error(self.ftp.pwd())

    def uploadFile(self, localpath, remotepath='./'):
        try:
            if not os.path.isfile(localpath):
                return False
            print 'Read to STOR%s' % (remotepath)
            self.ftp.storbinary('STOR ' + remotepath.encode('utf-8'), open(localpath, 'rb'))
            return True
        except Exception, e:
            logger_ftp.error(str(e))
            # self.ftp.quit()
            return False

    def getfileList(self, fileDir):
        try:
            self.ftp.cwd(fileDir)
        except:
            logger_ftp.info(u'目录%s不存在，继续...' % fileDir)
            return
        self.file_list = []
        try:
            print u"当前位置：", self.ftp.pwd()
            self.ftp.dir(self.get_file_list)
        except Exception:
            logger_ftp.error("cannot read file Direction : %s" % fileDir)
            self.ftp.quit()

        return self.file_list

    def get_file_list(self, line):
        ret_arr = []
        file_arr = self.get_filename(line)
        if file_arr[1] not in ['.', '..']:
            self.file_list.append(file_arr)

    def get_filename(self, line):
        pos = line.rfind(':')
        while (line[pos] != ' '):
            pos += 1
        while (line[pos] == ' '):
            pos += 1
        file_arr = str(line[pos:]).split(' ')
        return file_arr

    def cwd(self, filedir):
        try:
            self.ftp.cwd(filedir)
            logger_ftp.info(u'切换至目录 %s' % self.ftp.pwd())
        except:
            logger_ftp.error(u'目录%s不存在，继续...' % filedir)
            logger_ftp.error(u'切换至目录 %s' % self.ftp.pwd())
            return

    def mkd(self, file):
        self.ftp.mkd(file)

    def pwd(self):
        return  self.ftp.pwd()

    def quit(self):
        self.ftp.quit()
        self.connected = False

    def nlst(self, path = '.'):
        print 'nlst'
        return self.ftp.nlst(path)

    def clearDir(self,path):
        logger_ftp.info("ready to rmd %s"%path)
        filelist = self.nlst(path)
        logger_ftp.info(u"%s下有：%s"%(path,str(filelist)))
        if len(filelist) > 0:
            self.cwd(path)
            for i in filelist:
                try:

                    logger_ftp.info("Del :%s"%i)
                    self.ftp.delete(i)
                except Exception,e:
                    logger_ftp.info(self.pwd())
                    logger_ftp.error(str(e))

            self.cwd('\\')
        #self.ftp.rmd(path)


    def __del__(self):
        # self.ftp.close()
        try:
            if self.ftp != None:
                if self.connected == True:
                    self.ftp.quit()
                self.ftp = None
        except Exception,e:
            logger_ftp.exception(str(e))


if __name__ == '__main__':
    host = '172.16.43.169'
    usr = 'guest'
    psw = '1'
    ftp = ftpTool(host, usr, psw)
    ftp.connect()

    ftp.clearDir('sc')

