import time
import dns.resolver
import requests
import subprocess
import socket
import maxminddb

class Scanner:
    def __init__(self,domain):

        self.scan_time = time.time()
        self.domain = domain
        self.IPv4s = self.get_IP_Addresses('A')
        self.IPv6s = self.get_IP_Addresses('AAAA')
        
        
        self.http_server = None
        self.insecure_http = False
        self.redirect_to_https = False
        self.hsts = False
        
        
        self.set_http_server_things()
        self.tls_versions =self.check_tls_support()    
        self.rdns_names = self.reverse_dns_lookup()
        self.geo_locations = self.get_geo_location()
        self.rca = self.get_root_ca()
        self.rtt_range = self.get_rtt_for_ips()
        

    def gen_dict(self):
        json_dict = {
            "scan_time": self.scan_time,
            "ipv4_addresses": self.IPv4s,
            "ipv6_addresses": self.IPv6s,
            "http_server": self.http_server,
            "insecure_http": self.insecure_http,
            "redirect_to_https": self.redirect_to_https,
            "hsts": self.hsts,
            "tls_versions": self.tls_versions,
            "rdns_names": self.rdns_names,
            "geo_locations": self.geo_locations,
            "root_ca": self.rca,
            "rtt_range": self.rtt_range
        }
        return json_dict
        
    def reverse_dns_lookup(self):
        ip_addresses = self.IPv4s
        
        dns_list = []
        for ip in ip_addresses:
            try:
                # Perform the reverse DNS lookup and get the first result
                hostname, _, _ = socket.gethostbyaddr(ip)
                print(f"IP Address: {ip} -> Hostname: {hostname}")
                dns_list.append(hostname)
                
            except socket.herror as e:
                # Handle errors (e.g., no host name found for the IP address)
                print(f"IP Address: {ip} -> Error: {e}")
        
        return dns_list
                
                
    #return a list of ip address, record type can be A or AAAA
    def get_IP_Addresses(self, record_type :str):
        list_of_ips = []
        try:
            result = dns.resolver.resolve(self.domain, record_type)
            for ipval in result:
                list_of_ips.append(ipval.to_text())
        except dns.resolver.NoAnswer:
            print(f"No record exists for {self.domain}.")
        except Exception as e:
            print(f"Error occurred: {e}")
        print(list_of_ips)
        return list_of_ips

    #return the headers of some http header value using a get request
    def set_http_server_things(self):
        self.http_server = None
        self.insecure_http = False
        self.redirect_to_https = False
        self.hsts = False

        try:
            
            ###MAKE SURE WITH TA IS IS FINE
            url = "http://" + self.domain
            response = requests.get(url, timeout=5)
            
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"   
        
        self.insecure_http = True
        
        if 'Server' in response.headers:
            self.http_server = response.headers.get('Server','Server information not found')
        
        if response.history:
            print("Request was redirected.")
            for resp in response.history:
                print(f"Redirected from {resp.url} to {response.url}")
                if "http://" in resp.url and "https://" in response.url:
                    self.redirect_to_https = True
                    break
        
        
        if 'Strict-Transport-Security' in response.headers:
            self.hsts = True
    
    def check_tls_support(self):
        url = self.domain
        protocols = {
            "SSLv2": "-ssl2",
            "SSLv3": "-ssl3",
            "TLSv1.0": "-tls1",
            "TLSv1.1": "-tls1_1",
            "TLSv1.2": "-tls1_2",
            "TLSv1.3": "-tls1_3",
        }
        results = []

        for protocol, option in protocols.items():
            try:
                # Construct and run the command
                command = f"echo | openssl s_client {option} -connect {url}:443"
                result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                
                # If the command was successful, the protocol is supported
                results.append(protocol)
            except subprocess.CalledProcessError:
                # If the command fails, the protocol is not supported
                print("not supported")
                pass

        return results
    
    def get_root_ca(self):
        try:
            command = f"echo | openssl s_client -connect {self.domain}:443"
            result = subprocess.run(command, check=True, shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
            certificate_chain = str(result).split("---")[1]

            bottom_row = certificate_chain.split("\\n")
            print(bottom_row)

            
            
            comma_list = bottom_row[-2].split(',')
            
            root_ca = ""
            for chunk in comma_list:
                if ' O = ' in chunk:
                    root_ca = chunk[len(' O = '):]
                elif 'i:O = ' in chunk:
                    root_ca = chunk[len('i:O = '):]
                    
            
            
            #print(match.group(1))

            #root_ca = bottom_row.split("0 = ")[1]
            
            print("root_ca: ", root_ca)

            return root_ca
            
        except subprocess.CalledProcessError:
            print("error, could not find ca")
            return None


        
    
    def get_rtt_for_ips(self):
        def get_rtt(host, port):
            try:
                command = f"sh -c \"time echo -e '\x1dclose\x0d' | telnet {host} {port}\""
                result = str(subprocess.run(command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout)
                # print(result)
                rtt = result.split("real\\t")[1][2:7]
                # print(rtt)
                return float(rtt)

                    
            except subprocess.CalledProcessError as e:
                print("process error, could not get rtt")
                return None
        rtt_list = []
        common_ports = [80, 22, 443]

        if not self.IPv4s:
            return None
            
        for ip in self.IPv4s:
            for port in common_ports:
                rtt = get_rtt(ip,common_ports)
                if rtt is not None:
                    rtt_list.append(rtt)
                    #only need one to work
                    break

            print(rtt_list)

        if rtt_list:
            return [min(rtt_list)*1000,max(rtt_list)*1000]

        else:
            return None

    def get_geo_location(self):
        locations = []
        
        addy_list = []
        for ip in self.IPv4s:
            with maxminddb.open_database('GeoLite2-City.mmdb') as reader:
                res = reader.get(ip)
                if "country" in res:
                    locations.append(res["country"]["names"]["en"])
                if  'subdivisions' in res:
                    locations.append(res["subdivisions"][0]["names"]['en'])
                if  'city' in res:
                    locations.append(res["city"]["names"]['en'])
                
                addy_list.append(f','.join(locations))
        
        return addy_list



            

