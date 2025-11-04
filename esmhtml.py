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

session = requests.Session()
response = session.post(invoke_url, headers=headers, json=payload)

try:
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
    print(f"Response content: {response.text}")
    sys.exit(1)

response_body = response.json()

# --- FIX 1: Get the first PDB string from the 'pdbs' list ---
try:
    pdb_string = response_body['pdbs'][0]
except (KeyError, IndexError, TypeError):
    print("Error: 'pdbs' key not found or is empty in API response.")
    print(f"API Response Keys: {response_body.keys()}")
    sys.exit(1)

# --- FIX 2: Save to HTML instead of trying to 'show' ---
view = py3Dmol.view(width=600, height=400)

# Use the 'pdb' format type
view.addModel(pdb_string, 'pdb')

view.setStyle({'cartoon': {'color': 'spectrum'}})
view.zoomTo()

# Save the interactive viewer to an HTML file
output_filename = "protein.html"
view.write_html(output_filename)

print(f"Successfully generated 3D model. Open '{output_filename}' in your browser to view.")
