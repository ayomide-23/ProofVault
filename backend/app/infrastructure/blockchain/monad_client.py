from web3 import Web3 #used to communicate with the blockchain
from eth_account import Account #used to create wallet accounts, create transactions, and sign transactions
from app.domain.repositories import  BlockChainService
from app.infrastructure.securtiy.encryption import decrypt_key

class MonadBlockChainService(BlockChainService):
    #run this function only once
    def __init__(self, monad_rpc_url: str, contract_address: str, contract_abi: list):
        self.web3 = Web3(Web3.HTTPProvider(monad_rpc_url)) #creates a connection to monad rpc
        #create a contract object that allows us to interact with the smart contract on the monad blockchain
        self.contract = self.web3.eth.contract(
            address=contract_address, #adress of the smart contract on the monad blockchain
            abi=contract_abi #instruction manual for the smart contract on the monad blockchain
        )

    async def record_agreement(
        self,
        signer_private_Key: str, #private key of the signer which authorizes the signing of the agreement 
        fingerprint_hash: str, #unique hash of the agreement being sent to the blockchain
        counterparty_wallet_address: str, #wallet address of the counterparty
        creator_wallet_address: str, #wallet address of the creator
    ) -> str: 
        #decrypt the private key and load it into the wallet
        private_Key = decrypt_key(signer_private_Key)
        account = Account.from_key(private_Key) #loading the private key into the wallet
        
        #building the transaction to send to the monad blockchain
        transaction = self.contract.functions.recordAgreement(
            bytes.fromhex(fingerprint_hash), #converts the fingerprint hash from hex to bytes
            Web3.toChecksumAddress(creator_wallet_address), #checking the address of the creator
            Web3.toChecksumAddress(counterparty_wallet_address) #checking the address of the counterparty
        ).build_transaction({
            "from": account.address, #address of the signer
            "nonce": self.web3.eth.get_transaction_count(account.address), #getting the number of transactions sent from the signer's address to prevent replay attacks
            "gas": 3000000, 
            "gasPrice": self.web3.eth.gas_price, #getting the current gas price on the monad blockchain
            "chainId": 10143
        })
        
        #signing the transaction with the signer's private key
        signed_transaction = account.sign_transaction(transaction)
        
        #sending the signed transaction to the monad blockchain
        tranasaction_Hash = self.web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
        
        #waiting for confirmation
        receipt = self.web3.eth.wait_for_tranasaction_receipt(tranasaction_Hash)
        
        #returning it
        return receipt.transactionHash.hex()