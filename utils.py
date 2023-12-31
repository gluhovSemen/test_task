import uuid

import eth_account
from eth_account.messages import encode_defunct
from web3 import Web3
from web3.auto import w3


def create_auth_token() -> str:
    """This function is used for creating unic user token"""
    return str(uuid.uuid4())


def get_signature(user_id, key) -> str:
    """This function hashes the user_id preparing message for signing and signs it using the private_key from config"""
    hashed_user_id = Web3.solidity_keccak(["uint256"], [user_id]).hex()
    signable_message = eth_account.messages.defunct_hash_message(
        hexstr=hashed_user_id
    ).hex()
    signed_message = w3.eth.account.signHash(signable_message, private_key=key)
    return signed_message.signature.hex()
