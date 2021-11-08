from web3 import Web3
import json

def getErcMintable721AssetInfo(address):
   MINTABLE_ERC721_SELECTOR = Web3.keccak(text="MintableERC721Token(address,uint256)")[:4]
   print(MINTABLE_ERC721_SELECTOR)
   asset_info = MINTABLE_ERC721_SELECTOR + bytes.fromhex(address[2:]).rjust(32, b'\0')
   # For Mintable ERC721, asset_info is 36 bytes long.
   return asset_info


def getMintableErc721AssetType(address):
   asset_info = getErcMintable721AssetInfo(address)
   print('asset info is', asset_info)
   asset_type = Web3.solidityKeccak(["bytes", "uint256"], [asset_info, 1])
   return asset_type


def getMintableErc721AssetId(minting_blob, address):
   blob_hash = Web3.solidityKeccak(["bytes"], [minting_blob])
   asset_type = getMintableErc721AssetType(address)
   hash = Web3.solidityKeccak(["string", "bytes", "bytes"], ['MINTABLE:', asset_type, blob_hash])
   asset_id = (int.from_bytes(hash, "big") & 0x0000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) |  (1 << 250)
   return asset_id

minting_blob = {
    'token_base_url': 'https://www.google.com',
    'symbol': "RNM"
}

minting_blob_bytes = json.dumps(minting_blob).encode('utf8')

contract_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
print('mintable erc721 asset id is', getMintableErc721AssetId(minting_blob_bytes, contract_address))
