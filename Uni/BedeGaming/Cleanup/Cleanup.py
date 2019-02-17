import glob
import logging
import zipfile
import ctypes
import os
import platform
import sys
import psutil
import shutil

logger = logging.getLogger()
logger.setLevel(logging.INFO)

loggingdirectory = '/home/bedegaminguser/loggingdirectory'

# Mode determines what action should be taken against log files once we hit 95% usage
mode = 'ROTATION'
disk = '/home'
obj_Disk = psutil.disk_usage(disk)
diskUsedSpace = obj_Disk.percent



class Cleanup():

    def zipfunction(path, zipf):
        for root, dirs, files in os.walk(path):
            for file in files:
                os.chdir(root)
                zipf.write(file)
                os.remove(file)

    def rotation(self):
        os.chdir(loggingdirectory)
        list_of_files = glob.glob(loggingdirectory)  # * means all if need specific format then *.csv
        try:
            sorted_files = sorted(list_of_files, key=os.path.getmtime)
            print(sorted_files[-1])
            print(sorted_files[-2])
            print(sorted_files[-3])
        except IndexError:
            logging.error("No logs to delete")



            # shutil.copy2(latest_file, 'log2.log')
            # f.truncate(0)
            # f.close()

    def removeFilesFromDirectory(self):
        for root, dirs, files in os.walk(loggingdirectory):
            for file in files:
                os.chdir(root)
                os.remove(file)

    def main(self):
        global mode
        logging.info("Cleaning Script Started")
        logging.info("Disk selected: " + disk)
        logging.info("Selected Hard Disk Size: " + str(obj_Disk.total / (1024.0 ** 3)))
        logging.info("Percent of harddrive space used: " +  str(diskUsedSpace))

        if(diskUsedSpace > 99):
            mode = 'ROTATE'
            self.actionToBeTaken()
            logging.warning("Disk space above 99%")
            logging.info("Running actions to conserve space")

        elif(diskUsedSpace > 95):
            mode = 'ROTATE'
            self.actionToBeTaken()
            logging.warning("Disk space above 95%")


        elif (diskUsedSpace > 90):
            mode = 'ROTATE'
            self.actionToBeTaken()
            logging.warning("Disk space above 90%")

        else:
            logging.info("Disk space within parameters (NO ACTION TAKEN)")

            mode = 'ROTATE'
            self.actionToBeTaken()




    def actionToBeTaken(self):
        if (mode == 'ZIP'):
            print("ZIP")
            ziph = zipfile.ZipFile('logzipped.zip', 'w', zipfile.ZIP_DEFLATED)
            self.zipfunction(loggingdirectory, ziph)

        elif (mode == 'ROTATE'):
            print('Rotate')
            self.rotation()


        elif (mode == 'WIPE'):
            print('WIPE')
            self.removeFilesFromDirectory()





if __name__ == "__main__":
    Cleanup().main()


