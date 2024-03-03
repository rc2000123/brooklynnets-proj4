import subprocess

def check_tls_support(url):
    protocols = {
        "SSLv2": "-ssl2",
        "SSLv3": "-ssl3",
        "TLSv1.0": "-tls1",
        "TLSv1.1": "-tls1_1",
        "TLSv1.2": "-tls1_2",
        "TLSv1.3": "-tls1_3",
    }
    results = {}

    for protocol, option in protocols.items():
        try:
            # Construct and run the command
            command = f"echo | openssl s_client {option} -connect {url}:443"
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
            # If the command was successful, the protocol is supported
            results[protocol] = "Supported"
        except subprocess.CalledProcessError:
            # If the command fails, the protocol is not supported
            results[protocol] = "Not supported"

    return results

# Example usage:
url = "tls13.cloudflare.com"  # Use the domain part only, without the protocol
results = check_tls_support(url)
for protocol, status in results.items():
    print(f"{protocol}: {status}")
