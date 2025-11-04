import requests
import py3Dmol
import sys # Good to add for error checking
import os

invoke_url = "https://health.api.nvidia.com/v1/biology/nvidia/esmfold"

# os.environ.get() safely reads the variable.
# It will return 'None' if the variable isn't found.
api_key = os.environ.get('NGC_API_KEY')


# Stop the script if the key is missing.
if not api_key:
    print("Error: The 'NGC_API_KEY' environment variable is not set.")
    print("Please set it before running the script.")
    print("Example (Linux/macOS): export NGC_API_KEY='your_api_key_here'")
    sys.exit(1) # Exit the script

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
}

payload = {
  "sequence": "MDILCEENTSLSSTTNSLMQLNDDTRLYSNDFNSGEANTSDAFNWTVDSENRTNLSCEGCLSPSCLSLLHLQEKNWSALLTAVVIILTIAGNILVIMAVSLEKKLQNATNYFLMSLAIADMLLGFLVMPVSMLTILYGYRWPLPSKLCAVWIYLDVLFSTASIMHLCAISLDRYVAIQNPIHHSRFNSRTKAFLKIIAVWTISVGISMPIPVFGLQDDSKVFKEGSCLLADDNFVLIGSFVSFFIPLTIMVITYFLTIKSLQKEATLCVSDLGTRAKLASFSFLPQSSLSSEKLFQRSIHREPGSYTGRRTMQSISNEQKACKVLGIVFFLFVVMWCPFFITNIMAVICKESCNEDVIGALLNVFVWIGYLSSAVNPLVYTLFNKTYRSAFSRYIQCQYKENKKPLQLILVNTIPALAYKSSQLQMGQKKNSKQDAKTTDNDCSMVALGKQHSEEASKDNSDGVNEKVSCV"
}

# re-use connections
session = requests.Session()

response = session.post(invoke_url, headers=headers, json=payload)

response.raise_for_status()
response_body = response.json()
#print(response_body)

print("API Response JSON Keys:")
print(response_body.keys())

pdb_string = response_body['pdbs'][0]

view = py3Dmol.view(width=600, height=400)
view.addModel(pdb_string, 'pdb')
view.setStyle({'cartoon': {'color': 'spectrum'}})
view.zoomTo()
view.show()
view.write_html()
