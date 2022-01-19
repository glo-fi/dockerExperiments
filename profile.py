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
pc.defineParameter('create_lan', 'Create Virtual LAN', portal.ParameterType.BOOLEAN, 'True')
pc.defineParameter('scenario', 'Choose scenario to run (test, httpd) ', portal.ParameterType.STRING, None)

params = pc.bindParameters()

if params.scenario is None:
    pc.reportError(portal.ParameterError('You Must Choose A Scenario.', ['scenario']))

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

def run_init_script(node, script):
    node.addService(pg.Execute(shell='bash', command='chmod +x /local/repository/detgenScripts/init/' + script))
    node.addService(pg.Execute(shell='bash', command='/local/repository/detgenScripts/init/' + script))

def build_local_dockerfile(node, dockerfile):
    node.addService(pg.Execute(shell='bash', command='sudo docker build -t ' + dockerfile + ' /local/repository/detgenScripts/images/' + dockerfile + '/'))

def attach_tcpdump(node, container_name):
    node.addService(pg.Execute(shell='bash', command='sudo docker run -v /local/repository/collectedData:/data --network=container:' + container_name + ' docker-tcpdump /usr/sbin/tcpdump')

for i in range(params.node_count
    node = request.RawPC('node' + str(i))

    if params.create_lan:
        if params.node_count > 1:
            iface = node.addInterface('eth1')
            lan.addInterface(iface)

    run_install_script(node, 'install_docker.sh')
    run_install_script(node, 'install_docker_compose.sh')
    
    if params.scenario == "test":
        pass
    elif params.scenaro == "httpd":
        if i == 0:
            run_init_script(node, 'init-httpd.sh')
        if i == 1:
            build_local_dockerfile(node, 'docker-wget')
            run_init_script(node, 'init-wget.sh')
        
pc.printRequestRSpec(request)
