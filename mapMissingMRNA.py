import requests
from bs4 import BeautifulSoup
import csv
import os
import sys

headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15",
            "Access-Control-Origin": "*",
            "Access-Control-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type"
        }

def extract_mrna(id_ref):
    url = "https://www.ncbi.nlm.nih.gov/nuccore/" + id_ref 
    req = requests.get(url, headers=headers)

    if req.status_code != requests.codes.ok:
        req.raise_for_status()
        exit(-1)
    
    bsObj = BeautifulSoup(req.content, "html.parser")
    links = bsObj.findAll("a")
    
    for link in links:
        print(link)
        content = link.string
        if content[:2] == "NM":
            print(content)

def main(args):
    input_csv, output_csv = args

    if not os.path.isfile(input_csv):
        print("Empty input file")
        exit(-1)
    
    id_refs = []

    with open(input_csv, newline='') as file:
        rows = csv.DictReader(file, delimiter=",")
        for row in rows:
            id_refs.append(row["ID_REF"])
        file.close()
    
    for index, id_ref in enumerate(id_refs):
        if id_ref[:2] == "NM":
            continue
        print(id_ref)
        extract_mrna(id_ref)

if __name__ == "__main__":
    main(sys.argv[1:])