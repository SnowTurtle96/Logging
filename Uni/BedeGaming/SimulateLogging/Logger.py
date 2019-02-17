import logging



logging1 = logging.basicConfig(filename="/home/bedegaminguser/loggingdirectory/sample1.log",format='%(asctime)s %(message)s', level=logging.INFO)
logging2 = logging.basicConfig(filename="/home/bedegaminguser/loggingdirectory/sample2.log",format='%(asctime)s %(message)s', level=logging.INFO)
logging3 = logging.basicConfig(filename="/home/bedegaminguser/loggingdirectory/sample3.log",format='%(asctime)s %(message)s', level=logging.INFO)
logging4 = logging.basicConfig(filename="/home/bedegaminguser/loggingdirectory/sample4.log",format='%(asctime)s %(message)s', level=logging.INFO)
logging5 = logging.basicConfig(filename="/home/bedegaminguser/loggingdirectory/sample5.log",format='%(asctime)s %(message)s', level=logging.INFO)



i = 0;
while(i < 2000):

    logging1.debug("Debug Information")
    logging2.info("Informational message")
    logging3.error("Error Information!")
    logging4.error("Error Information!")
    logging5.error("Error Information!")
    i+=1;