import socket
import time
import subprocess

def get_rtt(host, port):

    try:
        command = f"sh -c \"time echo -e '\x1dclose\x0d' | telnet {host} {port}\""
        result = str(subprocess.run(command, check=True, shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout)
        # print(result)
        rtt = result.split("real\\t")[1][2:7]
        print(rtt)

            
    except subprocess.CalledProcessError:
        print("process error, could not get rtt")
        return None

'''     
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
'''
# Example usage
get_rtt('142.250.191.206', 80)  # Replace 'example.com' and 80 with your server's host and port
