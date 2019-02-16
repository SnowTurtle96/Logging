import logging
import zipfile
import ctypes
import os
import platform
import sys
import psutil

loggingdirectory = '../Logging Directory'
loggingfile = ''

ziph = zipfile.ZipFile('logzipped.zip', 'w', zipfile.ZIP_DEFLATED)
print(os.listdir(loggingdirectory))
# Mode determines what action should be taken against log files once we hit 95% usage
mode = 'ZIP'

obj_Disk = psutil.disk_usage('D:')

logging.info(obj_Disk.total / (1024.0 ** 3))
logging.info(obj_Disk.percent)


def main():
    if(mode == 'ZIP'):
        print("ZIP")
        zipfunction(loggingdirectory, ziph)


    if(mode == 'ROTATE'):
        print('Rotate')


    if(mode == 'WIPE'):
        print('WIPE')
        for root, dirs, files in os.walk(loggingdirectory):
            for file in files:
                os.chdir(root)
                os.remove(file)

    if(obj_Disk.percent > 95):
        os.chdir('../Logging Directory')
        with open('sample.log', 'r') as f:
            lines = f.read().splitlines()
            f.close()
            last_line = lines[-1]
            print(last_line)


    elif(obj_Disk.percent < 95):
        print("Space limit not reached")


def zipfunction(path, zipf):
    for root, dirs, files in os.walk(path):
        for file in files:
            os.chdir(root)
            zipf.write(file)
            os.remove(file)

