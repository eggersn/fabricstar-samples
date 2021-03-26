## Fabric* Samples
Mostly based on [fabric-samples](https://github.com/hyperledger/fabric-samples) with small modifications in first-network.
After following their official installation guide, a small Fabric* network can be started. Please ensure, that all required docker images are locally installed beforehand (i.e. fabric_star/kafka, fabric_star/fabric-orderer and fabric_star/fabric-peer).

## Fabric* Judge Implementation
After installing the Go counterpart [Fabric_Judge](https://github.com/eggersn/Fabric_Judge), the judging procedure can be executed in [first-network/scripts/judge](https://github.com/eggersn/fabricstar-samples/tree/master/first-network/scripts/judge).
For this, a functioning network should be running (using the first-network/byfn.sh script). To make it more interesting, one can interact with the network using the following commands:
```console
# Start a shell on the client container 
docker exec -it cli /bin/bash
# Query the Ledger
peer chaincode query -C mychannel -n mycc -c '{"Args":["query","a"]}'
# Invoke (a sends 10 coins to b)
peer chaincode invoke -o orderer.example.com:7050 -C mychannel -n mycc --peerAddresses peer0.org1.example.com:7051 --peerAddresses peer0.org2.example.com:9051 -c '{"Args":["invoke","a","b","10"]}'
```
After performing a few transactions, one can call the juding procedure as follows (inside [first-network/scripts/judge](https://github.com/eggersn/fabricstar-samples/tree/master/first-network/scripts/judge))
```console
python Judge.py -p peer0.org1.example.com -p peer1.org1.example.com 
```
