from texttable import Texttable
import json
import sys
def main():
    if len(sys.argv) != 3:
        print("Usage: python3 report.py [input_file.json] [output_file.txt]")
        sys.exit(1)  # Exit the script with an error code

    # Extract arguments
    inputfile_location = sys.argv[1]
    outputfile_location = sys.argv[2]
    
    
    input_str = ""
    with open(inputfile_location, 'r') as file:
        input_str = file.read()
    
    data_source = json.loads(input_str)
    
    column_len = len('redirect_to_https')
    output_str = ""
    
    output_str += "\n###1. A textual or tabular listing of all the information returned in Part 2, with a section for each domain.###\n"
    for domain,domain_data in data_source.items():
        table = Texttable()
        
        domain_data['domain'] = domain
        table.header(domain_data.keys())
        
        table.set_cols_width(len(domain_data.keys()) * [column_len]) 
        row = []
        for param in domain_data.keys():
            row.append(str(domain_data[param]))
        table.add_row(row)
        output_str += table.draw()
        output_str += '\n'
        
    
    
    
    list_of_min_rtt_minmax_domain = []
    for domain,domain_data in data_source.items():
        
        rtt_range=domain_data["rtt_range"]
        
        #[min, [min_max] , domain]
        new_list = [domain_data["rtt_range"][0],domain_data["rtt_range"],domain]
        list_of_min_rtt_minmax_domain.append(new_list)
    
    sorted_list = sorted(list_of_min_rtt_minmax_domain, key=lambda x: x[0])
    output_str += ("\n###2. A table showing the RTT ranges for all domains, sorted by the minimum RTT (ordered from fastest to slowest)###\n")
    
    rtt_table = Texttable()
    rtt_table.header(['domain','rtt_range'])
    for item in sorted_list:
        rtt_table.add_row([item[2],str(item[1])])
    
    output_str += (rtt_table.draw())

    output_str +=("\n###3. A table showing the number of occurrences for each observed root certificate authority (from Part 2i), sorted from most popular to least.###\n")
    
    ca_dict = {}
    for domain,domain_data in data_source.items():
        if domain_data["root_ca"] not in ca_dict:
            ca_dict[domain_data["root_ca"]] = 1
        else:
            ca_dict[domain_data["root_ca"]] += 1
    
    sorted_list = sorted(list(ca_dict.items()), key=lambda x: x[1])[::-1]
    
    ca_table = Texttable()
    ca_table.header(['Certificate Authority','Count'])
    for item in sorted_list:
        ca_table.add_row([item[1],item[0]])
    
    
    output_str += ca_table.draw()
    
    http_dict = {}
    output_str +=("\n###4.A table showing the number of occurrences of each web server (from Part 2d), ordered from most popular to least.###\n")
    for domain,domain_data in data_source.items():
        if domain_data["http_server"] not in http_dict:
            http_dict[domain_data["http_server"]] = 1
        else:
            http_dict[domain_data["http_server"]] += 1
    
    http_table = Texttable()
    http_table.header(['HTTP Server','Count'])
    sorted_list = sorted(list(http_dict.items()), key=lambda x: x[1])[::-1]
    for item in sorted_list:
        http_table.add_row([item[1],item[0]])
    
    output_str += http_table.draw()
    
    output_str +=('\n###5.A table showing the percentage of scanned domains supporting: each version of TLS listed in Part 2h. I expect to see close to zero percent for SSLv2 and SSLv3. "plain http" (Part 2e) "https redirect" (Part 2f) "hsts" (Part 2g) "ipv6" (from Part 2c)###\n')
    
    percentage_dict = {}
    protocols = [
            "SSLv2",
            "SSLv3",
            "TLSv1.0",
            "TLSv1.1",
            "TLSv1.2",
            "TLSv1.3"
    ]
    for protocol in protocols:
        percentage_dict[protocol] = 0
        
    percentage_dict['plain_http_count'] = 0
    percentage_dict['redirect_https_count'] = 0
    percentage_dict['hsts_count'] = 0
    percentage_dict['ipv6_count'] = 0
        
    
    for domain,domain_data in data_source.items():
        for tls_version in domain_data['tls_versions']:
            percentage_dict[tls_version] += 1
    
    for domain,domain_data in data_source.items():
        if domain_data['insecure_http'] == True:
            percentage_dict['plain_http_count'] += 1
        if domain_data['redirect_to_https'] == True:
            percentage_dict['redirect_https_count'] += 1
        if domain_data['hsts'] == True:
            percentage_dict['hsts_count'] += 1
        if len(domain_data['ipv6_addresses']) > 0:
            percentage_dict['ipv6_count'] += 1
    
    for item in percentage_dict.keys():
        percentage_dict[item] =  str(( percentage_dict[item] / len(data_source) ) * 100) + "%"
            
    support_table = Texttable()
    support_table.header(protocols + ['plain http','redirect https','hsts','ipv6'])
    support_table.set_cols_width(len(percentage_dict) * [column_len]) 
    support_table.add_row(percentage_dict.values())
    output_str += (support_table.draw())
    
    with open(outputfile_location,'w') as file:
        file.write(output_str)
        
        
if __name__ == "__main__":
    main()
    