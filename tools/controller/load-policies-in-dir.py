#!/usr/bin/env python

# read-write-policy-file retrieves all pickled policies in directory
import pybsn
import argparse
import pickle
import logging
import json
import sys
import controller_info
from pathlib import Path

POLICIES_DIR = "policies/"

parser = argparse.ArgumentParser(description='Read pickled policies')

parser.add_argument('--host', '-H', type=str, default=controller_info.HOST, help="Controller IP/Hostname to connect to")
parser.add_argument('--user', '-u', type=str, default=controller_info.USER, help="Username")
parser.add_argument('--password', '-p', type=str, default=controller_info.PASSWORD, help="Password")
parser.add_argument('--directory', '-d', default=POLICIES_DIR, type=str,
                    help="Policy dir to read")  # no default filename, command line to override policy name

args = parser.parse_args()
policy = {}


# display all policies
def show_policies_all():
    dict = cntl.root.applications.bigtap.policy.get()
    print(dict)

def show_policies_all_pretty():
    dict = cntl.root.applications.bigtap.policy.get()
    print(json.dumps(dict, indent=4))

def show_policies_name():
    # get retuns policylist=[] list of policy={} dictionaries
    policylist = cntl.root.applications.bigtap.policy.get()
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

try:
    cntl = pybsn.connect(args.host, args.user, args.password)
    print("Displaying active policies")
    show_policies_all()
except Exception:
    logger.info("Controller connection failed - check IP address, Username and Password")
    exit(1)

dir = args.directory
print("Policy directory is %s" % dir)
policy_in = {}  # policy to read from file

# read all pickled policies (*.p) in directory or in directory tree '**/*.p'
for p in Path(POLICIES_DIR).glob('*.p'):
    print("Reading file %s" % p.name)
    with open(POLICIES_DIR + p.name, 'rb') as handle:
        policy_in = pickle.load(handle)
        print(str(policy_in))  # replace with controller post() to create policy
        try:
            cntl.root.applications.bigtap.policy.post(policy_in)
            #cntl.root.applications.bigtap.policy.get()
        except Exception:
            logger.info("Policy update failed - check policyname, key and value")

        handle.close()

