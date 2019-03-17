class InitialNode:

    def createInitialNode(user):
        f = open("nodesRecieved.json", "w+")
        userJSONFormat = "[" + user + "]"
        f.write(str(userJSONFormat))
