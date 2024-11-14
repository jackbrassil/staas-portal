#!/usr/bin/env python
import pybsn
import argparse
import controller_info

parser = argparse.ArgumentParser(description='Add a full policy')

PATH="controller"

parser.add_argument('path', type=str, default=PATH, nargs='?')
parser.add_argument('--host', '-H', type=str, default=HOST , help="Controller IP/Hostname to connect to")
parser.add_argument('--user', '-u', type=str, default=USER , help="Username")
parser.add_argument('--password', '-p', type=str, default=PASSWORD , help="Password")

args = parser.parse_args()

cntl = pybsn.connect(args.host, args.user, args.password)
# this replaces a node by name. If no name, it adds it
cntl.root.applications.bigtap.policy.put({
    'action': 'forward',
    'delivery-group': [{'bigtap-name': 'eth10'}, {'bigtap-name': 'eth12'}],
    'delivery-mode': 'custom',
    'duration': 0,
    'expired-delivery-count': False,
    'expired-time': False,
    'filter-group': [{'bigtap-name': 'eth10'}, {'bigtap-name': 'eth12'}],
    'filter-mode': 'custom',
    'inactive': False,
    'name': 'ONE-jtb-hardwire-eth12-eth10',
    'policy-description': 'Connect jtb-dell-6515-1 interface 12 (200.5) to jtb-dell-6525-1 interface 10 (200.10)',
    'priority': 100,
    'replay': False,
    'rule': [{'any-traffic': True, 'sequence': 1}],
    'start-time': '2022-01-01T00:00:00-05:00'
})

# verify replacement of node
dict=cntl.root.applications.bigtap.policy.get({
    'name': 'ONE-jtb-hardwire-eth12-eth10',
})
print(dict)
