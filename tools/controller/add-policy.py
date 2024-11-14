#!/usr/bin/env python
import pybsn
import argparse
import json
import controller_info

parser = argparse.ArgumentParser()

parser.add_argument('--host', '-H', type=str, default=HOST , help="Controller hostname or IP address")
parser.add_argument('--user', '-u', type=str, default=USER , help="Username")
parser.add_argument('--password', '-p', type=str, default=PASSWORD , help="Password")

args = parser.parse_args()

cntl = pybsn.connect(args.host, args.user, args.password)
# this replaces a node by name. If no name, it adds it

# Example of a policy_dict
policy_dict={
    'action': 'forward',
    'delivery-group': [{'bigtap-name': 'eth10'}, {'bigtap-name': 'eth12'}],
    'delivery-mode': 'custom',
    'duration': 0,
    'expired-delivery-count': False,
    'expired-time': False,
    'filter-group': [{'bigtap-name': 'eth10'}, {'bigtap-name': 'eth12'}],
    'filter-mode': 'custom',
    'inactive': False,
    'name': 'FOUR-jtb-hardwire-eth12-eth10',
    'policy-description': 'Connect jtb-dell-6515-1 interface 12 (200.5) to jtb-dell-6525-1 interface 10 (200.10)',
    'priority': 100,
    'replay': False,
    'rule': [{'any-traffic': True, 'sequence': 1}],
    'start-time': '2022-04-01T00:00:00-05:00'
}

cntl.root.applications.bigtap.policy.post(policy_dict)

# verify addition of node
def show_policies_all():
    dict=cntl.root.applications.bigtap.policy.get()
    print(json.dumps(dict, indent=4))

show_policies_all()
