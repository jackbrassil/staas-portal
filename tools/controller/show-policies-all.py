#!/usr/bin/env python
import os

import pybsn
import argparse
import json
import controller_info
import logging, sys

parser = argparse.ArgumentParser()
parser.add_argument('--host', '-H', type=str, default=controller_info.HOST , help="Controller IP/Hostname to connect to")
parser.add_argument('--user', '-u', type=str, default=controller_info.USER , help="Username")
parser.add_argument('--password', '-p', type=str, default=controller_info.PASSWORD , help="Password")
args = parser.parse_args()

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

try:
    print(args.host, args.user, args.password)
    print(os.getcwd(), sys.path)
    cntl = pybsn.connect(args.host, args.user, args.password)
except Exception:
    logger.info("Controller connection failed - check IP address, Username and Password")
    exit(1)

def show_policies_all():
    #get retuns policylist=[] list of policy={} dictionaries
    policylist=cntl.root.applications.bigtap.policy.get()
    for policy in policylist:
        value = policy['name']
        print("\n" + value)
        print(policy)
        #print(json.dumps(policy, indent=2)) #prettier output

show_policies_all()
exit()
