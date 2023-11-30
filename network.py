import socket
import time


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost" # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
                                    # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
                                    # ipv4 address. This feild will be the same for all your clients.
        self.port = 5555
        self.addr = (self.host, self.port)
        self.connected = False
        self.id = self.connect()
    
    def setConnection(self):
        self.connected = True

    def connect(self):
        count = 0
        while count < 3:
            try:
                print("connecting..")
                self.client.connect(self.addr)
                self.setConnection()
                return self.client.recv(2048).decode()
            except (socket.error, ConnectionRefusedError) as e:
                print(f"Connection failed: {e}")
                print("Retrying connection in 5 seconds...")
                time.sleep(5)  # Wait for 5 seconds before retrying
                count = count + 1
        print("server is down, connection not able to establish please try again later")

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            print("Str Encode Data:" + str(str.encode(data)))

            # Set a timeout for receiving data (adjust the timeout value as needed)
            self.client.settimeout(5)  # 5 seconds timeout for example

            try:
                reply = self.client.recv(2048).decode()
                print("Reply:" + str(reply))
                if (reply is None or reply == "") :
                    print("server unavailable")
                    return "Server is unavailable."
                else:
                    return reply
            except socket.timeout:
                print("Server didn't respond within the timeout.")
                return "Server is unavailable."
            except ConnectionResetError:
                print("Connection with the server was reset. Server is unavailable.")
                return "Server is unavailable."

        except socket.error as e:
            return str(e)