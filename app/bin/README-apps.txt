The apps in this directory rely on a "gateway" Linux machine running a NAT. This machine has a network interface on the campus network, and a network interface on the external network (e.g., a FABRIC connection via a FACILITY PORT).

Before starting the portal start the NAT by running the script
     start-nft-nat
The administrator should modify this script to permit any persistent translations needed, while ensuring that campus resources are secure from malicious parties on the external network.

Applications in this directory control flows requested by an experimenter. 
To achieve this the application can perform many tasks, including 1) manipulating software-defined campus networks; 2) starting an application on a campus based source machine; 3) manipulating routing tables, 4) modifying NAT chains and rules; and many other possible tasks.

Example: The create-flow app performs this set of tasks:

--- Step a: create dnat on gateway machine ("nat") to map nat_port to destination_port on experimenter's target destination machine
    e.g., $APP_BIN/add-prerouting-dnat-rule $NAT_PORT $DESTINATION_ADDRESS $DESTINATION_PORT $PORT_TYPE

--- Step b: create host route on source machine
    e.g., APP_BIN/add-host-route-remote $SOURCE_ADDRESS $NAT_ADDRESS $SOURCE_INTFC $DESTINATION_ADDRESS

--- Step c: start application on source machine
    e.g., ssh USER@$SOURCE_ADDRESS $SOURCE_COMMAND $DESTINATION_ADDRESS $DESTINATION_PORT > /tmp/staas-app-log-$DESTINATION_ADDRESS-$DESTINATION_PORT.out 2> /tmp/staas/app-log-$DESTINATION_ADDRESS-$DESTINATION_PORT.err < /var/log/syslog
