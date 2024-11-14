#!/usr/bin/env python

# restore-policies.py

import pybsn
import argparse
import json
import controller_info

parser = argparse.ArgumentParser(description='Add a full policy')

PATH="controller"

parser.add_argument('path', type=str, default=PATH, nargs='?')
parser.add_argument('--host', '-H', type=str, default=HOST , help="Controller IP/Hostname to connect to")
parser.add_argument('--user', '-u', type=str, default=USER , help="Username")
parser.add_argument('--password', '-p', type=str, default=PASSWORD , help="Password")


args = parser.parse_args()

cntl = pybsn.connect(args.host, args.user, args.password)

'''
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
    'name': 'NEWjtb-hardwire-eth12-eth10',
    'policy-description': 'Connect jtb-dell-6515-1 interface 12 (200.5) to jtb-dell-6525-1 interface 10 (200.10)',
    'priority': 100,
    'replay': False,
    'rule': [{'any-traffic': True, 'sequence': 1}],
    'start-time': '2022-01-03T00:00:00-05:00'
})
'''

experimenter='NEW'
policyname=experimenter+'All_forward-eth6-eth15'
print("Created a new policy %s" % policyname)
dict={'start-time': '2022-01-11T00:00:00-05:00'}

cntl.root.applications.bigtap.policy.match(name=policyname).patch(dict)

current=cntl.root.applications.bigtap.policy.match(name=policyname)()
print(type (json.dumps(current, indent=4)))
print(json.dumps(current, indent=4))

'''
cntl.root.applications.bigtap.policy.match(name='NEWAll_forward-eth6-eth15').patch({
    'start-time': '2022-01-03T00:00:00-05:00'
})
'''

'''
cntl.root.applications.bigtap.policy.delete({
    'action': 'forward',
    'delivery-group': [{'bigtap-name': 'traffic-monitor'}],
    'delivery-mode': 'custom',
    'duration': 0,
    'expired-delivery-count': False,
    'expired-time': False,
    'filter-group': [{'bigtap-name': 'monitor_HPport_b7'}],
    'filter-mode': 'custom',
    'inactive': True,
    'managed-service': [{'name': 'masking-service',
        'optional': False,
        'sequence': 101,
        'use-service-delivery': False}],
    'name': 'NEWAll_forward-eth6-eth15',
    'policy-description': 'Forward TCP, UDP, ICMP: port 6->15 without masking-service',
    'priority': 100,
    'replay': False,
    'root-switch': '00:00:f0:d4:e2:43:d9:e7',
    'rule': [{'ether-type': 2048, 'ip-proto': 6, 'sequence': 1},
         {'ether-type': 2048, 'ip-proto': 17, 'sequence': 2},
         {'ether-type': 2048, 'ip-proto': 1, 'sequence': 3}],
    'start-time': '2022-01-11T16:55:27-05:00'
})
'''

'''
cntl.root.applications.bigtap.policy.put({
    'action': 'forward',
    'delivery-group': [{'bigtap-name': 'monitor-11'}],
    'delivery-mode': 'custom',
    'duration': 0,
    'expired-delivery-count': False,
    'expired-time': False,
    'filter-group': [{'bigtap-name': 'Mirror-5406-B5'}],
    'filter-mode': 'custom',
    'inactive': True,
    'name': 'TCP-UDP-ICMP-forward-5to11',
    'policy-description': 'Forward all TCP, UDP, ICMP traffic from eth5 to eth11',
    'priority': 110,
    'replay': False,
    'root-switch': '00:00:f0:d4:e2:43:d9:e7',
    'rule': [{'any-traffic': False, 'ether-type': 2048, 'ip-proto': 6, 'sequence': 1},
         {'any-traffic': False, 'ether-type': 2048, 'ip-proto': 17, 'sequence': 2},
         {'any-traffic': False, 'ether-type': 2048, 'ip-proto': 1, 'sequence': 3}],
    'start-time': '2021-10-18T13:55:15-04:00'
})

 {'action': 'forward',
  'delivery-group': [{'bigtap-name': 'traffic-monitor'}],
  'delivery-mode': 'custom',
  'duration': 0,
  'expired-delivery-count': False,
  'expired-time': False,
  'filter-group': [{'bigtap-name': 'Mirror-5406-B3'}],
  'filter-mode': 'custom',
  'inactive': True,
  'managed-service': [{'name': 'masking-service',
    'optional': False,
    'sequence': 101,
    'use-service-delivery': False}],
  'name': 'TCP-forward',
  'policy-description': 'Forward TCP, UDP, ICMP: port 7->15 without masking-service',
  'priority': 100,
  'replay': False,
  'root-switch': '00:00:f0:d4:e2:43:d9:e7',
  'rule': [{'ether-type': 2048, 'ip-proto': 6, 'sequence': 1},
   {'ether-type': 2048, 'ip-proto': 17, 'sequence': 2},
   {'ether-type': 2048, 'ip-proto': 1, 'sequence': 3}],
  'start-time': '2021-10-25T14:57:00-04:00'},
 {'action': 'forward',
  'delivery-group': [{'bigtap-name': 'monitor-11'}],
  'delivery-mode': 'custom',
  'duration': 0,
  'expired-delivery-count': False,
  'expired-time': False,
  'filter-group': [{'bigtap-name': 'Mirror-5406-B3'}],
  'filter-mode': 'custom',
  'inactive': False,
  'managed-service': [{'name': 'slicing-service',
    'optional': False,
    'sequence': 7,
    'use-service-delivery': False}],
  'name': 'TCP-forward_7_11',
  'policy-description': 'Forward TCP, UDP, ICMP: port 7->11 with masking-service',
  'priority': 100,
  'replay': False,
  'root-switch': '00:00:f0:d4:e2:43:d9:e7',
  'rule': [{'any-traffic': True, 'sequence': 4}],
  'start-time': '2022-05-03T12:09:00-04:00'},
 {'name': '_hardwire-eth12-eth10_o_hardwire-eth6-eth15'},
 {'action': 'forward',
  'delivery-group': [{'bigtap-name': 'eth10'}, {'bigtap-name': 'eth12'}],
  'delivery-mode': 'custom',
  'duration': 0,
  'expired-delivery-count': False,
  'expired-time': False,
  'filter-group': [{'bigtap-name': 'eth10'}, {'bigtap-name': 'eth12'}],
  'filter-mode': 'custom',
  'inactive': False,
  'name': 'hardwire-eth12-eth10',
  'policy-description': 'Connect jtb-dell-6515-1 interface 12 (200.5) to jtb-dell-6525-1 interface 10 (200.10)',
  'priority': 100,
  'replay': False,
  'rule': [{'any-traffic': True, 'sequence': 1}],
  'start-time': '2021-12-22T15:45:00-05:00'},
 {'action': 'forward',
  'delivery-group': [{'bigtap-name': 'eth35'}],
  'delivery-mode': 'custom',
  'duration': 0,
  'expired-delivery-count': False,
  'expired-time': False,
  'filter-group': [{'bigtap-name': 'eth53'}],
  'filter-mode': 'custom',
  'inactive': False,
  'name': 'hardwire-eth53-eth35',
  'priority': 100,
  'replay': False,
  'rule': [{'any-traffic': True, 'sequence': 1}],
  'start-time': '2022-05-16T18:52:05-04:00'},
 {'action': 'forward',
  'delivery-group': [{'bigtap-name': 'eth10'},
   {'bigtap-name': 'eth12'},
   {'bigtap-name': 'traffic-monitor'}],
  'delivery-mode': 'custom',
  'duration': 0,
  'expired-delivery-count': False,
  'expired-time': False,
  'filter-group': [{'bigtap-name': 'eth10'},
   {'bigtap-name': 'eth12'},
   {'bigtap-name': 'monitor_HPport_b7'}],
  'filter-mode': 'custom',
  'inactive': False,
  'name': 'hardwire-eth6-eth15',
  'policy-description': 'Connect jtb-dell-6515-1 interface 12 (200.5) to jtb-dell-6525-1 interface 10 (200.10)',
  'priority': 100,
  'replay': False,
  'rule': [{'any-traffic': True, 'sequence': 1}],
  'start-time': '2022-01-05T17:25:58-05:00'
})
'''
