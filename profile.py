"""
Basic Geni-lib example

Goal: Get Apache running via this scripting interface.

NB: Tried to get Docker container running on raw pc and connected to another raw pc. That isn't working and it actually seems easier to connect it to another docker container running on that pc.
"""


# import portal object

import geni.portal as portal
import geni.rspec.pg as rspec

import geni.rspec.emulab as emulab

# Create a Request Obect to start building the rspec
request = portal.context.makeRequestRSpec()

# Create LAN to put containers into
lan = request.LAN("lan")

# Add regular node for testing apache
host1 = request.RawPC("host1")
node1 = request.DockerContainer("node1") # Node running Apache in Container



host0 = request.RawPC("host0")
host0.hardware_type = "d430"
# Add a DockerContainer to the request
node0 = request.DockerContainer("node0") # Node running Apache in Container
node0.docker_extimage = "httpd:2.4"
node0.exclusive = True



iface1 = node0.addInterface("if1")
#iface1.component_id = "eth1"
#iface1.addAddress(rspec.IPv4Address("192.168.1.1", "255.255.255.0"))

iface2 = node1.addInterface("if1")
#iface2.component_id = "eth1"
#iface2.addAddress(rspec.IPv4Address("192.168.1.2", "255.255.255.0"))

lan.addInterface(iface1)

lan.addInterface(iface2)

# Add Docker Contaner to host
node0.InstantiateOn(host0.client_id)
node1.InstantiateOn(host1.client_id)

# Write the request in rspec format
node1.addService(rspec.Execute(shell="bash", command='sudo docker run -dit --name apache-app -p 8080:80 -v /local/repository/htdocs:/usr/local/apache2/htdocs/ httpd:2.4'))
portal.context.printRequestRSpec()
