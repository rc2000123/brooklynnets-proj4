import socket

# Example list of IPv4 addresses
ip_addresses = ['8.8.8.8', '8.8.4.4']

# Function to perform reverse DNS lookup
def reverse_dns_lookup(ip_addresses):
    for ip in ip_addresses:
        try:
            # Perform the reverse DNS lookup and get the first result
            hostname, _, _ = socket.gethostbyaddr(ip)
            print(f"IP Address: {ip} -> Hostname: {hostname}")
        except socket.herror as e:
            # Handle errors (e.g., no host name found for the IP address)
            print(f"IP Address: {ip} -> Error: {e}")

# Perform reverse DNS lookups on the provided list of IP addresses
reverse_dns_lookup(ip_addresses)
