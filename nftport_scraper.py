from typing import AnyStr
from requests import get, post
import urllib.request
from application.models import Nft, Contract
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import os
import json
import concurrent
import concurrent.futures

NFT_PORT_API_URL = 'https://api.nftport.xyz/v0/nfts/{contract_address}?chain=ethereum&page_size=50&page_number={page_number}'

AUTH_HEADER = {"Authorization": "721c8e6c-4bc0-4ded-8c07-0350ce4b2430"}

engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql://postgres:postgres@postgres/postgres"))


DBSession = sessionmaker(bind=engine)

logger = logging.getLogger(__name__)


class BadRequest(Exception):
    pass


def scrape_contract_nfts(contract_address: AnyStr):
    logger.info(f"Starting to scrape nft for contract: {contract_address}")
    contract, nfts = get_contract_nfts(contract_address)
    logger.info(f"Saving contract for contract {contract_address}")
    save_contract(contract)
    logger.info(f"finished saving contract for {contract_address}")
    for nft in nfts:
        try:
            token_uri = get_token_uri(nft)
            nft_metadata = scrape_ipfs_token_metadata(token_uri)
            nft["token_uri"] = token_uri
            nft.update(nft_metadata)
            # Save  NFT
            save_nft(nft)
        except TypeError:
            logger.info("Skipping invalid token uri")
            continue
        except BadRequest as e:
            logger.info("Skipping invalid token request")
            logger.info(e)
            continue
    logger.info(f"Starting to scrape nft for contract: {contract_address}")


def save_nft(nft):
    session = DBSession()
    existing_record = session.query(Nft).filter_by(contract_address=nft["contract_address"],
                                                   token_id=nft["token_id"]).first()
    if existing_record is None:
        new_nft = Nft(**nft)
        session.add(new_nft)
        session.commit()
        session.close()
        # Download the image
        download_nft_assets(nft["image"])


def save_contract(contract):
    session = DBSession()
    existing_record = session.query(Contract).filter_by(contract_address=contract["contract_address"],
                                                        symbol=contract["symbol"]).first()
    if existing_record is None:
        new_contract = Contract(**contract)
        session.add(new_contract)
    session.commit()


def get_contract_nfts(contract_address: AnyStr):
    page_number = 1
    nfts = []
    contract = None
    while True:
        results = scrape_contract_nft_by_page(contract_address, page_number)
        if results["response"] != 'OK':
            # print validation error
            break
        elif len(results["nfts"]) == 0:
            # We got to end of page
            break
        nfts += results['nfts']
        if contract is None:
            contract = results["contract"]
            contract["contract_address"] = contract_address
        # Continue
        page_number += 1
    return contract, nfts


def download_nft_assets(img_uri):
    root_dir = os.path.dirname(os.path.realpath(__file__))
    assets_dir = os.path.join(root_dir, "application", "assets")
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    file_path = os.path.join(assets_dir, "%s.png" % os.path.basename(img_uri))
    urllib.request.urlretrieve(f"https://ipfs.io/ipfs/{os.path.basename(img_uri)}", file_path)


def scrape_ipfs_token_metadata(token_uri):
    if token_uri.startswith('ipfs://'):
        token_url = f"https://ipfs.io/ipfs/{token_uri.lstrip('ipfs://')}"
    else:
        token_url = token_uri
    response = get(token_url)
    if response.status_code != 200:
        raise BadRequest("invalid path for token uri")
    return response.json()


def get_token_uri(nft):
    HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "contract_id": nft["contract_address"],
        "token_id": nft["token_id"]
    }
    TOKEN_GATEWAY = os.getenv("TOKEN_GATEWAY", "http://localhost:3000")
    result = post(f"{TOKEN_GATEWAY}/get-token-uri", headers=HEADERS, json=payload)
    if result.status_code == 400:
        raise BadRequest("missing revert data in call exception")
    return result.json()["token_uri"]


def scrape_contract_nft_by_page(contract_address: AnyStr, page_number: int = 1) -> dict:
    url = NFT_PORT_API_URL.format(contract_address=contract_address, page_number=page_number)
    response = get(url, headers=AUTH_HEADER)
    return response.json()


def scrape_contracts():
    with open("collections.json", "r") as f:
        contracts = json.load(f)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            tasks = [executor.submit(scrape_contract_nfts, contract) for contract in contracts]
            for task in concurrent.futures.as_completed(tasks):
                logger.info(task.result())


scrape_contracts()
