import sys

from pytkt.app import CmdLineApp, Ticket

cmd = CmdLineApp(tkt_filename="/Users/ollieellis/prototypes/pytkt/tickets.json")
cmd.load_all()
cmd.dispacth(sys.argv)