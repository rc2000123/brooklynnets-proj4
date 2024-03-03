import requests

def get_http_server(url):
    try:
        response = requests.get(url)
        # Check if the 'Server' header exists in the response
        print(response)
        print(response.headers)
        server = response.headers.get('Server', 'Server information not found')
        return server
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# Example usage
url = "http://example.com"  # Replace this URL with the one you're interested in
server_info = get_http_server(url)
print(f"The HTTP server for {url} is: {server_info}")
