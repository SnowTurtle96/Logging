import json

class Utils:
    def combineJSONFiles(self, oldData, newUser):

        with open('DHT.json') as dhtfile:
            data = json.loads(dhtfile.read())
            oldData = str(oldData)
            newUser = str(newUser)
            oldData = oldData.replace(']', "")
            oldData = ''.join((oldData, ','))
            newUser = ''.join((newUser, ']'))

            sanitised = oldData + newUser
            sanitised = sanitised.replace('\'', '"')

            return sanitised