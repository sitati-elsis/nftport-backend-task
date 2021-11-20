# NFTPort Backend Test Assignment

### Getting NFTs

Use this [API endpoint](https://docs.nftport.xyz/docs/nftport/b3A6MjAzNDUzNTQ-retrieve-contract-nf-ts)
to fetch all contract addresses and token ids.

### Web3 gateway

Connects to the EVM compatible blockchain and fetches either tokenUri() or uri()
value from a given smart contract. Example usage in `web3_example.py`

Deploy web3 gateway:

```
cd web3_gateway
docker-compose up
```

Run example:

```
conda env create -f environment.yml
conda activate nftport-backend-task
python web3_example.py
```

Or just implement the equivalent API call in your language. 

# Setup Development Environment Using docker-compose
`docker-compose` comes in handy when you don't want to clutter your bare-metal machine with additional services. Those services can instead be made available through docker containers.

## Prerequisites
* docker
  - This is the software platform that runs and manages containers.
  - Download and install [instructions can be found here](https://docs.docker.com/engine/install/).
* docker-compose
  - This is a tool that runs on docker.
  - It is used for defining and running a multi-container Docker application.
  - Download and install [instructions can be found here](https://docs.docker.com/compose/install/)

## Running the docker-compose Development Environment
Use the following command to run the app.
```bash
docker-compose up
```
The host port for the app is `port 8080` therefore the app runs on `http://localhost:8080/`

To stop the app, use Ctrl + C on the terminal. 
```bash
^CGracefully stopping... (press Ctrl+C again to force)
```

To stop the app and remove containers created by `docker-compose up`, run the following.
```bash
docker-compose down
```

`docker-compose` can also be used to build a new api image after new changes have been made to the code.
```bash
docker-compose build
```

## Endpoints

1. `GET /api/v1/nfts/<contract_address>`: returns all the nfts for a givenn contract address
