#what i want to be able to do;
#add ticket
#delete tickets
#move ticket
#filter tickets
#clear list
#display tickets
#store, reload tickets
#spend the absolute minum time developing this; primative types allowed, low qualitity tests to

from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional
import json
from loguru import logger
import time

DEFAULT_LISTS = ["BackLog", "InProgress", "Done", "Blocked"]

@dataclass
class Ticket:
    id_: int
    task: str
    minutes: int = None
    parent_id: int = None
    other: Dict[str, str] = field(default_factory=dict)


class CmdLineApp:
    lists = Dict[str, List[Ticket]]
    tkt_filename = str

    def __init__(self, tkt_filename=None) -> None:
        self.lists = {}
        self.tkt_filename = tkt_filename

    def dispacth(self, argsv):
        if len(argsv) == 1:
            self.display()
            return
        
        match argsv[1].lower():
            case "move":
                self.move_func(argsv[2:])
            case "add":
                self.add_func(argsv[2:])
            case "remove":
                self.remove_func(argsv[2:])
            case "start":
                self.start_func(argsv[2:])
            case _:
                logger.error("Command Not Recognized")

        self.display()
        try:
            self.store_all()
        except Exception as e:
            logger.error(f"failed to store: {e}")

    def add_func(self, remaining_args):
        params = self.unpack_add_params(remaining_args)
        if params is None:
            return 
        self.add(*params)

    def move_func(self, remaining_args):
        params = self.unpack_move_params(remaining_args)
        if params is None:
            return 
        self.move(*params)

    def remove_func(self, remaining_args):
        ticket_id = self.unpack_remove_args(remaining_args)
        self.remove(ticket_id)

    def start_func(self, remaining_args):
        ticket_id = self.unpack_remove_args(remaining_args)
        ticket_index = self.get_ticket_index(ticket_id)
        t = self.lists[ticket_index[0]][ticket_index[1]] #magic funcs these
        time = t.minutes
        if time is None:
            time = int(input(f"For how long? minutes: int \n"))
        self.start(ticket_id, time)

    def add(self, task: str, dest_list: str, minutes: int=None, parent_id=None, other=None):
        if dest_list not in self.lists:
            if input(f"No list: {dest_list}, Do you want to create new list?: Y/N").upper() not in ["Y", "YES"]:
                return
            self.lists[dest_list] = []
        id_ = self.get_next_index(self.lists)
        ticket = Ticket(id_, task, minutes, parent_id, other)
        self.lists[dest_list].append(ticket)

    def move(self, ticket_id: int, dest_list: str):
        try:
            ticket_index = self.get_ticket_index(ticket_id)
            if ticket_index is None:
                print("No ticket Found")
                return
            self.lists[dest_list].append(self.lists[ticket_index[0]][ticket_index[1]])
            self.lists[ticket_index[0]].pop(ticket_index[1])
        except Exception as e:
            logger.error(f"Failed to move ticket {e}")

    def remove(self, ticket_id: int):
        ticket_index = self.get_ticket_index(ticket_id)
        if ticket_index is None:
            print("No ticket Found")
            return
        self.lists[ticket_index[0]].pop(ticket_index[1])

    def start(self, ticket_id: int, time: int):
        self.move(ticket_id, "InProgress")
        self.store_all()
        self.print_timer(time)

    def store_all(self, filename: Optional[str] = None):
        if filename is None:
            filename = self.tkt_filename
        json_dict = self.list_to_dict(self.lists)
        with open(filename, 'w') as f:
            json.dump(json_dict, f, indent=4)


    def load_all(self, default_lists: List[str]=DEFAULT_LISTS, filename: Optional[str] = None):
        if filename is None:
            filename = self.tkt_filename
        try:
            lists = {i: [] for i in default_lists}
            with open(filename, 'r') as f:
                tickets_dicts = json.load(f)
            for lname, ticket_list in tickets_dicts.items():
                lists[lname] = [Ticket(**t) for t in ticket_list]
            self.lists=lists
        except Exception as e:
            logger.error(f"Failed to Load Json {e}")
    
    def display(self, others: bool=False):
        #this is really bad to test...
        #make this into a decorater
        [print() for i in range(10)]
        for lname, ticket_list in self.lists.items():
            print(lname)
            for ticket in ticket_list:
                print(f"\t {ticket.id_}: {ticket.task}")
            print("-"*60)

    def unpack_add_params(self, remaining_args):
        if len(remaining_args) < 1:
            print("Add requires Task def: str as minumum")
            return
        params = remaining_args + [None]*max(0, 5-len(remaining_args))
        try:
            minutes = int(remaining_args[1])
            params[1] = None
            params[2] = minutes
        except:
            pass

        if params[1] == None:
            params[1] = "BackLog"
    
        return params[:5]
    
    def unpack_move_params(self, remaining_args):
        if len(remaining_args) != 2:
            print("Add requires task_id: int and dest_list: str as minumum")
            return 
        remaining_args[0] = int(remaining_args[0])
        return remaining_args

    def unpack_remove_args(self, remaining_args):
        if len(remaining_args) != 1:
            print("Add requires task_id: int")
            return 
        remaining_args[0] = int(remaining_args[0])
        return remaining_args[0]
        

    def list_to_dict(self, lists: Dict[str, List[Ticket]]):
        return {k: [asdict(ticket) for ticket in v] for k,v in lists.items()}
    
    def get_ticket_index(self, ticket_id: int):
        ticket_index = None
        for lname, ticket_list in self.lists.items():
            for i, ticket in enumerate(ticket_list):
                if ticket.id_ == ticket_id:
                    ticket_index = (lname, i)
                    break
        return ticket_index
    
    def get_next_index(self, lists: Dict[str, List[Ticket]]):
        max_id = 0
        for lname, ticket_list in lists.items():
            for i, ticket in enumerate(ticket_list):
                max_id = max(max_id, ticket.id_)
        return max_id + 1
    
    def print_timer(self, minutes: int):
        for i in range(minutes, 0, -1):
            print(f"{i} minutes left", end='\r')
            time.sleep(60)
