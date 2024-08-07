import socket


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

