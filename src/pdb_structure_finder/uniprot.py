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