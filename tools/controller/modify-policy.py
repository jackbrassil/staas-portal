#!/usr/bin/env python

# modify-policy.py  -- add/delete/change a single key/value for an existing policy
# Example: change policy start time
#     Usage: modify-policy.py -n Forward_Any_eth6_to_eth15 -k start-time -v 2022-06-18T13:55:15-04:00
# Example: inactivate a policy
#     Usage:  ./modify-policy.py -n L4slice-eth7-eth15 -k "inactive" -v "true"
# To run from terminal first manually activate venv:    staas-portal/venv/bin/source activate

import pybsn
import controller_info
import logging
import argparse
import json
import sys

parser = argparse.ArgumentParser(description='Add a full policy')
parser.add_argument('--host', '-H', type=str, default=controller_info.HOST , help="Controller IP/Hostname to connect to")
parser.add_argument('--user', '-u', type=str, default=controller_info.USER , help="Username")
parser.add_argument('--password', '-p', type=str, default=controller_info.PASSWORD , help="Password")

parser.add_argument('--policyname', '-n', type=str, default="Forward_Any_eth6_to_eth15" , help="Policy name")
parser.add_argument('--key', '-k', type=str, default='start-time' , help="Key")
parser.add_argument('--value', '-v', type=str, default='2022-08-01T00:00:00-00:00' , help="Value")
args = parser.parse_args()

# display all policies
def show_policies_all():
    dict=cntl.root.applications.bigtap.policy.get()
    print(json.dumps(dict, indent=4))

def show_policies_name():
    #get retuns policylist=[] list of policy={} dictionaries
    policylist=cntl.root.applications.bigtap.policy.get()
    for policy in policylist:
        value = policy['name']
        print(value)

def checkvalidpolicyname(label):
    policylist = cntl.root.applications.bigtap.policy.get()
    print(label)
    for policy in policylist:
        if (policy['name'] == label):
            print("Policy %s is valid" % policy['name'])
            return
    print("No matching policyname - provide valid policyname to modify")
    exit()


def config_logger():
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(  
           '%(asctime)s:%(levelname)s:%(name)s:%(module)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger = logging.getLogger('staas')
config_logger()

policyname=args.policyname
key=args.key
value=args.value

try:
    cntl = pybsn.connect(args.host, args.user, args.password)
except Exception:
    logger.info("Controller connection failed - check IP address, Username and Password")
    exit(1)

if (len(sys.argv) == 1):
    logger.info("Valid policyname required.")
    print("Active policies are:")
    show_policies_name()
    exit(1)

dict = {} 
dict[key] = value
print(key)
print(value)

#check if policy active
checkvalidpolicyname(policyname)

try:
    cntl.root.applications.bigtap.policy.match(name=policyname).patch(dict)
except Exception:
    logger.info('Policy update failed - check policyname, key and value')
    exit(1)

# display update policy only
def show_policy_updated():
    try:
        dict=cntl.root.applications.bigtap.policy.match(name=policyname)()
        print(json.dumps(dict, indent=4))
    except Exception:
        logger.info("Unable to display updated policy %" %policyname)
        #not clear how this would happen unless connection failed after update
        exit(1)

show_policy_updated()

