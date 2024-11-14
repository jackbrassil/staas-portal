Princeton Universtiy relies on an Arista Distributed Monitoring Framework (DMF)
-- formerly a Big Switch Network (BSN) -- to implement a campus-wide software-defined
network monitoring infrastructure.

For compatibility with the campus infrastructure, the STAAS project elected to build a
parallel experimental DMF. This would allow a successful prototype quick access to offered
traffic sources throughout the entire campus.

The tools in this directory are examples of functions that STAAS uses to control the
experimental campus monitoring network.

IF you create or reuse a DMF network on your campus, you might find these tools valuable.
To use them:

1. Clone "pybsn" (https://github.com/bigswitch/pybsn), an open source python interface to Arista/Big Switch network products:

    pip3 install pybsn

2. Modify the controller_info.py file to include the IP address and administrative credentials for your SDN controller:

    HOST="YOUR_CONTROLLER_IP_ADDRESS"
    USER="admin"
    PASSWORD="YOUR_CONTROLLER_PASSWORD"

3. Some tools include examples with controller-specific information (e.g., detailed policy descriptions) to serve as a
guide for your own implementation. Please replace any controller-specific information with your own.
