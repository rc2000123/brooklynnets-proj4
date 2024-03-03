import dns.resolver

# The domain you want to get the IPv6 address for
domain = 'twitter.com'

try:
    # Query for AAAA records
    result = dns.resolver.resolve(domain, 'AAAA')
    for ipval in result:
        print('IPv6 address:', ipval.to_text())
except dns.resolver.NoAnswer:
    print(f"No AAAA record exists for {domain}.")
except Exception as e:
    print(f"Error occurred: {e}")


try:
    # Query for AAAA records
    result = dns.resolver.resolve(domain, 'A')
    for ipval in result:
        print('IPv4 address:', ipval.to_text())
except dns.resolver.NoAnswer:
    print(f"No A record exists for {domain}.")
except Exception as e:
    print(f"Error occurred: {e}")

