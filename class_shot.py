# -*- coding :cp936-*-
# coding=utf-8
import subprocess
import os
import time
'''将sdcard中指定后缀名的文件复制到电脑里'''
class adb_files():
    def __init__(self, suffix, absolutepath):
        self.suffix = suffix
        self.absolutepath = absolutepath.replace('\\', '/')
    def store_path_get(self):
        foldername = time.strftime(r"%Y-%m-%d_%H-%M-%S", time.localtime())
        os.makedirs(r'%s' % ( foldername ))
        final_path = '%s\\\%s' % (self.absolutepath, foldername)
        return final_path
    def files_from_device(self):
        print "begin to get fileslist..."
        sfix = self.suffix
        p_filesget = subprocess.Popen("adb shell cd sdcard && ls |grep {suffix}".format(suffix=sfix),
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        files = p_filesget.stdout.read().decode('utf-8').encode('gb2312')
        Files = files.split('\r\r\n')[0:-2]
        return Files
    def copy_files_from_device(self):
        path = self.store_path_get()
        files = self.files_from_device()
        for file in files:
            p_copy = subprocess.Popen("adb pull /sdcard/{file} {file_path}\{file}".format(file=file, file_path=path),
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p_copy.wait()
            print "%s.png is copied " % file
            print '+'*15
        self.file_mainlog()
    def remove_files_from_device(self):
        print "begin to remove files from device..."
        files = self.files_from_device()
        for file in files:
            p_del = subprocess.Popen("adb shell cd sdcard && rm -r {filename}".format(filename=file),
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p_del.wait()
            print "%s is deleted from device" % file
            print '-'*15
        self.file_mainlog()
    def screencap_auto(self):
        print "begin to screencap ... "
        sfix = self.suffix
        for i in range(100):
            OK = raw_input('screencap?(y): '.decode('utf-8').encode('gb2312'))
            if OK =='y':
                p_cap = subprocess.Popen("adb shell /system/bin/screencap -p /sdcard/{filename}.{sfix}".format(filename=i, sfix=sfix),
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                p_cap.wait()
                print "%s.png is captured" % str(i)
            else:
                self.file_mainlog()
    def file_mainlog(self):
        o = raw_input("what do you want 2 do(r|c|s): ")
        if o == 'r':
            self.remove_files_from_device()
        elif o == 'c':
            self.copy_files_from_device()
        elif o == 's':
            self.screencap_auto()
        elif o == 'e':
            self.file_mainlog()
        else:
            print "work done-------"
            pass
if __name__ == "__main__":
    suffix = 'png'
    path = os.getcwd()
    pngfilemove = adb_files(suffix, path)
    pngfilemove.file_mainlog()










