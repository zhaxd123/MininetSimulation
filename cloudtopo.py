import sys
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI

if len(sys.argv) > 3:

	class MyTopo( Topo ):
	    "Distributed Cloud Topology"
	    def __init__( self ):
		"Create custom topo."
	    	Topo.__init__( self )

		
		flag = 'OFF'		
		datacenter_id = 1
		client_id = 1		
		host_id = 1
		dc_switch_list = []
		dc_gw_list = []

		for i in sys.argv:

			if i == '-d':
				flag = 'datacenter'
				continue
			if i == '-c':
				flag = 'client'
				continue

			if flag == 'datacenter':

				dc_host_num = int(i)

				dc_switch = self.addSwitch('s%d' % (2*datacenter_id - 1))
				dc_switch_list.append(dc_switch)

				dc_gw = self.addSwitch(('s%d' % (2*datacenter_id)))
				dc_gw_list.append(dc_gw)

				for j in range (1,dc_host_num+1):
					host = self.addHost('h%d' % host_id ,  ip='10.0.%d.%d/24' % (datacenter_id,j))
					host_id = host_id + 1
					self.addLink(host,dc_switch)

				datacenter_id = datacenter_id + 1


			if flag == 'client':

				cl_host_num = int(i)

				for j in range (1,cl_host_num+1):
					cl_host = self.addHost('h%d' % host_id ,  ip='10.1.%d.1/24' % j)
					host_id = host_id + 1
					cl_switch = self.addSwitch('s%d' % (2*(datacenter_id - 1)+j))
					self.addLink(cl_host,cl_switch)



		for dc_switch in dc_switch_list:
			for dc_gw in dc_gw_list:
				self.addLink(dc_switch,dc_gw)



	net = Mininet(topo = MyTopo())
	net.start()
	CLI(net)
	net.stop()

else:
	print "Not enough input variables."