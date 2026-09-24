from web3 import Web3 #used to communicate with the blockchain
from eth_account import Account #used to create wallet accounts, create transactions, and sign transactions
from app.domain.repositories import  BlockChainService
from app.infrastructure.securtiy.encryption import decrypt_key
import json
import os


def load_contract_abi() -> list:
    abi_path = os.path.join(os.path.dirname(__file__), "proofvault_abi.json") #loads the contract abi from the proofvault_abi.json file
    with open(abi_path, "r") as f:
        return json.load(f) #reads the abi from the file and returns it as a list

class MonadBlockChainService(BlockChainService):
    #run this function only once
    def __init__(self, monad_rpc_url: str, contract_address: str, contract_abi: list, chain_id: int):
        self.web3 = Web3(Web3.HTTPProvider(monad_rpc_url)) #creates a connection to monad rpc
        contract_address = Web3.to_checksum_address(contract_address) #converts the contract address to a checksum address
        self.chain_id=chain_id #chain id of the monad blockchain
        #create a contract object that allows us to interact with the smart contract on the monad blockchain
        self.contract = self.web3.eth.contract(
            address=contract_address, #adress of the smart contract on the monad blockchain
            abi=contract_abi, #instruction man ual for the smart contract on the monad blockchain
        )
        
        #function to calculate gas price to be used
    async def estimate_sign_cost(self, signer_wallet_address: str, creator_wallet_address: str, fingerprint_hash: str) -> float:
        estimated_gas = self.contract.functions.recordAgreement(
            bytes.fromhex(fingerprint_hash),
            Web3.to_checksum_address(creator_wallet_address),
            Web3.to_checksum_address(signer_wallet_address),
        ).estimate_gas({"from": signer_wallet_address})
    
        current_gas_price = self.web3.eth.gas_price
        estimated_cost_wei = estimated_gas * current_gas_price
    
        # added 10% in case gas price shifts slightly before the real tx executes
        buffered_cost_wei = int(estimated_cost_wei * 1.1)
    
        return float(self.web3.from_wei(buffered_cost_wei, "ether"))
        

    async def record_agreement(
        self, 
        signer_private_key: str, #private key of the signer which authorizes the signing of the agreement 
        fingerprint_hash: str, #unique hash of the agreement being sent to the blockchain
        counterparty_wallet_address: str, #wallet address of the counterparty
        creator_wallet_address: str, #wallet address of the creator
    ) -> str: 
        #decrypt the private key and load it into the wallet
        private_Key = decrypt_key(signer_private_key)
        account = Account.from_key(private_Key) #loading the private key into the wallet
        
        #estimating gas to be used
        estimated_gas = self.contract.functions.recordAgreement(
            bytes.fromhex(fingerprint_hash),
            Web3.to_checksum_address(creator_wallet_address),
            Web3.to_checksum_address(counterparty_wallet_address)
        ).estimate_gas({"from": account.address})
        
        #building the transaction to send to the monad blockchain
        transaction = self.contract.functions.recordAgreement(
            bytes.fromhex(fingerprint_hash), #converts the fingerprint hash from hex to bytes
            Web3.to_checksum_address(creator_wallet_address), #checking the address of the creator
            Web3.to_checksum_address(counterparty_wallet_address) #checking the address of the counterparty
        ).build_transaction({
            "from": account.address, #address of the signer
            "nonce": self.web3.eth.get_transaction_count(account.address), #getting the number of transactions sent from the signer's address to prevent replay attacks
            "gas": estimated_gas, 
            "gasPrice": self.web3.eth.gas_price, #getting the current gas price on the monad blockchain
            "chainId": self.chain_id 
        })
        
        #signing the transaction with the signer's private key
        signed_transaction = account.sign_transaction(transaction)
        
        #sending the signed transaction to the monad blockchain
        transaction_Hash = self.web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
        
        #waiting for confirmation
        receipt = self.web3.eth.wait_for_transaction_receipt(transaction_Hash)
        
        #returning it
        return receipt.transactionHash.hex()