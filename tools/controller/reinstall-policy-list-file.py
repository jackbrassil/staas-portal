#!/usr/bin/env python
# This utility reads a text file which is the output of a *.policy.get()
# This output is a string representation of a list of policy dicts
# Each policy in the file is posted, overwriting any existing policies
# Use this to restore controller to previous policy state.

# post policies in text file (retrieved from earlier get())
import pybsn
import argparse
import pickle
import logging
import json
import sys
import ast
import controller_info
from pathlib import Path

POLICIES_DIR = "policies/"

parser = argparse.ArgumentParser(description='Read pickled policies')

parser.add_argument('--host', '-H', type=str, default=controller_info.HOST, help="Controller IP/Hostname to connect to")
parser.add_argument('--user', '-u', type=str, default=controller_info.USER, help="Username")
parser.add_argument('--password', '-p', type=str, default=controller_info.PASSWORD, help="Password")
parser.add_argument('--file', '-f', default="policies.txt", type=str, help="Policy file to read")

args = parser.parse_args()
policy = {}


# display all policies
def show_policies_all():
    dict = cntl.root.applications.bigtap.policy.get()
    print(dict)

def show_policies_all_pretty():
    dict = cntl.root.applications.bigtap.policy.get()
    print(json.dumps(dict, indent=4))

def show_policies_by_name():
    # get retuns policylist=[] list of policy={} dictionaries
    policylist = cntl.root.applications.bigtap.policy.get()
    for policy in policylist:
        value = policy['name']
        print(value)
        print(policy)
        print("\n")

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

try:
    cntl = pybsn.connect(args.host, args.user, args.password)

except Exception:
    logger.info("Controller connection failed - check IP address, Username and Password")
    exit(1)

print("\nDisplaying active policies\n")
show_policies_by_name()

policy_file = args.file
print("Policy file to load is %s\n" % policy_file)
policy_dict = {}  # policy to read from file

policy_list = []
# read list of text policy dicts from file retrieved by get()
f = open(POLICIES_DIR + policy_file, "r")
data = f.read()

policy_list = ast.literal_eval(data)
#close file
f.close()
 
for policy_dict in policy_list:
    try:
        cntl.root.applications.bigtap.policy.post(policy_dict)  # post() updates nodes, put() replaces all and just adds current policy
    except Exception:
        logger.info("Policy %s post unsuccessful - check if policy already exists" % policy_dict['name'])

print("\nUpdated active policies\n")
show_policies_by_name()
