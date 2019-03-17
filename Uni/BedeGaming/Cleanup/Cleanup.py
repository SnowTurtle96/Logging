import logging
import zipfile
import os
import psutil
import shutil


loggingdirectory = '../Logging Directory'
loggingfile = ''

ziph = zipfile.ZipFile('logzipped.zip', 'w', zipfile.ZIP_DEFLATED)
# Mode determines what action should be taken against log files once we hit 95% usage
mode = 'ZIP'

obj_Disk = psutil.disk_usage('D:')

logging.info(obj_Disk.total / (1024.0 ** 3))
logging.info(obj_Disk.percent)


def main():
    global mode

    if(obj_Disk.percent > 99):
        mode = 'ROTATE'
        actionToBeTaken()
        logging.info("Disk space above 90%")
        logging.info("Running actions to conserve space")

    elif(obj_Disk.percent > 95):
        mode = 'ROTATE'
        actionToBeTaken()



    elif (obj_Disk.percent > 90):
        mode = 'ROTATE'
        actionToBeTaken()


    else:
        logging.info("Disk space within parameters, no action taken")


def actionToBeTaken():
    if (mode == 'ZIP'):
        print("ZIP")
        zipfunction(loggingdirectory, ziph)

    elif (mode == 'ROTATE'):
        print('Rotate')
        rotation()


    elif (mode == 'WIPE'):
        print('WIPE')
        removeFilesFromDirectory()


def zipfunction(path, zipf):
    for root, dirs, files in os.walk(path):
        for file in files:
            os.chdir(root)
            zipf.write(file)
            os.remove(file)

def rotation():
    os.chdir('../Logging Directory')
    with open('sample.log', 'r+') as f:
        shutil.copy2('sample.log', 'sample2.log')
        f.truncate(0)
        f.close()

def removeFilesFromDirectory():
    for root, dirs, files in os.walk(loggingdirectory):
        for file in files:
            os.chdir(root)
            os.remove(file)


if __name__ == "__main__":
    main()


