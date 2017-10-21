# -*- coding :cp936-*-
# coding=utf-8
import os
import time
'''实现根据路径获取包名，覆盖安装，进入主页面检查效果，功能'''

class operation_mine():
    def __init__(self, file_dir):
        self.file_dir = file_dir.replace('\\', '/')+'/'
    def filenamelist_get(self):
        # filenamelist = [x for x in os.listdir(self.file_dir) if os.path.isfile(x) and \
        #                 os.path.splitext(x)[-1] == '.apk']
        filenamelist = []
        for root, dir1, files in os.walk(self.file_dir):
            for file1 in files:
                if os.path.splitext(file1)[-1] =='.apk':
                    filenamelist.append(os.path.join(root, file1))
        return filenamelist
    def install (self):
        print (" "*10)
        print ("start to install apps in your devices...")
        # os.open("adb wait for device...")
        oripackages = self.filenamelist_get()
        print "apk list : "
        count = 0
        for oripackage in oripackages:
            count += 1
            re_install_package = oripackage
            print (re_install_package.split('/')[-1])
            os.popen("adb install -r " + re_install_package)
            print (re_install_package.split('/')[-1] +" is installed "+ str(count))
            mainpack = os.popen("adb shell pm list packages {name}".format(name='tv'))
            for oripackage in mainpack:
                activepackage = oripackage.split(':')[1][0:-2]
                print ("Entering MainPage...")
                main_activity_name = "/MainActivity name of your apk package"
                os.popen("adb shell am start -n " + activepackage + main_activity_name)
            time.sleep(3)
            print ('-'*10+'*'+'-'*10)
        self.apk_mainlog()
    def delapk(self):
        print ("start to uninstall apps in your device... ")
        os.popen("adb wait for device...")
        corename = raw_input("input your ap package corename: ")
        oripackages = os.popen("adb shell pm list packages {name}".format(name='tv'))
        for oripackage in oripackages:
            deletePackage = oripackage.split(':')[1]
            os.popen("adb uninstall " + deletePackage)
            print (deletePackage + " is uninstalled ")
        self.apk_mainlog()
    def apk_mainlog(self):
        OK = raw_input("install or delete ? (i|d):")
        if OK == 'i':
            self.install()
        elif OK == 'd':
            self.delapk()
        else:
            print "work done-------"
            pass
if __name__ == "__main__":
    file_dir = "your apkpackage absolute path"
    ex = operation_mine(file_dir)
    ex.apk_mainlog()
