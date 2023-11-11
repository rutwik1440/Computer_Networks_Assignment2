# Computer_Networks_Assignment2



For question 1, there are two files - a.py for part a of the question and c.py for part c of the question.

Part a of the question asks to implement the given topology. To do so, just run a.py using command - 'sudo python3 a.py'.
To check that everything is working fine, just write 'pingall' when mininet starts.

Part c of the question asks for the packet from h1 to take a specific route to reach h6. We have done this by changing the routing table of the routers.
We disconnected routers a and c and made the required changes in the routing table. The changes are shown in the .pdf document of the submission.
To confirm that the packet is taking the desired path, run the following command when mininet starts - 'h1 traceroute h6' and match the ip addresses printed
from the ip addresses in the routing tables.



For question 2, there are 3 files - maincode.py, plot.py, plotmultiple.py and 3 directories - part_a part_c and part_d.
maincode.py contains the main code of the question that contains the implementation of the given topology. You have to run this code for all parts of the question.
For part c of the question, run the following command - 'sudo python3 maincode --config=c'
For parts b and d of the question, run the command - 'sudo python3 maincode --config=b'
Then give the required values and link loss and congestion control scheme.

When running for part b or part d, a new file named 'resulth1.txt' containing the statistics for the packets sent by h1 would be created. To plot the graph of
throughput vs time run this command - 'python3 plot.py'

When running for part c, three files would be created - 'resulth1.txt', 'resulth2.txt' and 'resulth3.txt'. To plot the graph of throughput vs time run this
command - 'python3 plotmultiple.py'

When running 'maincode.py' for the second time, do remember to clear any extra files created by running the command - 'rm result*'

The directories part_a, part_c and part_d contain these extra 'result*' created by us and navigating them should be self explanatory!
