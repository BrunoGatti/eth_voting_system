from web3 import Web3
import socket

class Booth:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider('http://172.22.112.1:7545'))  # Connect to your Ganache Ethereum client
        self.contract_address = "0xeEEbA05741c3C5E285e18f6fc44216040dBBA3D0"  # Replace with your contract address
        self.contract_abi = [{"../build/contracts/Ballot.json"}]  # Replace with your contract ABI
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.contract_abi)
        self.private_key = None
        self.public_key = None

    def receive_key_pair(self, key_pair):
        # Split the received key pair into public and private keys
        public_key, private_key = key_pair.split()
        self.public_key = public_key
        self.private_key = private_key

    def cast_vote(self, candidate):
        if not self.private_key:
            print("No private key available. Cannot cast vote.")
            return

        try:
            nonce = self.web3.eth.getTransactionCount(self.public_key)
            gas_price = self.web3.toWei('10', 'gwei')  # Adjust the gas price as needed
            gas_limit = 200000  # Adjust the gas limit as needed

            # Specify the function and arguments to call in your contract
            function = self.contract.functions.vote(candidate)
            transaction = function.buildTransaction({
                'chainId': 1,  # Replace with your chain ID
                'gas': gas_limit,
                'gasPrice': gas_price,
                'nonce': nonce,
            })

            # Sign the transaction with the private key
            signed_transaction = self.web3.eth.account.signTransaction(transaction, self.private_key)

            # Send the signed transaction
            transaction_hash = self.web3.eth.sendRawTransaction(signed_transaction.rawTransaction)
            print(f"Vote casted by {self.public_key} for candidate {candidate}. Transaction hash: {transaction_hash.hex()}")
        except Exception as e:
            print(f"Error casting vote: {str(e)}")

    def show_prompt(self):
        print("\nBooth Menu:")
        print("1. Receive Key Pair")
        print("2. Cast Vote")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            key_pair = input("Enter the received key pair (public_key private_key): ")
            self.receive_key_pair(key_pair)
        elif choice == '2':
            if not self.public_key:
                print("No key pair received. Receive a key pair first.")
            else:
                candidate = int(input("Enter the candidate (1, 2, or 3) to vote for: "))
                self.cast_vote(candidate)
        elif choice == '3':
            print("Exiting...")
            exit()
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    booth = Booth()
    while True:
        booth.show_prompt()

