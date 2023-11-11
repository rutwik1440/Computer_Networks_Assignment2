from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import Node
from mininet.topo import Topo
from mininet.node import OVSController
from mininet.log import info


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class NetworkTopo(Topo):
    def build(self, **_opts):
        r1 = self.addHost('r1', cls=LinuxRouter, ip='192.168.1.1/24')
        r2 = self.addHost('r2', cls=LinuxRouter, ip='172.16.0.1/24')
        r3 = self.addHost('r3', cls=LinuxRouter, ip='10.0.0.1/24')

        s1, s2, s3 = [self.addSwitch(s) for s in ('s1', 's2', 's3')]

        self.addLink(s1, r1, intfName2='r1-eth1', params2={'ip': '192.168.1.1/24'})
        self.addLink(s2, r2, intfName2='r2-eth1', params2={'ip': '172.16.0.1/24'})
        self.addLink(s3, r3, intfName2='r3-eth1', params2={'ip': '10.0.0.1/24'})

        h1 = self.addHost('h1', ip='192.168.1.100/24', defaultRoute='via 192.168.1.1')
        h2 = self.addHost('h2', ip='192.168.1.101/24', defaultRoute='via 192.168.1.1')
        h3 = self.addHost('h3', ip='172.16.0.100/24', defaultRoute='via 172.16.0.1')
        h4 = self.addHost('h4', ip='172.16.0.101/24', defaultRoute='via 172.16.0.1')
        h5 = self.addHost('h5', ip='10.0.0.100/24', defaultRoute='via 10.0.0.1')
        h6 = self.addHost('h6', ip='10.0.0.101/24', defaultRoute='via 10.0.0.1')

        for h, s in [(h1, s1), (h2, s1), (h3, s2), (h4, s2), (h5, s3), (h6, s3)]:
            self.addLink(h, s)

        self.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth3', params1={'ip':'5.0.0.1/24'}, params2={'ip':'5.0.0.2/24'})
        self.addLink(r2, r3, intfName1='r2-eth2', intfName2='r3-eth3', params1={'ip':'5.0.1.1/24'}, params2={'ip':'5.0.1.2/24'})
        #self.addLink(r3, r1, intfName1='r3-eth2', intfName2='r1-eth3', params1={'ip':'5.0.2.1/24'}, params2={'ip':'5.0.2.2/24'})

def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)
    info(net['r1'].cmd('ip route add 172.16.0.0/24 via 5.0.0.2 dev r1-eth2')) #r1 connects to r2
    info(net['r1'].cmd('ip route add 10.0.0.0/24 via 5.0.0.2 dev r1-eth2')) #r1 connects to r3

    info(net['r2'].cmd('ip route add 192.168.1.0/24 via 5.0.0.1 dev r2-eth3')) #r2 connects to r1
    info(net['r2'].cmd('ip route add 10.0.0.0/24 via 5.0.1.2 dev r2-eth2'))

    info(net['r3'].cmd('ip route add 192.168.1.0/24 via 5.0.1.1 dev r3-eth3')) #r3 connects to r1
    info(net['r3'].cmd('ip route add 172.16.0.0/24 via 5.0.1.1 dev r3-eth3'))

    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
