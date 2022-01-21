"""
General script for spawning nodes and containers
"""


import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.emulab as emulab
import geni.rspec.igext as igext

from random import randint

# Define constants here




# Create Portal Context

pc = portal.Context()

# Build Request Object for RSpec
request = pc.makeRequestRSpec()

# Define, Build and Verify Parameters

pc.defineParameter('node_count', 'Number of nodes', portal.ParameterType.INTEGER, 2)
pc.defineParameter('create_lan', 'Create Virtual LAN', portal.ParameterType.BOOLEAN, 'True')
pc.defineParameter('scenario', 'Choose scenario to run (test, httpd) ', portal.ParameterType.STRING, "httpd")

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
    tcpdump_id  = str(randint(0, 10000))
    node.addService(pg.Execute(shell='bash', command='chmod +x /local/repository/detgenScripts/init/init_tcpdump.sh'))
    node.addService(pg.Execute(shell='bash', command='sudo /local/repository/detgenScripts/init/init_tcpdump.sh ' + container_name + ' ' + tcpdump_id))

def execute_container_script(node, container_name, script, *args):
    arg_list = []
    for arg in args:
        arg_list.append(args)
    arg_string = ' '.join(arg_list)
    node.addService(pg.Execute(shell='bash', command='sudo docker exec ' + container_name + ' /local/scripts/' + script + ' ' + arg_string))

for i in range(params.node_count):
    node = request.RawPC('node' + str(i))

    if params.create_lan:
        if params.node_count > 1:
            iface = node.addInterface('eth1', pg.IPv4Address('192.168.6.%d' % (i+1), '255.255.255.0'))
            lan.addInterface(iface)

    run_install_script(node, 'install_docker.sh')
    run_install_script(node, 'install_docker_compose.sh')

    if params.scenario == "test":
        pass
    elif params.scenario == "httpd":
        if i == 0:
            build_local_dockerfile(node, 'docker-tcpdump')
            run_init_script(node, 'init_httpd.sh')
            attach_tcpdump(node, 'docker-httpd')
        elif i == 1:
            build_local_dockerfile(node, 'docker-wget')
            build_local_dockerfile(node, 'docker-tcpdump')
            run_init_script(node, 'init_wget.sh')
            attach_tcpdump(node, 'docker-wget')
            execute_container_script(node, 'docker-wget', 'exec_wget.sh', '192.168.6.1', '5')
        
pc.printRequestRSpec(request)
