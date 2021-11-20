import requests
import os

"""
Start the web3 gateway service before running.

cd web3_gateway
docker-compose up
"""

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
payload = {
    "contract_id": "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d",
    "token_id": "0"
}
TOKEN_GATEWAY = os.getenv("TOKEN_GATEWAY", "http://localhost:3000")
result = requests.post(f"{TOKEN_GATEWAY}/get-token-uri", headers=HEADERS, json=payload)
result_json = result.json()
print(f"Got NFT tokenUri: {result_json}")
