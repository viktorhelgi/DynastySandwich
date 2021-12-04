import pickle
import pandas as pd
from dataclasses import dataclass, field
from typing import List
import sys

#######################
# This is a dataclass #
#######################
#@dataclass(slots=True, order=True) python version 3.10
@dataclass(order = True)   
class PlayerID: 
    name: str
    id: int
    pos: str
    index: int = field(init=False)
    def __post_init__(self):
        """This is run after the explicit variables have been defined. It puts the value on the index variable."""
        object.__setattr__(self, 'index', self.name)
    def __repr__(self) -> str:
        return f"\nPlayerID\n  name= '{self.name}'\n  id=    {self.id}\n  pos=  '{self.pos}'"
    def  __eq__(self, other):
        if other == self.name:
            return True
        return False


#@dataclass(slots=True) python version 3.10
@dataclass
class PlayersIDs:
    """Collection of PlayerID objects. Subscriptable and players can be added to the collection with obj.add_players()"""
    players: List[PlayerID] = field(default_factory=list)
    def add_player(self, name:str, id:int, position:str):
        self.players.append(PlayerID(name, id, position))
    def __getitem__(self,name):
        return self.players[self.players.index(name)]
    def __str__(self):
        return str(self.players)
    

def get_sleeper_ids():
    players_ids = PlayersIDs()
    id_dir = 'C:/Users/Lenovo/Documents/VSCode_Tests/NFL/Dynasty_Sandwich/data/ID_files/'
    id_files = ['QB', 'RB', 'WR', 'TE']
    for pos in id_files:
        with open(f'{id_dir}{pos}.txt', 'r') as f:
            f.readline()
            lines = f.readlines()
        for line in lines:
            name, id = line.replace('\n', '').split(',')
            players_ids.add_player(name, id, pos)
    return players_ids


if __name__ == '__main__':
    players_ids = get_sleeper_ids()
    print(players_ids['jamarr chase'])