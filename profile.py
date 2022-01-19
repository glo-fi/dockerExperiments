"""
General script for spawning nodes and containers
"""


import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.emulab as emulab
import geni.rspec.igext as igext

# Define constants here




# Create Portal Context

pc = portal.Context()

# Build Request Object for RSpec
request = pc.makeRequestRSpec()

# Define, Build and Verify Parameters

pc.defineParameter('node_count', 'Number of nodes', portal.ParameterType.INTEGER, 2)
pc.defineParameter('create_lan', 'Create Vertual LAN', portal.ParameterType.BOOLEAN, 'True')

params = pc.bindParameters()
pc.verifyParameters()

if params.create_lan:
    if params.node_count > 1:
        if params.node_count == 2:
            lan = request.Link()
        else:
            lan.request.LAN()

def run_install_script(node, script):
    node.addService(pg.Execute(shell='bash', command='chmod +x /local/repository/install/' + script))
    node.addService(pg.Execute(shell='bash', command='/local/repository/install/' + script))


for i in range(params.node_count):
    node = request.RawPC('node' + str(i))

    if params.create_lan:
        if params.node_count > 1:
            iface = node.addInterface('eth1')
            lan.addInterface(iface)

    run_install_script(node, 'install_docker.sh')
    run_install_script(node, 'install_docker_compose.sh')

pc.printRequestRSpec(request)
