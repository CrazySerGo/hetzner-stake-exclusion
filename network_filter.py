import ipaddress
import csv
import subprocess
import json

netmasks = []
gossip = json.loads(subprocess.check_output("solana -ut gossip --output json", shell=True))

with open('hetz1.json') as user_file:
    file_contents = user_file.read()
dim_hetzner_list = json.loads(file_contents)

with open('range.csv', newline='') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        netmasks.append(row[0])

identity_list_in_gossip = []
for node in gossip:
    nodeIp = node['ipAddress']
    isInHetzner = False
    for mask in netmasks:
        isInHetzner = ipaddress.ip_address(nodeIp) in ipaddress.ip_network(mask)
    if not isInHetzner:
        identity_list_in_gossip.append(node['identityPubkey'])

destakable_nodes = []
for hetzner_node in dim_hetzner_list:
    if hetzner_node['identity'] not in identity_list_in_gossip:
        destakable_nodes.append(hetzner_node['vote'])

solana_ledger_tool_cmd = "solana-ledger-tool --ledger <ledger path> create-snapshot 160991175 <ledger path> --hard-fork 160991175 \ \n"
for destakable_node in destakable_nodes:
    solana_ledger_tool_cmd += "--destake-vote-account " + destakable_node + " \ \n"

print(solana_ledger_tool_cmd)

