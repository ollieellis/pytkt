from pytkt.app import Ticket, CmdLineApp

cmd = CmdLineApp()

class TestStoreAndLoad:

    def test_to_dict(self):
        t = Ticket(1, "test")
        assert cmd.list_to_dict({"test_list": [t]}) == self.get_one_ticket_dict()

    def test_store_one_ticket(self):
        t = Ticket(1, "test")
        cmd.lists = {"test_list": [t]}
        cmd.store_all("test_dir/test1.json")

    def test_load_one_ticket(self):
        t = Ticket(1, "test")
        fname = "test_dir/test2.json"
        cmd.lists = {"test_list": [t]}
        cmd.store_all(fname)
        cmd.load_all(default_lists=["test_list"], filename=fname)
        desired = self.get_one_ticket_dict()
        desired["test_list"] = [Ticket(**i) for i in desired["test_list"]]
        assert cmd.lists == desired

    def get_one_ticket_dict(self):
        return  {"test_list":
            [
                {
                    "id_": 1,
                    "task": "test",
                    "minutes": None,
                    "parent_id": None,
                    "other": {}
                }
            ]
        }
    
    def test_stored_broken(self):
        fname = "test_dir/added.json"
        cmd = CmdLineApp()
        cmd.load_all(fname)

class TestAdd:

    def test_simple(self):
        cmd = CmdLineApp()
        cmd.lists = {"test": []}
        cmd.add("test_task", "test")
        assert len(cmd.lists["test"]) == 1

class TestMove:
    
    def test_simple(self):
        fname = "test_dir/added.json"
        cmd = CmdLineApp()
        cmd.load_all(filename=fname)
        cmd.move(-999, "Done")
        assert len(cmd.lists["Done"]) == 1
        assert len(cmd.lists["BackLog"]) == 0

class TestRemove:
    
      def test_simple(self):
        fname = "test_dir/added.json"
        cmd = CmdLineApp()
        cmd.load_all(filename=fname)
        cmd.remove(-999)
        assert len(cmd.lists["BackLog"]) == 0

class TestDisplay:

    def test_simple(self):
        t1 = Ticket(1, "test")
        t2 = Ticket(2, "test2")
        t3 = Ticket(3, "test3")
        lists = {"l1": [t1, t2], "l2": [t3]}
        cmd.display(lists)


class TestUnpackAddParams:

    def test_minimal_params(self):
        params = ["test_task", "Done"]
        fname = "test_dir/added.json"
        cmd = CmdLineApp()
        t = cmd.unpack_add_params(params)
        assert t == ["test_task", "Done", None, None, None]

    def test_to_many(self):
        params = list(range(0, 10))
        cmd = CmdLineApp()
        assert cmd.unpack_add_params(params) == [0, 1, 2, 3, 4]

class TestGetTicketIndex:

    def test_ez(self):
        cmd = CmdLineApp()
        cmd.lists = self.get_simple_test_case()
        assert cmd.get_ticket_index(2) == ("test_list", 1) #0 index list

    def get_simple_test_case(self):
        return  {"test_list":
            [
                Ticket(**{
                    "id_": 1,
                    "task": "test",
                    "minutes": None,
                    "parent_id": None,
                    "other": {}
                }),
                Ticket(**{
                    "id_": 2,
                    "task": "test2",
                    "minutes": None,
                    "parent_id": None,
                    "other": {}
                })
            ],
            "test_list2":
            [
                Ticket(**{
                    "id_": 3,
                    "task": "test3",
                    "minutes": None,
                    "parent_id": None,
                    "other": {}
                })
            ],
        }