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
    
    
    for domain,domain_data in data_source.items():
        table = Texttable()
        table.header(domain_data.keys())
        for param in domain_data.keys():
            domain_data[param] = str(domain_data[param])
        table.add_row(domain_data.values())
        print(table.draw())
    
if __name__ == "__main__":
    main()
    