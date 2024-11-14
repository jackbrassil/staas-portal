The staas-portal project has been tested under Ubuntu 20.04 LTS and Ubuntu 22.04 LTS.
Other systems supporting nfttables shold work as well.

A minimal hardware configuration is discussed in README-deployment.txt

a. Clone the staas-portal github project

b. Install:
    sudo apt install -y python3-pip
    sudo apt install -y python3-venv
    optional: sudo apt install -y build-essential libssl-dev libffi-dev python3-dev

c. Create a python virtual environment. You might wish to create a virtual-environments directory to store the new venv you will build

        cd virtual-environments

    Create a virtual environment called staas-venv on target with

        python3 -m venv staas-venv

    Activate the staas-venv virtual environment

        source staas-venv/bin/activate

d. Return to the staas-portal project directory

e. Install dependencies

        pip3 install -r ./requirements.txt


f. Ensure that your hardware configuration is consistent with

        README-deployment.txt

g. On the NAT "gateway" machine run

        bin/start-nft-nat

To run the staas-portal web server:


      python3 staas_site.py


If you encounter errors such as
AttributeError: module 'collections' has no attribute 'MutableMapping'
Change all instances of "collections" imported in this file to use "collections.abc"
  /home/jtb/Desktop/code/virtual-environments/staas-venv/lib/python3.10/site-packages/jinja2/tests.py
  /home/jtb/Desktop/code/virtual-environments/staas-venv/lib/python3.10/site-packages/flask/sessions.py
  /home/jtb/Desktop/code/virtual-environments/staas-venv/lib/python3.10/site-packages/sqlalchemy/sql/base.py 
  /home/jtb/Desktop/code/virtual-environments/staas-venv/lib/python3.10/site-packages/sqlalchemy/sql/base.py 
  /home/jtb/Desktop/code/virtual-environments/staas-venv/lib/python3.10/site-packages/sqlalchemy/util/_collections.py

h. If you elect to use the existing database staas.db there are two existing registered accounts:

i. Create Users and Administrators

Name 		Role    Usernamei		Password
Frank Furter    User	frank@furter.com	frank
Jack Brassil    Admin	jbrassil@princeton.edu	jack

You can restrict those eligible to become Administrators as you please.
In the current implementation any @princeton.edu email address (unauthenticated) can serve as an Administrator

To modify this change the Flask /register decorator in staas_site.py from the following:

    if '@princeton.edu' in form.email.data:
               user.is_admin = True


You can also delete the staas.db file, register your own Users and Administrators, and create your own flows.
