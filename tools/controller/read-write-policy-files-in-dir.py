#!/usr/bin/env python

#read-write-policy-file retrieves all pickled policies in directory
import pybsn
import argparse
import pickle
import controller_info
from pathlib import Path

POLICIES_DIR="policies/"

parser = argparse.ArgumentParser(description='Read pickled policies')

parser.add_argument('--host', '-H', type=str, default=controller_info.HOST , help="Controller IP/Hostname to connect to")
parser.add_argument('--user', '-u', type=str, default=controller_info.USER , help="Username")
parser.add_argument('--password', '-p', type=str, default=controller_info.PASSWORD , help="Password")
parser.add_argument('--directory', '-d', default=POLICIES_DIR, type=str, help="Policy dir to read")    #no default filename, command line to override policy name

args = parser.parse_args()

#cntl = pybsn.connect(args.host, args.user, args.password)

dir = args.directory
print("Policy directory is %s" %dir)
policy_in = {}      #policy to read from file


#read all pickled policies (*.p) in directory or in directory tree '**/*.p'
for p in Path(POLICIES_DIR).glob('*.p'):
    print("Reading file %s" %p.name)
    with open(POLICIES_DIR+p.name, 'rb') as handle:
        policy_in = pickle.load(handle)
        print(str(policy_in))   #replace with controller post() to create policy
        handle.close()

exit()




