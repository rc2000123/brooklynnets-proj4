from Scanner import Scanner
import sys
import json
import concurrent.futures

def scan(domain):
    myscan = Scanner(domain)
    return [domain, myscan.gen_dict()]

def main():
    # Check if the number of arguments is correct (including the script name)
    if len(sys.argv) != 3:
        print("Usage: python3 scan.py [input_file.txt] [output_file.json]")
        sys.exit(1)  # Exit the script with an error code

    # Extract arguments
    inputfile_location = sys.argv[1]
    outjson_location = sys.argv[2]
    
    web_domain_list = []
    # Open the file in read mode ('r')
    with open(inputfile_location, 'r') as file:
        # Iterate over each line in the file
        for line in file:
            # Process the line (in this example, we'll just print it)
            web_domain_list.append(line.strip()) # Using strip() to remove leading/trailing whitespace, including newlines

    print(web_domain_list)
    domain_dict = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for domain in web_domain_list:
            futures.append(executor.submit(scan, domain))
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            domain_dict[result[0]] = result[1]

    with open(outjson_location, "w") as f:
        json.dump(domain_dict, f, sort_keys=True, indent=4)
    

if __name__ == "__main__":
    main()


"""result = subprocess.check_output(["nslookup", "northwestern.edu", "8.8.8.8"],
      timeout=2, stderr=subprocess.STDOUT).decode("utf-8")
print(result)"""