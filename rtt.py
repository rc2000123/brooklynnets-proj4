import socket
import time

def get_rtt(host, port):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((host, port))
    
    try:
        # Send some data (a simple "ping" message)
        message = 'ping'
        start_time = time.time()  # Record the send time
        client_socket.sendall(message.encode())
        
        # Wait for the response
        response = client_socket.recv(1024)
        end_time = time.time()  # Record the receive time
        
        # Calculate RTT
        rtt = end_time - start_time
        print(f"RTT: {rtt} seconds")
        
    finally:
        # Close the socket to clean up
        client_socket.close()

# Example usage
get_rtt('example.com', 80)  # Replace 'example.com' and 80 with your server's host and port
