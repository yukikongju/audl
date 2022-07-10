import pandas as pd
from abc import ABC


class GameEvent(ABC):

    def __init__(self, row, description):
        """ 
        Parameters 
        ----------
        description: string
            description of event
        row: json 
            json document [t,l,r,x,y,s,c,q]
        """
        self.row = row
        self.description = description

    def print(self):
        pass

    def _read_json_dict(self):
        pass
        

class GameEventSimple(GameEvent):

    """ Game Event with only t """

    def __init__(self, code_type, description, json_dict):
        super().__init__(code_type, json_dict)

    def print(self):
        print(f"t: {self.code_type}")
        

class GameEventLineup(GameEvent):

    """ Game Event with lineup l """

    def __init__(self, code_type, description, json_dict):
        super().__init__(code_type, json_dict)

    def print(self):
        pass
        
        
class GameEventReceiver(GameEvent):

    """ Game Event with receiver r """

    def __init__(self, code_type, description, json_dict):
        super().__init__(code_type, json_dict)

    def print(self):
        pass

        
class GameEventS(GameEvent):

    """ Game Event with s """

    def __init__(self, code_type, description, json_dict):
        super().__init__(code_type, json_dict)

    def print(self):
        pass





