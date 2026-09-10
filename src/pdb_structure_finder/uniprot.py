from pathlib import Path
import httpx
import json
import pandas as pd

url = "https://rest.uniprot.org/uniprotkb/P00450.json"
response = httpx.get(url)
print(response)
if response.status_code == 200:
    content = response.json()

# condensed requests
PDB_infos = [elem for elem in content["uniProtKBCrossReferences"] if elem["database"] == "PDB"]
print("one row database scraped")
print(PDB_infos[0]["properties"])

report = []

for info in PDB_infos:
    uniprot_id = "P00450"
    database_id = info["id"]
    method = [x["value"] for x in info["properties"] if x["key"] == "Method"][0]
    resolution = [x["value"] for x in info["properties"] if x["key"] == "Resolution"][0]
    chain = [x["value"] for x in info["properties"] if x["key"] == "Chains"][0]

    report.append({
        "uniprot_id": uniprot_id,
        "database": "PDB",
        "database_id": database_id,
        "method": method,
        "resolution": resolution,
        "chain": chain,
    })

df = pd.DataFrame(report)
print(df)

# Try to use PDB API for getting the sctructures
# Still try with P00450
pdb_code = df["database_id"].iloc[0]
url_pdb = f"https://files.rcsb.org/download/{pdb_code}.cif"
response_pdb = httpx.get(url_pdb)
print(response_pdb)
if response_pdb.status_code == 200:
    content_pdb = response_pdb.text

# save cif file
from pathlib import Path
DEST_FOLDER = Path(f"../../tests")
with open(f"{DEST_FOLDER}/{pdb_code}.cif", "w") as k:
    k.write(content_pdb)

# check non-polymer entity
# Using GraphQL
import requests
url_graph = "https://data.rcsb.org/graphql"
query = """
    query GetEntry($pdb_id: String!) {
        entry(entry_id: $pdb_id) {
            rcsb_id
            nonpolymer_entities {
                rcsb_id
                rcsb_nonpolymer_entity_container_identifiers {
                    entry_id
                    entity_id
                    auth_asym_ids
                    asym_ids
                    nonpolymer_comp_id
                }
                nonpolymer_comp {
                    chem_comp {
                        id
                        formula_weight
                        name
                        formula
                    }
                }
            }
        } 
    }
"""
variables = {
        "pdb_id": pdb_code
}
response_graph = requests.post(
        url_graph,
        json={
            "query":query,
            "variables": variables
        }
)

data = response_graph.json()
print(data)
url_non_polymer = "https://data.rcsb.org/rest/v1/core/nonpolymer_entity/{pdb_code}/1"
response_non_polymer = httpx.get(url_non_polymer)
print(response_non_polymer)
if response_non_polymer.status_code == 200:
    content_non_polymer = response_non_polymer.json()
    print(content_non_polymer)
