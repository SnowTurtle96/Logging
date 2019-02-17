import logging
from time import sleep


def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

logger1 = setup_logger('first_logger', '/home/bedegaminguser/loggingdirectory/log1.log')
logger2 = setup_logger('second_logger', '/home/bedegaminguser/loggingdirectory/log2.log')
logger3 = setup_logger('third_logger', '/home/bedegaminguser/loggingdirectory/log3.log')
logger4 = setup_logger('fourth_logger', '/home/bedegaminguser/loggingdirectory/log4.log')
logger5 = setup_logger('fifth_logger', '/home/bedegaminguser/loggingdirectory/log5.log')

i = 0;
while(i < 1000):

    logger1.info("Debug Information")
    i+=1;
i = 0;
sleep(1)
while(i < 1000):

    logger4.info("Debug Information")
    i+=1;
i = 0;
sleep(1)

while(i < 1000):

    logger2.info("Debug Information")
    i+=1;
i = 0;
sleep(1)

while(i < 1000):

    logger5.info("Debug Information")
    i+=1;
i = 0;
sleep(1)
while(i < 1000):

    logger3.info("Debug Information")
    i+=1;