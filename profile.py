"""
Basic Geni-lib example

Goal: Get Apache running via this scripting interface.
"""


# import portal object

import geni.portal as portal
import geni.rspec.pg as rspec

import geni.rspec.emulab as emulab
# Create a Request Obect to start building the rspec
request = portal.context.makeRequestRSpec()

host = request.RawPC("host")
host.hardware_type = "d430"

# Add a DockerContainer to the request
node0 = request.DockerContainer("node0") # Node running Apache in Container
node0.docker_extimage = "apache:2.4"
node0.exclusive = True

# Add Docker Contaner to host
node0.InstantiateOn(host.client_id)

# Add regular node for testing apache
node1 = request.RawPC("node1")


# Create Link Between Them
link1 = request.Link(members = [host, node1])

# Write the request in rspec format
node1.addService(rspec.Execute(shell="bash", command='sudo docker run -dit --name apache-app -p 8080:80 -v /local/repository/htdocs:/usr/local/apache2/htdocs/ httpd:2.4'))
portal.context.printRequestRSpec()
