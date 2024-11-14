To show STAAS generating/redirecting traffic originating on campus and injecting
it into a FABRIC sliver, we demonstrate a minimal 3 node network.

The FABRIC sliver is created with publicly available Jupyter Notebook

	facility_port_PRIN_2local.ipyn

The sliver relies on the use of a FACILITY PORT (FP) to connect a STAAS system on campus.
A FABRIC network (e.g., IPv4Network) is assigned 10.20.0.0/24 to connect the sliver
to campus-side resources.
VLAN 2000 is used for the FP. A single FABRIC VM destination "node1" (10.20.0.101) is created.
The FP terminates on a campus-side ethernet switch assigned 10.20.0.2.

A campus-side node "staas-620-3" is connected to the boundary ethernet switch and servers as a NAT. The node is assigned a sliver IP address 10.20.0.3 (on interface "enp5s0f0np0")
and an internal campus private IP address 10.43.214.45 (on interface "enp5s0f1np1").

Other campus-side nodes serve as traffic sources. While these nodes might reside on the internal
10.43.214.0/24 private network, they can reside anywhere on campus. Nodes are dynamically
connected to the NAT over an SDN network (Arista DMZ). While the SDN controller is a private campus resource, a node on the FABRIC sliver can request to initiate/terminate a traffic source through the STAAS traffic portal, which can be visible to web browsers running on nodes inside the FABRIC sliver.

The address of the remote traffic target is known as
IP_REMOTE="10.20.0.101"

The NAT node1 receives traffic originating on campus and received on its Input InterFace (IIF)
NAT_IIF="enp5s0f1np1"
and transmitted over its Output InterFace (0IF)
NAT_OIF="enp5s0f0np0"
Traffic directed to the target FABRIC destination node1 is assigned the source IP address 10.20.0.3
(NAT's outbound address on the sliver) regardless of its source on the internal campus network.

In general, no Destination NAT (DNAT) service is provided; incoming connections to private campus nodes from external nodes on the FABRIC sliver are rejected.

Traffic generated on campus must be explicitly offered by local administrators to be directed to
the FABRIC network. If offered, that traffic can be initiated/terminated by Experimenters
on the FABRIC sliver. However, the details of internal campus network operations (e.g., how and from where the traffic originates) are opaque to FABRIC experimenters, unless explicitly shared as Offered Flow metadata on the STAAS portal.
