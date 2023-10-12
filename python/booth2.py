import socket

class Booth:
    def __init__(self):
        self.private_key = None

    def start_server(self, host, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, port))
                s.listen()
                print(f"Booth is listening on {host}:{port}")
                while True:
                    conn, addr = s.accept()
                    with conn:
                        print(f"Received private key from Chairperson: {addr}")
                        self.private_key = conn.recv(1024).decode()
                        self.handle_votes()
        except Exception as e:
            print(f"Error: {str(e)}")

    def handle_votes(self):
        while True:
            print("Booth Menu:")
            print("1. Cast Vote")
            print("2. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                if self.private_key:
                    candidate = input("Enter the candidate to vote for (1, 2, or 3): ")
                    # Implement the logic to cast a vote using the private_key
                    print(f"Voted for candidate {candidate} using private key: {self.private_key}")
                else:
                    print("Private key not received. Cannot vote.")
            elif choice == '2':
                print("Returning to idle state...")
                return
            else:
                print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    booth = Booth()
    booth.start_server('localhost', 4242)

