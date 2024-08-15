import socket
import threading
import time

# Define a rate limit (e.g., max_requests per time_window seconds)
MAX_REQUESTS = 3
TIME_WINDOW = 10  # time window in seconds

# Dictionary to store the request timestamps for each client
client_requests = {}

IP = '127.0.0.1'
PORT = 9998

def main():
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

def handle_client(client_socket):
    client_address = client_socket.getpeername()  # Get the client's IP and port
    client_ip = client_address[0]

    while True:  # This 'while True' loop needs to run indefinitely to handle incoming data from the client machine.
        try:
            # Rate Time Limiting Check
            current_time = time.time()
            if client_ip in client_requests:
                request_times = client_requests[client_ip]
                # Remove timestamps outside of the time window
                request_times = [t for t in request_times if current_time - t < TIME_WINDOW] # This function generates
                # a new list that includes only the timestamps from the request_times collection that fall within the
                # specified TIME_WINDOW. In other words, it filters out any timestamps that lie outside the defined
                # time frame, thereby retaining solely the most recent requests.
                client_requests[client_ip] = request_times

                # What do these lines of code mean?

                if len(request_times) >= MAX_REQUESTS: # If the length (i.e. "number of items") of request_times
                    # (attempts) is more than or equal to the MAX_REQUESTS you can make. Then send (print) the
                    # error_message and break the try loop.

                    # Since it would not be "true," it would be "false" logic for the number of requests to be more
                    # than or equal to the given TIME_WINDOW of opportunity to make a request (request_time) which is
                    # the same as the current_time.

                    error_message = "Error: Rate limit exceeded. Please try again later."
                    client_socket.send(error_message.encode("utf-8"))
                    print(f'[*] Rate limit exceeded for {client_ip}')
                    break

            # Receive data from the client
            request = client_socket.recv(1024)  # We can receive up to 1024 bytes of data from the tcp client.
            if not request:  # If no data is received, it means the client has closed the connection.
                break
            print(f'[*] Requested: {request.decode("utf-8")}')  # Print the received data.

            # Add (or "append") the current timestamp to the client's request times
            if client_ip not in client_requests:
                client_requests[client_ip] = []
            client_requests[client_ip].append(current_time)

            # Send an ACK response to the client to acknowledge receipt of the data.
            ack_message = "ACK"  # This message is to be sent as an acknowledgment that the server received the
            # client's data.
            client_socket.send(ack_message.encode("utf-8"))  # Encode the message as bytes and send the ack_message
            # back to the client.

        except Exception as e:
            print(f"Error: {e}")  # Log any errors encountered during data reception, if any.
            break
    client_socket.close()  # Close the client socket when done.

if __name__ == "__main__":
    main()  # If the name of the function is called main, then let's call the main function to start the server.


