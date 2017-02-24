import sys
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI

if len(sys.argv) == 3:
	
	datacenter = int(sys.argv[1])
	client = int(sys.argv[2])
	print "Create %s datacenters and %s clients" % (datacenter, client)

	class MyTopo( Topo ):
	    "Distributed Cloud Topology"
	    def __init__( self ):
		"Create custom topo."
	    	Topo.__init__( self )


		dc_net = self.addHost('h%d' % (datacenter+client+1),ip = '10.0.0.%d/24' % (datacenter+client+1))
		cl_net = self.addHost('h%d' % (datacenter+client+2),ip = '10.0.1.%d/24' % (datacenter+client+2))


		for i in range(1, datacenter+1):

			dc = self.addHost('h%d' % i,  ip='10.0.0.%d/24' % i)

			print "Create h%d as datacenter host, the ip address is 10.0.0.%d" % (i,i)

			dc_switch = self.addSwitch('s%d' % i)


			self.addLink(dc,dc_switch)
			self.addLink(dc_net,dc_switch)


		for j in range(datacenter+1, datacenter+client+1):

			cl = self.addHost('h%d' % j, ip = '10.0.0.%d/24' % j)

			print "Create h%d as client host, the ip address is 10.0.1.%d" % (j,j)

			cl_switch = self.addSwitch('s%d' % j)


			self.addLink(cl,cl_switch)
			self.addLink(cl_net,cl_switch)

		self.addLink(cl_net,dc_net)



	net = Mininet(topo = MyTopo())
	net.start()
	CLI(net)
	net.stop()

else:
	print "Not enough input variables."
