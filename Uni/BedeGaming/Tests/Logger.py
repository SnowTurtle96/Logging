import logging

# add filemode="w" to overwrite
logging.basicConfig(filename="sample.log",format='%(asctime)s %(message)s', level=logging.INFO)

logging.debug("Debug Information")
logging.info("Informational message")
logging.error("Error Information!")