#!/usr/bin/python

import os, sys
import json
import pathlib
import subprocess

from InputArguments import InputArguments
from QueryPeer import QueryPeer
from BasicCorrectness import BasicCorrectness

from ctypes import cdll

def verdict(id):
    width = os.get_terminal_size().columns  
    print(f"{a:#<{width}}")

def main():
    inputArgs = InputArguments()
    inputArgs.printIntro()

    # Get Input Arguments
    peer1_name, peer2_name = inputArgs.getArguments()
    
    if peer1_name == None or peer2_name == None:
        return 

    width = os.get_terminal_size().columns  

    print("".center(width, '#'))
    print(" Starting Judging Procedure ".center(width, '#'))
    print("".center(width, '#'))
    print()

    query = QueryPeer()
    min_ledger_height = query.queryBlocksAndLedgers(peer1_name, peer2_name)

    print("".center(width, '#'))
    print(" Verifying Basic Correctness ".center(width, '#'))
    print("".center(width, '#'))
    print()

    basicCorrectness = BasicCorrectness()
    if basicCorrectness.checkBasicCorrectness(peer1_name) != 0:
        verdict(peer1_name)
        return
        
    if basicCorrectness.checkBasicCorrectness(peer2_name) != 0:
        verdict(peer2_name)
        return

    print("".center(width, '#'))
    print(" Verifying Consistency ".center(width, '#'))
    print("".center(width, '#'))
    print()

    basePath = pathlib.Path().parent.absolute()

    dir1 = basePath / "data/{}_blocks/blocks/".format(peer1_name)
    dir2 = basePath / "data/{}_blocks/blocks/".format(peer2_name)
    pkFile = pathlib.Path().parent.absolute().parent.parent / "KafkaKeyPair/public.key"

    runGoCommand = "fabric_judge {} {} {} {} {} 10 512000".format(dir1, dir2, peer1_name, peer2_name, pkFile)
    process = subprocess.Popen(runGoCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error != None:
        return

    print()
    print("".center(width, '#'))
    print(" Blocks are semantically equal ".center(width, '#'))
    print("".center(width, '#'))
    print()

if __name__ == "__main__":
    main()
