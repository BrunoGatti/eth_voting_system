import socket

class Chairperson:
    def __init__(self):
        self.private_keys = []
        self.current_key_index = 0

    def load_private_keys(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.private_keys = [line.strip() for line in file.readlines()]
                print(f"Loaded {len(self.private_keys)} private keys from '{file_path}'")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"Error loading private keys: {str(e)}")

    def send_next_private_key_to_booth(self, host, port):
        if self.current_key_index < len(self.private_keys):
            private_key = self.private_keys[self.current_key_index]
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, port))
                    s.sendall(private_key.encode())
                    print(f"Sent private key to Booth: {private_key}")
                    self.current_key_index += 1
            except Exception as e:
                print(f"Error sending private key to Booth: {str(e)}")
        else:
            print("All private keys have been sent.")

    def show_prompt(self):
        print("\nChairperson Menu:")
        print("1. Load Private Keys")
        print("2. Send Next Private Key to Booth")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            file_path = input("Enter the path to the private keys file: ")
            self.load_private_keys(file_path)
        elif choice == '2':
            if not self.private_keys:
                print("No private keys loaded. Load private keys first.")
            else:
                self.send_next_private_key_to_booth('localhost', 4242)
        elif choice == '3':
            print("Exiting...")
            exit()
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    chairperson = Chairperson()
    while True:
        chairperson.show_prompt()

