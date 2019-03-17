import hashlib
import json
import logging
import os
import time
from pathlib import Path
from tkinter import *
from tkinter import scrolledtext

from twisted.internet import reactor, protocol, tksupport

from Node1 import Utils
from Node1.Client.DHTFactory import DHTFactory
from Node1.Client.DHTSearch import DHTSearch
from Node1.Client.MessageFactory import MessageFactory
from Node1.Client.RegisterFactory import MessageCFactory
from Node1.DHT.initialization import Initialization
from Node1.Encryption.Encryption import Encryption
from Node1.Models.User import User
from Node1.Utils import InitChecks

from Node1.TOR.OR import OR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format("./", "client")),
        logging.StreamHandler()
    ])
logger = logging.getLogger()

class Client(protocol.Protocol, logging.Handler):
    encryption = Encryption()
    initialSetup = True;
    recipitent = "N/A"
    recipitentKey = None
    recipitentPort = None
    recipitentIP = None
    peers = None
    user = None
    root = None
    nodeidval = None
    predecessorval = None
    successorval = None
    readyToMessage = None
    text_entry = None

    try:
        os.remove("messagingPartner.json")
    except:
        print("Error while deleting file ")





    """Read in our node list and user file if it exists, throw an exception if not"""

    def __init__(self):
        self.initialSetup = InitChecks.checkDHTInitialized()
        print(self.initialSetup)
        if (self.initialSetup):
            self.initialGUI()
            print("wow")

        if (self.initialSetup == False):
            self.peers = open("DHT.json", "r")
            self.peers = self.peers.read()
            self.peers = json.loads(self.peers)

            self.user = open("Models.json", "r")
            self.user = self.user.read()
            self.user = json.loads(self.user)
            self.mainGUI()




    def initialGUI(self):
        global root
        root = Tk()
        tksupport.install(root)
        root.geometry("300x300+200+200")
        root.title('GUI')
        root.geometry('{}x{}'.format(460, 350))

        leftFrame = Frame(root)
        leftFrame.pack(side="left", expand=True, fill="both")

        rightFrame = Frame(root)
        rightFrame.pack(side="right", expand=True, fill="both")

        leftFrame = Frame(root)
        leftFrame.pack(side="left", expand=True, fill="both")

        Label(leftFrame, text="Bootstrapping IP").grid(row=0, column=2, sticky=W)
        initialIP = Entry(leftFrame, width=19)
        initialIP.grid(row=1, column=2, sticky=W)

        Label(leftFrame, text="Boostrapping Port").grid(row=2, column=2, sticky=W)
        initialPort = Entry(leftFrame, width=19)
        initialPort.grid(row=3, column=2, sticky=W)

        Label(leftFrame, text="Your IP").grid(row=4, column=2, sticky=W)
        yourIP = Entry(leftFrame, width=19)
        yourIP.grid(row=5, column=2, sticky=W)

        Label(leftFrame, text="Your Port").grid(row=6, column=2, sticky=W)
        yourPort = Entry(leftFrame, width=19)
        yourPort.grid(row=7, column=2, sticky=W)

        Label(leftFrame, text="Username").grid(row=8, column=2, sticky=W)
        userName = Entry(leftFrame, width=19)
        userName.grid(row=9, column=2, sticky=W)

        Label(rightFrame, text="Username").grid(row=8, column=2, sticky=W)
        username = Entry(rightFrame, width=19)
        username.grid(row=9, column=2, sticky=W)

        Label(rightFrame, text="Your IP").grid(row=10, column=2, sticky=W)
        yourip = Entry(rightFrame, width=19)
        yourip.grid(row=11, column=2, sticky=W)

        Label(rightFrame, text="Your Port").grid(row=12, column=2, sticky=W)
        yourport = Entry(rightFrame, width=19)
        yourport.grid(row=13, column=2, sticky=W)

        Button(leftFrame, text='Connect to existing',
               command=lambda arg1=initialIP, arg2=initialPort, arg3=yourIP, arg4=yourPort, arg5=userName: self.connectToExistingNetwork(arg1,arg2,arg3,arg4,
                                                                                           arg5)).grid(
            row=14, column=2, sticky=W)

        Button(rightFrame, text='Start a network',
               command=lambda arg1=yourip, arg2=yourport, arg3=username: self.createNewNetwork(yourip, yourport,
                                                                                               username)).grid(row=15,
                                                                                                               column=2,
                                                                                                               sticky=W)
        logger.info("GUI")

    def mainGUI(self):
        """Necessary to avoid recursion issues with 'after' call for updating successor and predecessor"""
        global root
        global predecessorval
        global successorval
        global nodeidval
        global readyToMessage
        global text_entry

        logger.info("GUI")
        root = Tk()
        tksupport.install(root)
        root.title(self.peers['nodeid']['user'])
        print(os.getcwd())
        root.iconbitmap('@logo.xbm')

        recipitentMessage = StringVar()
        recipitentMessage.set("Select a peer to message")

        recipitentIP = StringVar()
        recipitentIP.set("NULL")

        recipitentPORT = StringVar()
        recipitentPORT.set(10000)

        readyToMessage = StringVar()
        readyToMessage.set("CIRCUIT NOT CREATED")

        # menu left
        menu_left = Frame(root, width=10, height=50)
        menu_left_upper = Frame(menu_left, width=10, height=50)
        menu_left_lower = Frame(menu_left, width=10, height=50)

        menu_left_upper.grid(row=1, column=0, sticky=W)
        menu_left_lower.grid(row=1, column=1, sticky=W)


        # right area
        some_title_frame = Frame(root, bg="#dfdfdf")

        recipitentMessage = Label(some_title_frame, textvariable=recipitentMessage, bg="#dfdfdf",  borderwidth=2, relief="groove")

        recipitentMessage.grid(row=2, column=1)

        chat_textbox = scrolledtext.ScrolledText(root, width=70, height=30,  borderwidth=2, relief="groove")
        # canvas_area = Canvas(root, width=500, height=400, background="#ffffff")
        chat_textbox.grid(row=1, column=1)
        # chat_textbox.configure(state="disabled")

        """Create logging window"""
        logging2 = scrolledtext.ScrolledText(menu_left_lower, width=50, height=30,  borderwidth=2, relief="groove")
        logging2.grid(row=2, column=0)
        logging2.configure(font='TkFixedFont')

        """Create text handler"""
        text_handler = TextHandler(logging2)
        chat_handler = ChatHandler(chat_textbox)

        # Logging configuration
        logging.basicConfig(filename='test.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        """Add hander to the logger"""
        userInfo = logging.getLogger("1")
        userInfo.addHandler(text_handler)

        userInfo.info("Started Application")

        """Add hander to the logger"""
        chatA = logging.getLogger("2")
        chatA.addHandler(chat_handler)

        # status bar
        status_frame = Frame(root, height=10)
        messageToSend = StringVar()
        userToSearch = StringVar()

        messageToSend.set("Type here to send a message...")
        userToSearch.set("Search the DHT for a user")




        version = Label(menu_left_lower, text="Version: 1.0.0", width="20", borderwidth=2, relief="groove").grid(row=0, column=0,  sticky=W)
        author = Label(menu_left_lower, text="Author: Jamie Clarke", width="20", borderwidth=2, relief="groove").grid(row=0, column=1, sticky=EW)

        buttonToSearch = Button(menu_left_lower, width="10", text='Search!', command=lambda arg1=userToSearch: self.searchDHT(arg1)).grid(row=1, column=1, sticky=W)

        search_user = Entry(menu_left_lower, textvariable=userToSearch, width="80").grid(row=1, column=0, sticky=W)
        messageToSend.set("Type here to send a message...")

        text_entry = Entry(status_frame, textvariable=messageToSend, width="80")
        text_entry.grid(row=6, column=0, sticky=W)

        Button(status_frame, text='Send',
               command=lambda arg1=recipitentIP, arg2=recipitentPORT, arg3=messageToSend: self.sendMsg(arg1, arg2,
                                                                                                       arg3)).grid(row=6, column=1, sticky=EW)


        nodeidval = StringVar()
        predecessorval = StringVar()
        successorval = StringVar()

        nodeidval.set("DHT not intialized!")
        predecessorval.set("DHT not initialized!")
        successorval.set("DHT not initialized!")

        nodeid = Label(some_title_frame, textvariable=nodeidval, width=35, borderwidth=2, relief="groove").grid(row=1, column=0, sticky=W)
        predecessor = Label(some_title_frame, textvariable=predecessorval, width=35, borderwidth=2, relief="groove").grid(row=1, column=1, sticky=EW)
        successor = Label(some_title_frame, textvariable=successorval, width=35, borderwidth=2, relief="groove").grid(row=1, column=2)
        status = Label(some_title_frame, textvariable=readyToMessage, width=35, borderwidth=2, relief="groove").grid(row=1, column=3, sticky=W)

        menu_left.grid(row=0, column=10, rowspan=2, sticky="nsew")
        some_title_frame.grid(row=0, column=1, sticky="ew")
        status_frame.grid(row=2, column=0, columnspan=2, rowspan=4, sticky="ew")

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(1, weight=1)

        text_entry.config(state=DISABLED)

        self.repopulateListBox()

    def searchDHT(self, username):
        """Convert the username into a hash value that we can use to search the network"""
        usernameHash = hashlib.sha256(username.get().encode('utf-8')).hexdigest()
        print(usernameHash)

        DHTUserRequest = {}
        DHTUserRequest['username'] = usernameHash
        DHTUserRequest['ip'] = self.peers['nodeid']['ip']
        DHTUserRequest['port'] = self.peers['nodeid']['port']

        json_data = json.dumps(DHTUserRequest)

        reactor.connectTCP(self.peers['successor']['ip'], int(self.peers['successor']['port']), DHTSearch(DHTUserRequest))

    def repopulateListBox(self):
        global nodeidval
        global predecessorval
        global successorval
        global root
        global readyToMessage
        global text_entry
        self.peers = open("DHT.json", "r")
        self.peers = self.peers.read()
        self.peers = json.loads(self.peers)
        predecessorstr = self.peers['predecessor']['user']
        successorstr = self.peers['successor']['user']
        nodeidstr = self.peers['nodeid']['nodeid']

        predecessorval.set("Predecessor: " + predecessorstr)
        successorval.set("Successor: " + successorstr)
        nodeidval.set("Node ID: " + nodeidstr)

        sessionCreated = InitChecks.checkSessionExists()

        # TODO ALL INITIAL SETUPS TRUE AND FALSE ARE THE WRONG WAY ROUND LOGICALLY
        if(sessionCreated == False):
            readyToMessage.set("CIRCUIT CREATED!")
            text_entry.config(state=NORMAL)


        root.after(2000, self.repopulateListBox)


    def createNewNetwork(self, yourip, yourport, username):
        yourip = str(yourip.get())
        yourport = str(yourport.get())
        username = str(username.get())
        yourport = int(yourport)

        """Initialize DHT"""
        initialization = Initialization()

        self.encryption.generate_keys()

        user = User()
        user.ip = yourip
        user.port = yourport
        user.user = username
        user.publicKey = self.encryption.getPublicKey().decode("utf-8")
        user.nodeid = user.generateID()
        print("nodeid")
        print(str(user.nodeid))


        user2 = json.dumps(user.toDict())
        """Register username in a local file so we know who we are"""
        file = open("Models.json", "w+")
        file.write(str(user2))

        initialization = Initialization()
        initialization.fingerTable.nodeid = user.toDict()
        initialization.writeDHTInformation()



    def connectToExistingNetwork(self, initialIP, initialPort, yourIP, yourPort,  username):
        global listbox
        factory1 = protocol.ClientFactory()
        factory1.protocol = MessageCFactory
        initialIP = str(initialIP.get())
        initialPort = str(initialPort.get())
        yourIP = str(yourIP.get())
        yourPort = str(yourPort.get())
        username = str(username.get())
        """
        General data sanitation from the UI into things that our twisted application can understand
        Encoding as bytes for transfer
        """
        initialPort = int(initialPort)

        """Create our encryption keys"""
        self.encryption.generate_keys()
        logger.info("public key")
        logger.info(self.encryption.public_key)
        logger.info("Encryption public key")
        logger.info(self.encryption.getPublicKey())
        logger.info("Encryption private key")
        logger.info(self.encryption.getPrivateKey())

        """Initialize DHT"""
        initialization = Initialization()

        user = User()
        user.ip = yourIP
        user.port = yourPort
        user.user = username
        user.publicKey = self.encryption.getPublicKey().decode("utf-8")
        user.nodeid = user.generateID()

        initialization.fingerTable.nodeid = user.toDict()
        initialization.writeDHTInformation()

        print(user.publicKey)
        user.publicKey = self.encryption.getPublicKey().decode("utf-8")
        """Register username in a local file so we know who we are"""
        file = open("Models.json", "w+")
        userstr = json.dumps(user.toDict())
        file.write(str(userstr))
        logger.info("Models Dict" + userstr)
        print(userstr)
        reactor.connectTCP(initialIP, initialPort, DHTFactory(userstr))

    def listboxEvent(self, evt, recipitentMessage, recipitentIP, recipitentPORT):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        recipitent = value
        logger.info(recipitentIP.get() + "rec")

        for peer in self.peers:
            print(type(peer))
            if peer['successor'] == recipitent or peer['predecessor'] == recipitent:
                recipitentMessage.set("Now messaging " + value + " " + "(" + peer['ip'] + ")")
                recipitentIP.set(peer['ip'])
                recipitentPORT.set(peer['port'])
                self.recipitentIP = peer['ip']
                self.recipitentPort = peer['port']
                self.recipitentKey = peer['publickey']
                print(self.recipitentKey)

    def sendMsg(self, ip, port, msg):
        msgCMD = "==MSG=="
        port = int(port.get())
        ip = ip.get()



        """Assign protocol command"""
        msg = msgCMD + self.currentUser().upper() + ":" + " " + msg.get()

        #Instantiate our onion router
        onionRouter = OR()
        #Set the end node (reciever)
        onionRouter.setRecieverIP(ip)
        onionRouter.setRecieverPort(port)
        #Create our circuit
        onionRouter.constructRoute(self.peers)
        #Sanitise our circuit into a more friendly JSON format
        #Create symmetrical encryption keys for use at each hop of the circuit
        onionRouter.createKeys()
        onionRouter.encryptMsgForOnionRouting(msg)

        messageToSend = onionRouter.onionDict
        messageToSend = str(messageToSend)
        messageToSend = bytes(messageToSend, 'utf-8')

        print(messageToSend)
        reactor.connectTCP(onionRouter.route.hop1['ip'], int(onionRouter.route.hop1['port']), MessageFactory(messageToSend))

        sanitisedData = msg.replace('==MSG==', '')
        chatA = logging.getLogger("2")
        chatA.info(sanitisedData)

    def currentUser(self):
        return self.user['user']


class TextHandler(logging.Handler):

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state='normal')
            self.text.insert(END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(END)

        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


class ChatHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state='normal')
            self.text.insert(END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(END)

        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)