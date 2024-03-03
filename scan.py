from Scanner import Scanner
import sys
import json

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
    for domain in web_domain_list:
        
        
        myscan = Scanner(domain)
        domain_dict[domain] = myscan.gen_dict()
    
    
    with open(outjson_location, "w") as f:
        json.dump(domain_dict, f, sort_keys=True, indent=4)
    

if __name__ == "__main__":
    main()


"""result = subprocess.check_output(["nslookup", "northwestern.edu", "8.8.8.8"],
      timeout=2, stderr=subprocess.STDOUT).decode("utf-8")
print(result)"""