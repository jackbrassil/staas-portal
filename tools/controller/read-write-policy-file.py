#!/usr/bin/env python

#read-write-policy-file  saves and retrieves single pickled policy dict
import pybsn
import argparse
import pickle
import controller_info

POLICIES_DIR="policies/"

parser = argparse.ArgumentParser(description='Add a full policy')

parser.add_argument('--host', '-H', type=str, default=controller_info.HOST , help="Controller IP/Hostname to connect to")
parser.add_argument('--user', '-u', type=str, default=controller_info.USER , help="Username")
parser.add_argument('--password', '-p', type=str, default=controller_info.PASSWORD , help="Password")
parser.add_argument('--file', '-f', type=str, help="Policy file to add")    #no default filename, command line to override policy name

args = parser.parse_args()

#cntl = pybsn.connect(args.host, args.user, args.password)

policy_out = {}     #policy to save to file

policy_out={
    'action': 'forward',
    'delivery-group': [{'bigtap-name': 'eth10'}, {'bigtap-name': 'eth12'}],
    'delivery-mode': 'custom',
    'duration': 0,
    'expired-delivery-count': False,
    'expired-time': False,
    'filter-group': [{'bigtap-name': 'eth10'}, {'bigtap-name': 'eth12'}],
    'filter-mode': 'custom',
    'inactive': False,
    'name': 'TEST1-jtb-hardwire-eth12-eth10',
    'policy-description': 'Connect jtb-dell-6515-1 interface 12 (200.5) to jtb-dell-6525-1 interface 10 (200.10)',
    'priority': 100,
    'replay': False,
    'rule': [{'any-traffic': True, 'sequence': 1}],
    'start-time': '2022-04-01T00:00:00-05:00'
}


'''
###minimal policy template
basic_policy_template={
    'action': 'forward',
    'inactive': False,
    'name': 'MINIMUM_TEST_POLICY_TEMPLATE',
    'policy-description': 'Connect jtb-dell-6515-1 interface 12 (200.5) to jtb-dell-6525-1 interface 10 (200.10)',
    'priority': 100,
    'rule': [{'any-traffic': True, 'sequence': 1}],
    'start-time': '2022-04-01T00:00:00-05:00'
}
'''

if (args.file):
    filename = POLICIES_DIR + args.file
else:
    filename = POLICIES_DIR + str(policy_out['name']) + ".p"   #policy filename is policy name unless overridden on commandline

print("Policy file is %s" %filename)

with open(filename, 'wb') as handle:
    pickle.dump(policy_out, handle)
    handle.close()

policy_in = {}      #policy to read from file

with open(filename, 'rb') as handle:
    policy_in = pickle.load(handle)
    handle.close()




