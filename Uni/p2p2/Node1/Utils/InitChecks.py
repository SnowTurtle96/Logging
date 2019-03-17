from pathlib import Path


def checkInitialSetup():
    my_file = Path("nodesRecieved.json")
    if my_file.is_file():

        return False
    else:
        return True

def checkDHTInitialized():
    my_file = Path("DHT.json")
    if my_file.is_file():

        return False
    else:
        return True

def checkSessionExists():
    my_file = Path("messagingPartner.json")
    if(my_file.is_file()):
        return False
    else:
        return True



