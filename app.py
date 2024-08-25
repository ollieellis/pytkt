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
from typing import Dict, List
import json
from loguru import logger

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

    def __init__(self) -> None:
        self.lists = {}

    def add(self, task: str, dest_list: str, minutes: int=None, parent_id=None, other=None):
        if dest_list not in self.lists:
            if input(f"No list: {dest_list}, Do you want to create new list?: Y/N").upper() not in ["Y", "YES"]:
                return
            self.lists[dest_list] = []
        id_ = self.get_next_index(self.lists)
        ticket = Ticket(id_, task, minutes, parent_id, other)
        self.lists[dest_list].append(ticket)
        self.display()

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
        self.display()

    def remove(self, ticket_id: int):
        ticket_index = self.get_ticket_index(ticket_id)
        if ticket_index is None:
            print("No ticket Found")
            return
        self.lists[ticket_index[0]].pop(ticket_index[1])
        self.display()

    def store_all(self, filename: str = "/Users/ollieellis/prototypes/pytkt/tickets.json"):
        json_dict = self.list_to_dict(self.lists)
        with open(filename, 'w') as f:
            json.dump(json_dict, f, indent=4)


    def load_all(self, default_lists: List[str]=DEFAULT_LISTS, filename: str = "/Users/ollieellis/prototypes/pytkt/tickets.json"):
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
            print("-"*20)

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
        max_id = -999
        for lname, ticket_list in lists.items():
            for i, ticket in enumerate(ticket_list):
                max_id = max(max_id, ticket.id_)
        return max_id