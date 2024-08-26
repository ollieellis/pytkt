import sys

from pytkt.app import CmdLineApp, Ticket

cmd = CmdLineApp()
cmd.load_all()
cmd.dispacth(sys.argv)