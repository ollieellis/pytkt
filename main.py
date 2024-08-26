import code

from pytkt.app import CmdLineApp, Ticket

try:
    cmd = CmdLineApp()
    cmd.load_all()
    cmd.display()
    code.interact(local=locals())
except Exception as e:
    print(f"Error: {e}")
    if input("Save jsons? Y/N \n").upper() in ["Y", "YES"]:
        cmd.store_all()
    