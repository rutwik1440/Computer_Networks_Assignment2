from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import Node
from mininet.topo import Topo
from mininet.node import OVSController
from mininet.log import info
from mininet.link import TCLink
import threading
import argparse


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

l=0

class lossyNetworkTopo(Topo):
    def build(self, **_opts):
        s1, s2 = [self.addSwitch(s) for s in ('s1', 's2')]

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        for h, s in [(h1, s1), (h2, s1), (h3, s2), (h4, s2)]:
            self.addLink(h, s)

        global l
        self.addLink(s1, s2, cls=TCLink, loss=l)


class NetworkTopo(Topo):
    def build(self, **_opts):
        s1, s2 = [self.addSwitch(s) for s in ('s1', 's2')]

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        for h, s in [(h1, s1), (h2, s1), (h3, s2), (h4, s2)]:
            self.addLink(h, s)

        self.addLink(s1, s2)

def run_c(congestion_type):
    topo = NetworkTopo()
    net = Mininet(topo=topo)
    net.start()
    h1, h2, h3, h4 = net.get('h1', 'h2', 'h3', 'h4')
    h4.cmd('iperf -s &')
    h1.cmd(f'iperf -c 10.0.0.4 -t 600 -i 10 -Z {congestion_type} > resulth1.txt &')
    h2.cmd(f'iperf -c 10.0.0.4 -t 600 -i 10 -Z {congestion_type} > resulth2.txt &')
    h3.cmd(f'iperf -c 10.0.0.4 -t 600 -i 10 -Z {congestion_type} > resulth3.txt &')
    CLI(net)
    net.stop()


def run_b(linkloss, congestion_type):
    if linkloss==0:
        topo=NetworkTopo()
        net = Mininet(topo=topo)
    else:
        l = linkloss
        topo = lossyNetworkTopo()
        net = Mininet(topo=topo, link=TCLink)
    net.start()
    h1, h2, h3, h4 = net.get('h1', 'h2', 'h3', 'h4')
    h4.cmd('iperf -s &')
    h1.cmd(f'iperf -c 10.0.0.4 -t 360 -i 5 -Z {congestion_type} > resulth1.txt &')
    CLI(net)
    net.stop()

def main():
    parser = argparse.ArgumentParser(description='Your program description here')
    parser.add_argument('--config',type=str,choices=['b','c'], required=True)
    args = parser.parse_args()
    config_type = args.config
    congestion_choices = ['vegas', 'reno', 'cubic', 'bbr']
    congestion_type = input("Enter which congestion type do you want? vegas, reno, cubic or bbr?: ")
    if congestion_type not in congestion_choices:
        print("Please enter a valid congestion type!")
        return
    linkloss = int(input("Enter what percentage of linkloss? 0, 1 or 3?: "))
    if linkloss!=0 and linkloss!=1 and linkloss!=3:
        print("Please enter valid linkloss!")
        return
    setLogLevel('info')
    if config_type == 'c':
        run_c(congestion_type)
    else: #configuration b
        run_b(linkloss, congestion_type)


if __name__ == '__main__':
    main()
