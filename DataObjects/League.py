from HelperFunctions.bcolors import bcol
import numpy as np
from dataclasses import dataclass, field, astuple, asdict

from typing import Optional, List, Dict
import datetime
import json


#PandasDataFrame = TypeVar('pandas.core.frame.DataFrame(str)')
class SortIndexNotInPrintParams(Exception):
    """If sorting index is not in the parameters to be printed, then how should we sort this?"""
    pass
class FunctionHasNotBeenTested(Exception):
    """This Function stops the Code, for functions which either have not been tested or finished."""
    pass
class WhoIsthisHesNotaManagerError(Exception):
    """Managers: \n -  ebb  \n -  thorsteinns  \n -  nonni123  \n -  agustlogi  \n -  arnarleo  \n -  birgirms   \n -  viktorhelgi  \n -  2g1c  \n -  tindurs  \n -  vikkisibbi  \n -  thorsteinnah  \n -  jonhugi97 """
    pass

#@dataclass(slots=True, order=True) python version 3.10
@dataclass(order = True)
class Player:
    """
    attributes: [
        index: int,
        name: Optional[str],
        value: Optional[int],
        value_history: Optional[List[int]],
        team: Optional[str],
        position: Optional[str]
    ]
    functions: []

    ## Extra
    @dataclass(order = True)
    x = [Player('dj moore', 7261), Player('jamarr chase', 9999.0)]
    x.sort(reverse=True)
    print(x)
    -> [ Player('jamarr chase', 9999.0), Player('dj moore', 7261)]
    """
    #__slots__ = ('index', 'p_name', 'value', 'value_history', 'team', 'position')

    index: int = field(init=False, compare=True) # We define index as a field for the sorting function. However, we define 'init=False' so we do not initialize it
    value_history:Optional[List[int]] = None
    name:str = None
    value: Optional[int] = None
    team:Optional[str] = None
    position:Optional[str] = None
    sleeper_id:Optional[int] = None
    ktc_id:Optional[int] = None
    draft_pick:Optional[int] = None
    draft_round:Optional[int] = None
    draft_ovr:Optional[int] = None
    birthdate:datetime.datetime = None
    age:Optional[int] = None
    height:Optional[int] = None
    weight:Optional[int] = None

    def __str__(self):
        name     = f'name:    \t {self.name}\n'
        value    = f'value:   \t {self.value}\n'
        team     = f'team:    \t {self.team}\n'
        position = f'position:\t {self.position}\n'
        val_hist = f'value_history is {"undefined" if (type(self.value_history) == str) else "defined"}'
        return name + value + team + position + val_hist
    def __post_init__(self):
        # create index variable
        object.__setattr__(self, 'index', self.sleeper_id)
        # calculate age
        if self.birthdate != None and self.birthdate != 'unknown' and self.age == None:
            date_info = self.birthdate.split('-') # self.birthdate = "YYYY-MM-DD"
            datetime_obj = datetime.datetime(int(date_info[0]), int(date_info[1]), int(date_info[2]))
            object.__setattr__(self, 'age', (datetime.datetime.now() - datetime_obj).days/365.25)
    def  __eq__(self, other):
        """Allows indexing such that
            players.index('jamarr chase')
            -> 20
        """
        if other == self.name:
            return True
        return False

#@dataclass(slots=True, order=True) python version 3.10
@dataclass(order=True)
class Players:
    """
    attributes: [players: List[Player]]
    functions: [
        names () -> List[str],
        create_new_object (...) -> Players
    ]
    """
    players: List[Player] = field(default_factory=list)
    def __iter__(self):
        """Dont really know how this works. Might have to delete later, it lets us at least do a for-loop "for player in players:" (wher players:Players)"""
        yield from self.players
    def __getitem__(self, sleeper_id):
        return self.players[self.players.index(sleeper_id)]
    def __str__(self, indent=0):
       self.players.sort()
       return '\n'.join([f'{" "*indent + " "*(4-len(str(int(p.value))))}{int(p.value)}: {p.name}' for p in self.players])
    def add_player(self, **kwargs):
        input_vars = ['name', 'value', 'value_history', 'team', 'position', 'sleeper_id', 'ktc_id', 'draft_pick', 'draft_round', 'draft_ovr', 'birthdate', 'height', 'weight']
        for var in input_vars:
            if var not in kwargs.keys():
                kwargs[var] = 'unknown'
        self.players.append(Player(
             name= kwargs['name'],
             value= kwargs['value'],
             value_history= kwargs['value_history'],
             team = kwargs['team'],
             position = kwargs['position'],
             sleeper_id = kwargs['sleeper_id'],
             ktc_id = kwargs['ktc_id'],
             draft_pick = kwargs['draft_pick'],
             draft_round = kwargs['draft_round'],
             draft_ovr = kwargs['draft_ovr'],
             birthdate = kwargs['birthdate'],
             height = kwargs['height'],
             weight = kwargs['weight']
        ))
    @property
    def names(self):        
        return [p.name for p in self.players]
    @property 
    def values(self):
        return [p.value for p in self.players]

    def save_obj(self, file_name = 'data/players_collection.json'):
        if file_name == 'data/players_collection.json':
            x = int(input('WoWW are you sure, you want to owerwrite the file'))

        with open(file_name, 'w') as file:
            json.dump(
                asdict(self),
                file,
                indent = 4)

    #def index(self,player):
    #    self.players.index(player)
        
    def create_new_object(self, sort_attr='name', print_only=False, name_prefix='',*print_attr, **subset) -> object:
        """
        ### Player attributes
        - name
        - position
        - team
        - value
        - value_history

        ### *print_params
        This parameter is a list and includes those player attributes which will be printed. It iscomposed of all input variables not assigned a name. 
        ### **subset
        This parameter is a dictionary. Keys are attributes of the player and the values are lists having those specific attributes which will be used to created the subset.
        sort: what attribute to sort by.

        object.print(
            sort='name',
            position=['RB','WR'], 
            team=['GB', 'ARI', 'NE']
        )-> subset = {
            'position':['RB','WR'], 
            'team':['GB', 'ARI', 'NE']
        }
        """
        if not print_attr: # if print_attr is empty
            if print_only:
                print_attr = {'value':[], 'name':[]}
            else:
                print_attr = {'name': [], 'position': [], 'team': [], 'value': [], 'value_history': []}
        else:
            print_attr = {key:[] for key in print_attr}

        if sort_attr not in print_attr.keys():
            raise SortIndexNotInPrintParams('\nThe sorting index must be one of the parameters which will be printed.')
        if sort_attr=='name':
            self.players.sort()

        # Put player into list, conditional on "subset" and "name_prefix"
        for player in self.players:
            name = player.name
            add_player = True
            if subset:
                raise FunctionHasNotBeenTested('\nThis Function probably works, however, we first need to make the dataset bigger. We have no information about what teams players are playing for, nor what position the are playing in.')
                for attr, set in subset.items():
                    #print(name[0:len(name_prefix)])
                    add_player = add_player and (player[attr] in set) 
            if name_prefix:
                add_player = add_player and (name[0:len(name_prefix)] == name_prefix)
            if add_player:
                for key in print_attr:
                    player.__getattribute__(key)
                    print_attr[key].append(player.__getattribute__(key))
        
        # Sort Columns (return 'sorted_lists', the variable is iterable [[9999, 'jamaarr chase],[5282, 'james robinson'], ...[]] ]
        index = np.argmax(np.array(list(print_attr.keys())) == sort_attr) # the index of ``sort`` in the dictionary
        lists = list(print_attr.values())
        zipped_list = zip(*lists)
        if sort_attr in ['name', 'team', 'pos']:
            sorted_lists = sorted(zipped_list, key=lambda t: t[index], reverse = False)
        else:
            sorted_lists = sorted(zipped_list, key=lambda t: t[index], reverse = True)

        if print_only:
            # print the column names (e.g. 'value \t name')
            for attr in print_attr.keys():
                print(attr, end=' '*(6-len(attr)))
            print()
            # print the the attributes of each player
            for items in sorted_lists:
                for value, attr in zip(items,list(print_attr.keys())):
                    if attr != 'name':
                        print(int(value), end=' '*(6-len(str(int(value)))))
                    else:
                        print(value)
        else:
            players = []
            for items in sorted_lists:
                player = Player()
                for value, attr in zip(items,list(print_attr.keys())):
                    player.__setattr__(attr, value)
                players.append(player)
            return Players(players)

#@dataclass(slots=True) python version 3.10
@dataclass()
class Team:
    """
    attributes: [
        manager:str, 
        players:Players
    ]
    functions: [get_value () -> int]
    """
    manager: str
    players: Players
    def __str__(self):
        s = '\n'.join([
            bcol.B.w + 'type: ' + bcol.g + 'Team' + bcol.reset,
            bcol.B.w + 'attributes: ['+
            bcol.B.grey + 'manager:'+bcol.g+'str'+bcol.reset+', '+
            bcol.B.grey + 'players:'+bcol.g+'Players'+bcol.reset+']',
            bcol.B.grey + 'manager:'+bcol.g+' str '+bcol.reset+'= \n    '+bcol.y+ f"'{self.manager}'" + bcol.reset,
            bcol.B.grey + 'players:'+bcol.g+' Players '+bcol.reset+'=\n'
        ])
        s = s  +bcol.y+ self.players.__str__(indent=5) + bcol.reset
        return s

    @property
    def total_value(self) -> int:
        value = 0
        for name in self.players.names:
            player = self.players[name]
            value += player.value
        return int(value)
    
    @property
    def player_values(self) -> Dict[str, int]:
        players = {}
        for name in self.players.names:
            players[name] = self.players[name].value
        return players


    def  __eq__(self, other):
        """Allows indexing such that"""
        if other == self.manager:
            return True
        return False
    def __getitem__(self, player):
        return self.players[player]

#@dataclass(slots=True) python version 3.10
@dataclass()
class League:
    """
    attributes: [
        teams:List[Team], 
        name:str
    ]
    functions: [managers () -> List[str]]
    """
    teams: List[Team]
    name: str = 'Dynasty Sandwich'
    def __str__(self):
        s = '\n'.join([
            bcol.B.w + 'type: ' + bcol.g + 'League' + bcol.reset,
            bcol.B.w + 'attributes: ['+
            bcol.B.grey + 'name:'+bcol.g+'str'+bcol.reset+', '+
            bcol.B.grey + 'teams:'+bcol.g+'List[Team]'+bcol.reset+']',
            bcol.B.grey + 'name:'+bcol.g+' str '+bcol.reset+'= \n    '+bcol.y+ f"'{self.name}'" + bcol.reset,
            bcol.B.grey + 'teams:'+bcol.g+' List[Team] '+bcol.reset+'=\n'
        ])
        teams_values = sorted([[team.total_value, team.manager] for team in self.teams],key=lambda t: t[0], reverse = True)
        for value, manager in teams_values:
            s += bcol.y +' '*(11-len(str(value)))+ str(value) + ': '+ manager + '\n' + bcol.reset
        return s
    def __getitem__(self, manager) -> Team:
        return self.teams[self.teams.index(manager)]
    @property
    def managers(self) -> List[str]:
        return [r.manager for r in self.teams]



