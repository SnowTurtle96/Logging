import logging

# add filemode="w" to overwrite
logging.basicConfig(filename="../Logging Directory/sample.log",format='%(asctime)s %(message)s', level=logging.INFO)
i = 0;
while(i < 2000):

    logging.debug("Debug Information")
    logging.info("Informational message")
    logging.error("Error Information!")
    i+=1;