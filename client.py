import socket
from time import time # Import the 'time' function from the time module which offers a range of time-related functions.

# Create a dictionary ({}) to keep track of client requests
client_requests = {}

def handle_client(client_socket): # Function defined to handle client connections regarding our client socket.
    # Get the IP address of the client making the request
    client_ip = client_socket.getpeername()[0]
    # Get the current time
    current_time = time()


# Check if the client's IP is already in the dictionary
    if client_ip in client_requests:
        # If so, retrieve the last request time and the count of requests
        last_request_time, request_count = client_requests[client_ip]

        # Check if the time since the last request is within the 60 seconds window (has to be no more than 60 seconds)
        if current_time - last_request_time < 60:  # Create a 60 seconds time window
            # Check if the number of requests exceeds the limit of 100
            if request_count > 100:  # Limit of 100 requests
                # Inform the client that they have exceeded the rate limit
                client_socket.send("Rate limit exceeded".encode("utf-8"))
                # Close the client connection
                client_socket.close()
                return # Proceed with the rest of the program
            # If a client computer issues another request within the same time window, make sure their number of
            # requests--shown by the last digit of the source port from the client machine incrementing by 1--as it
            # should because requests only add up.
            client_requests[client_ip] = (last_request_time, request_count + 1)
        else:
            # If instead, the time window has expired, reset the request count and update (document) when the last
            # request was made by which client with their IP address.
            client_requests[client_ip] = (current_time, 1)
    else:
        # If instead there is a mew client, add their IP address to the dictionary with their request count
        client_requests[client_ip] = (current_time, 1)


def client_program():  # def: defines/specifies the start of a new function
    # We call/define this function as client_program.'
    IP = '127.0.0.1'  # IP address of the server
    PORT = 9998  # Port number of the server

    # Here we are creating a variable named client that's assigned to the newly created socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT)) # Have the client socket connect to the server's IP and PORT

    try:
        message = "Hello, Server! What's up?"  # Send the message to send to the server
        client.send(message.encode("utf-8"))  # Encode the message from string text to bytes and then send the
        # message to the server.

        response = client.recv(1024)  # Receive a response from the server,
        # each method call can receive up to 1024 bytes of data from the server. This data is in raw byte format
        # (i.e., in integer format rather than a human-readable text format.)
        # Byte data is a sequence of bytes that can be formatted from text to binary data.
        print(f"Server Response: {response.decode('utf-8')}")  # Print the server's response and make sure to decode
        # the Server's response using the UTF-8 encoding/decoding character standard so the bytes are decoded from
        # bytes to a string of text.

    except Exception as e:  # Follow the initial instructions for this program except for if this program encounters
        # an error, if so, then print the event that disrupted the flow of the program's execution and assign that
        # event to the variable 'e.'
        print(f"Error: {e}") # print the event

    finally:
        client.close()  # Close the client socket


if __name__ == "__main__":
    client_program()  # If the name of the function is called main,
    # then let's call the main function aka 'client_program.'

