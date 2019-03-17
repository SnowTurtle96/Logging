from __future__ import print_function

from twisted.internet import reactor, protocol

from Node1.Client import Client
from Node1.Server.Server import ServerFactory

"""Tracks what state the node is in"""
state = "s1"
"""Instantiate Encryption"""
# client/request code for the node


def main():
    """Server"""
    factory = protocol.ServerFactory()
    factory.protocol = ServerFactory
    reactor.listenTCP(8000, factory)
    reactor.callLater(0, Client.Client)
    reactor.run()


if __name__ == '__main__':
    main()
