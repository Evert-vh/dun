import csv
import requests

# Define your Uptime Kuma URL and API key
kuma_url = 'http://10.0.3.227:3001/api'  # Replace with your actual server URL
api_key = 'uk1_MSaF_b7diwHbMhyprGW0Gl8seYr-uVWgVugaBKnR'  # Replace with your actual API key

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# Load existing monitors to map NVR names to their IDs
response = requests.get(f"{kuma_url}/monitors", headers=headers)
monitors = response.json()
nvr_to_id = {monitor['name']: monitor['id'] for monitor in monitors if monitor['type'] == 'group'}

# Function to add a new camera
def add_camera(name, ip, nvr_group):
    group_id = nvr_to_id.get(nvr_group)
    if not group_id:
        print(f"Group {nvr_group} not found.")
        return

    data = {
        "name": name,
        "url": f"ping://{ip}",
        "type": "ping",
        "parent": group_id,
    }
    response = requests.post(f"{kuma_url}/monitors", headers=headers, json=data)
    if response.status_code == 200:
        print(f"Successfully added {name}")
    else:
        print(f"Error adding {name}: {response.text}")

# Read cameras from CSV and add them
with open('cameras.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row if your CSV has one
    for row in reader:
        name, ip, nvr_group = row
        add_camera(name, ip, nvr_group)

