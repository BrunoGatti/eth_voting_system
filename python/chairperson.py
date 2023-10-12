import socket
import os

class Chairperson:
    def __init__(self):
        self.private_keys = []

    def load_private_keys(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.private_keys = [line.strip() for line in file.readlines()]
            print(f"Loaded {len(self.private_keys)} private keys from '{file_path}'")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"Error loading private keys: {str(e)}")

    def send_private_key_to_booth(self, private_key, host, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(private_key.encode())
                print(f"Sent private key to Booth: {private_key}")
        except Exception as e:
            print(f"Error sending private key to Booth: {str(e)}")

    def show_prompt(self):
        print("\nChairperson Menu:")
        print("1. Load Private Keys")
        print("2. Send Private Key to Booth")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            file_path = input("Enter the path to the private keys file: ")
            self.load_private_keys(file_path)
        elif choice == '2':
            if not self.private_keys:
                print("No private keys loaded. Load private keys first.")
                return
            private_key_index = int(input("Enter the index of the private key to send: "))
            if 0 < private_key_index <= len(self.private_keys):
                private_key = self.private_keys[private_key_index - 1]
                self.send_private_key_to_booth(private_key, 'localhost', 4242)
            else:
                print("Invalid private key index.")
        elif choice == '3':
            print("Exiting...")
            exit()
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    chairperson = Chairperson()
    while True:
        chairperson.show_prompt()

