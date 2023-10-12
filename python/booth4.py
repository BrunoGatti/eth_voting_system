import json
from web3 import Web3, HTTPProvider
from eth_account import Account
from web3.middleware import geth_poa_middleware
import socket

class Booth:
    def __init__(self, chairperson_ip, chairperson_port, contract_address, contract_abi_path):
        self.web3 = Web3(HTTPProvider(f"http://{chairperson_ip}:{chairperson_port}"))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.contract_address = contract_address
        self.contract_abi = self.load_contract_abi(contract_abi_path)
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.contract_abi)
        self.private_key = None
        self.public_key = None

    def load_contract_abi(self, abi_file_path):
        with open(abi_file_path) as json_file:
            contract_data = json.load(json_file)
            return contract_data["abi"]

    def set_keys(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    def vote(self, candidate):
        if self.private_key is None or self.public_key is None:
            print("Private and public keys are not set. Use 'set_keys' method to set them.")
            return

        nonce = self.web3.eth.get_transaction_count(self.public_key)
        candidate = int(candidate)

        tx = self.contract.functions.vote(candidate).build_transaction({
            'from':self.public_key,
            'chainId': '0x539',  # Replace with the correct chain ID
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('20', 'gwei'),
            'nonce': nonce,
        })
        
        print("Transaction Data:")
        print(tx)
        signed_tx = self.web3.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Vote for candidate {candidate} submitted. Transaction hash: {tx_hash.hex()}")

    def receive_keys_from_chairperson(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 4242))
            s.listen()
            print("Waiting for the chairperson to provide key pair...")
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024).decode("utf-8")
                public_key, private_key = data.split()
                print(public_key)
                print(private_key)
                self.set_keys(public_key, private_key)
                print("Received key pair from chairperson.")

if __name__ == "__main__":
    chairperson_ip = "172.22.112.1"
    chairperson_port = "7545"
    contract_address = "0xB52440e905af1abd7cdBE2f3852F2c526Cda7Fa9"
    contract_abi_path = "../build/contracts/Ballot.json"
    
    booth = Booth(chairperson_ip, chairperson_port, contract_address, contract_abi_path)
    booth.receive_keys_from_chairperson()

    while True:
        candidate = input("Enter the candidate number to vote (1, 2, or 3): ")
        if candidate in ("1", "2", "3"):
            booth.vote(candidate)
        else:
            print("Invalid candidate number. Please choose 1, 2, or 3.")

