# Setting up sockets
import socket
# Each thread operates independently, allowing the program to execute multiple tasks concurrently
# and improve overall efficiency.
import threading

IP = '127.0.0.1'
PORT = 9998

def main():  # Now we are going to define our function and call it main.
    # In this main function, we are going to set up a server object and assign it
    # to our TCP connection.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow the socket to reuse the address if it was recently used.
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((IP, PORT))  # Bind the server socket to the variables IP and PORT.
        server.listen(4)  # Depending on the integer, that determines how many network connections this server
        # listens to simultaneously.
        print(f'[*] Listening on {IP}:{PORT}')  # Print the IP and PORT the server is listening on.

        while True:  # Inside our 'while True' loop we want our server to endlessly listen for a connection.
            client, address = server.accept() # Our defined variables 'client' and 'address' are assigned to our
            # server and we want our server to accept these two variables per connection.
            print(f'[*] Accepted connection from {address[0]}:{address[1]}') # With the 0 index, we can see the IP.
            # Whereas with a 1 index, of the address variable, that would be the port because of the order.
            client_handler = threading.Thread(target=handle_client, args=(client,)) # Now we are defining a 'client
            # _handler' which shows us what happens when we have successfully handled a network connection.
            client_handler.start() # Now that we have our 'client_handler' creates a thread, per network connection,
            # we need the client_handler actually starts per connection.

    except OSError as e:
        print(f"OS error: {e}")  # Print the error if binding fails.
    finally:
        server.close()  # Ensure that the server socket is closed properly.

def handle_client(client_socket):  # Function defined to handle client connections.
    while True:  # This 'while True' loop needs to run indefinitely to handle incoming data from the client.
        try:
            request = client_socket.recv(1024)  # We can receive up to 1024 bytes of data from the tcp client.
            # The data the client sends might come in as several small packets or one big packet.
            # Using a 1024-byte buffer lets you handle a good amount of data to the server with just one receive call,
            # without needing a ton of memory.
            if not request:  # If no data is received, it means the client has closed the connection.
                break
            print(f'[*] Requested: {request.decode("utf-8")}')  # Print the received data.

            # Send an ACK response to the client to acknowledge receipt of the data.
            ack_message = "ACK"  # This message is to be sent as an acknowledgment that the server received the
            # client's data.
            client_socket.send(ack_message.encode("utf-8"))  # Encode the message as bytes and send the ack_message
            # back to the client.

        except Exception as e:
            print(f"Error: {e}")  # Log any errors encountered during data reception.
            break
    client_socket.close()  # Close the client socket when done.

if __name__ == "__main__":
    main()  # If the name of the function is called main, then let's call the main function to start the server.


