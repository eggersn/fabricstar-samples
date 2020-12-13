import os, sys
import docker
import re
import tarfile
import shutil

class QueryPeer:
    # Get the Docker Environment
    def getDockerClient(self):
        return docker.from_env()


    def checkIfDockerImageExists(self, peer_name):
        client = self.getDockerClient()

        for container in client.containers.list():
            if container.name == peer_name:
                return container 

        return None

    def getLedgerHeight(self, peer_container):
        ret = None
        try:
            ret = peer_container.exec_run("peer channel getinfo -c mychannel")
        except docker.errors.APIError:
            return -1
        
        pattern = re.compile("\"height\":[0-9]+")
        match = pattern.search(str(ret.output))

        if match:
            return int(match.group().split(":")[1])
        else:
            return -1

    def queryBlocksOfPeer(self, peer_container, peer_name, min_ledger_height):
        try:        
            peer_container.exec_run("rm -rf blocks")
            peer_container.exec_run("mkdir blocks")
            print("Querying for common blocks on", peer_name)
            for i in range(0, min_ledger_height):
                peer_container.exec_run("peer channel fetch {} -c mychannel".format(i))
                peer_container.exec_run("mv mychannel_{}.block blocks/.".format(i))
        except docker.errors.APIError:
            print("ERROR: Unable to fetch all blocks of", peer_name)
            return -1

        if not os.path.exists("data"):
            os.mkdir("data")
        try:
            f = open("data/{}_blocks.tar".format(peer_name), "wb")
            bits, stat = peer_container.get_archive("/opt/gopath/src/github.com/hyperledger/fabric/peer/blocks")
            for chunk in bits:
                f.write(chunk)
            f.close()
        except docker.errors.APIError:
            print("ERROR: Unable to retrieve blocks.tar from", peer_name)
            return -1

        print("Extracting blocks of ", peer_name)
        tar = tarfile.open("data/{}_blocks.tar".format(peer_name))
        tar.extractall("data/{}_blocks".format(peer_name))
        tar.close()
        os.remove("data/{}_blocks.tar".format(peer_name))
        print("Done for", peer_name)

        return 0

    def queryLedgerOfPeer(self, peer_container, peer_name):
        try:
            f = open("data/{}_ledger.tar".format(peer_name), "wb")
            bits, stat = peer_container.get_archive("/var/hyperledger/production/ledgersData/chains/chains/mychannel")
            for chunk in bits:
                f.write(chunk)
            f.close()
        except docker.errors.APIError:
            print("ERROR: Unable to retrieve ledger.tar from", peer_name)
            return -1

        print("Extracting ledger of ", peer_name)
        tar = tarfile.open("data/{}_ledger.tar".format(peer_name))
        tar.extractall("data/{}_ledger".format(peer_name))
        tar.close()
        os.remove("data/{}_ledger.tar".format(peer_name))
        print("Done for", peer_name)

        return 0

    def queryBlocksAndLedgers(self, peer1_name, peer2_name):
        # Retrieve docker containers as specified in the input arguments
        print("Checking if specified docker containers exist.")    
        peer1_container = self.checkIfDockerImageExists(peer1_name)
        peer2_container = self.checkIfDockerImageExists(peer2_name)

        if peer1_container == None or peer2_container == None:
            print("ERROR: At least one of the specified containers does not exist! Exiting...")
            return

        print("Both docker container are up and running.\n")

        # First, query for the minimum ledger height
        print("Querying common ledger prefix...")
        min_ledger_height = min(self.getLedgerHeight(peer1_container), self.getLedgerHeight(peer2_container))
        
        if min_ledger_height == -1:
            print("ERROR: Unable to query for ledger height!")
        print("Common ledger height is {}\n".format(min_ledger_height))    

        # Now, query for the common blocks in both containers
        if os.path.exists("data"):
            try:
                shutil.rmtree("data")
            except OSError as e:    
                print ("Error: %s - %s." % (e.filename, e.strerror))

        print("Start querying blocks...")
        err = min(self.queryBlocksOfPeer(peer1_container, peer1_name, min_ledger_height), self.queryBlocksOfPeer(peer2_container, peer2_name, min_ledger_height))
        if err == -1:
            return
        print("Queried blocks successfully.\n")

        print("Start querying ledgers...")
        err = min(self.queryLedgerOfPeer(peer1_container, peer1_name), self.queryLedgerOfPeer(peer2_container, peer2_name))
        if err == -1:
            return
        print("Queried ledgers successfully.\n")

        return min_ledger_height