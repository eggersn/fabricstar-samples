import os, sys
import subprocess
import json

class BasicCorrectness:
    peer_name = None

    def runBlockVerifier(self):
        os.chdir("../block-verifier")
        subprocess.run(["npx", "bcverifier", "-n", "fabric-block", "-c", "../judge/data/{}_ledger/mychannel/blockfile_000000".format(self.peer_name), 
        "-o", "../judge/data/{}_ledger/mychannel/results.json".format(self.peer_name), "start"])
        os.chdir("../judge")

    def validateBlocks(self):
        with open("data/{}_ledger/mychannel/results.json".format(self.peer_name)) as json_file:
            data = json.load(json_file)
            for block in data["blocks"]:
                for result in block["results"]:
                    if result["result"] != "OK":
                        print("ERROR: Check failed for {} of {}".format(result[chckerID], self.peer_name))
                        return -1

        return 0


    def checkBasicCorrectness(self, peer_name):
        print("Verifying basic correctness for {}...".format(peer_name))

        self.peer_name = peer_name
        self.runBlockVerifier()

        print("Verifying blocks structure and signatures")
        if self.validateBlocks() != 0:
            print("ERROR: Basic Correctness not satisfied by {}".format(peer_name))
            return -1

        print("Verification successful\n")
        return 0

