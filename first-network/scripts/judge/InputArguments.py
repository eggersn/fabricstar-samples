import os, sys

class InputArguments:
    def printIntro(self):
        print("""This is a simple Judge Script to verify Consistency.

It will fetch the blocks of two given peers and compare them in an attempt to verify consistency. 
If they happen to be semantically unequal (meaning their world state differ), the judging procedure will determine the misbehaving parties according to the following protocol:

1. Basic Correctness: 
The judge starts by checking if all received blocks are well-formated. Furthermore, it verifies all signatures.
If at least one of those checks fail, the corresponding peer is to blame.

2. Consistency:
If basic correctness holds true, the judge checks whether there exist two blocks with the same block ID but different block bodies.
Since all transactions within the block contain a signature and merkle-proof of the kafka cluster, the judge first checks if there are two different transactions with the same sequence number of the kafka cluster.
In this case, the kafka cluster is blamed. 
Otherwise, the only remaining possibility for differing blocks is that they were cut differently. Thus, the judge examines the contained Time-to-Cut messages and renders a verdict to the 
misbehaving orderer.
""")

    def printHelp(self):
        print("""
    Usage: \"python judge.py -p [PEER0_NAME] -p [PEER1_NAME]\"

    Example: \"python judge.py -p peer0.org1.example.com -p peer1.org1.example.com

    Make sure that the peers names in the arguments are equal to the corresponding names of your docker container.
    """)

    # Currently, only the following inputs are valid
    # python judge.py -p [PEER0_NAME] -p [PEER1_NAME], or
    # python judge.py -h (or --help)
    def getArguments(self):
        args = sys.argv 
        if len(args) == 1 or (len(args) == 2 and (args[1] == "-h" or args[1] == "--help")):
            self.printHelp()
            return None, None
        if len(args) == 5 and args[1] == "-p" and args[3] == "-p":
            return args[2], args[4]
        print("Invalid Input! Printing Help Menu:\n")
        self.printHelp()