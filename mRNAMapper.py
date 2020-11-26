import collections
import requests
import sys
import os
import xml.etree.ElementTree as ET
import csv
from urllib.parse import quote
import time

headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15",
            "Access-Control-Origin": "*",
            "Access-Control-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type"
        }

def mapper(args):
    assert len(args) == 2, "Script must recieve 2 arguments <input_path> <output_path>"

    if not os.path.isfile(args[0]):
        print("Empty input file")
        exit(-1)
    
    input_path, output_path = args

    mRNA_list = []

    with open(input_path, newline='') as file:
        rows = csv.DictReader(file, delimiter=",")
        for row in rows:
            mRNA_list.append(row["ID_REF"])
        file.close()
    
    mRNA_ID_rows = []

    for mRNA in mRNA_list:
        print("fetching . . ." + mRNA)
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=" + mRNA + "+AND+\"Mus musculus\"[Organism]"
        print(url)
        req = requests.get(url, headers=headers)

        if req.status_code != requests.codes.ok:
            req.raise_for_status()
            exit(-1)
        
        root = ET.fromstring(req.content)

        try:
            ncbi_id = root.find("IdList").find("Id").text
        except AttributeError:
            print("NCBI ID not found!")
            ncbi_id = None
        
        if not ncbi_id:
            mRNA_ID_rows.append([mRNA, "None"])
        else:
            mRNA_ID_rows.append([mRNA, str(ncbi_id)])
        time.sleep(5)
    
    try:
        with open(output_path, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["ID_REF", "NCBI_ID"])
            writer.writerows(mRNA_ID_rows)
            file.close()
    except IOError:
        print("Error writing files")
        

if __name__ == "__main__":
    mapper(sys.argv[1:])