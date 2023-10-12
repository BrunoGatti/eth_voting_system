import socket

class Chairperson:
    def __init__(self):
        self.key_pairs = []  # List of (public_key, private_key) pairs
        self.current_key_index = 0

    def load_key_pairs(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file.readlines()]
                for line in lines:
                    if not line:
                        continue  # Skip empty lines
                    public_key, private_key = line.split()
                    self.key_pairs.append((public_key, private_key))
                print(f"Loaded {len(self.key_pairs)} key pairs from '{file_path}'")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"Error loading key pairs: {str(e)}")

    def send_next_key_pair_to_booth(self, host, port):
        if self.current_key_index < len(self.key_pairs):
            public_key, private_key = self.key_pairs[self.current_key_index]
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, port))
                    key_pair = f"{public_key} {private_key}"
                    s.sendall(key_pair.encode())
                    print(f"Sent key pair to Booth: {public_key} {private_key}")
                    self.current_key_index += 1
            except Exception as e:
                print(f"Error sending key pair to Booth: {str(e)}")
        else:
            print("All key pairs have been sent.")

    def show_prompt(self):
        print("\nChairperson Menu:")
        print("1. Load Key Pairs")
        print("2. Send Next Key Pair to Booth")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            file_path = input("Enter the path to the key pairs file: ")
            self.load_key_pairs(file_path)
        elif choice == '2':
            if not self.key_pairs:
                print("No key pairs loaded. Load key pairs first.")
            else:
                self.send_next_key_pair_to_booth('localhost', 4242)
        elif choice == '3':
            print("Exiting...")
            exit()
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    chairperson = Chairperson()
    while True:
        chairperson.show_prompt()

