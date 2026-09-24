import asyncio 
import os 
from web3 import Web3
from dotenv import load_dotenv
from eth_account import Account

load_dotenv()

class TreasuryWalletPool:
    def __init__(self, web3: Web3, chain_id: int):
        self.web3 = web3
        self.chain_id = chain_id
        self.accounts = [
            Account.from_key(os.getenv("TREASURY_KEY_1")),
            Account.from_key(os.getenv("TREASURY_KEY_2")),
            Account.from_key(os.getenv("TREASURY_KEY_3"))
        ]
        self.locks = [asyncio.Lock() for _ in self.accounts] #create 3 separate lock object and store them
    
    async def fund_wallet_if_needed(self, recepient_address: str, required_mon_amt: float):
        current_bal = self.web3.eth.get_balance(Web3.to_checksum_address(recepient_address)) #get address of the recipient
        current_mon_bal = float(self.web3.from_wei(current_bal, "ether")) #check recepient bal
        
        if current_mon_bal >= required_mon_amt:
            return #do not fund recipient wallet
        
        top_up_amt = required_mon_amt - current_mon_bal
        
        #find a free wallet 
        for account, lock in zip(self.accounts, self.locks):
            if not lock.locked():
                async with lock:
                    return await self._send_funding_tx(account, recepient_address, top_up_amt)
        #wait for the first wallet to become free then use
        async with self.locks[0]:
            return await self._send_funding_tx(self.accounts[0], recepient_address, top_up_amt)
    
    async def _send_funding_tx(self, account, recipient_addr: str, mon_amt: float):
        #building transaction details
        tx = {
            "from": account.address,
            "to": Web3.to_checksum_address(recipient_addr),
            "value": self.web3.to_wei(mon_amt, "ether"),
            "nonce": self.web3.eth.get_transaction_count(account.address),
            "gas": 21000,
            "gasPrice": self.web3.eth.gas_price,
            "chainId": self.chain_id
        }
        signed_tx = account.sign_transaction(tx) #sign the transaction
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction) #send to monad
        return self.web3.eth.wait_for_transaction_receipt(tx_hash) #receipt