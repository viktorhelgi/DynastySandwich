# -*- coding: utf-8 -*-
#######################################################
#                       Imports 
#######################################################
# external modules
from dataclasses import dataclass, field
from typing import Callable, Any, Optional, Dict, List, Union
import sys

# main operations
from Dynasty_Sandwich.visualize_excel import plot_history
from Dynasty_Sandwich.Operation_Funcs.fill_in_missing_data import print_missing_dates
from DataObjects.test_DataObjects import main_plot_test
from Dynasty_Sandwich.Helpers.update_file import update__keeptradecut_collection

# local helper modules
from HelperFunctions.bcolors import bcol
from Dynasty_Sandwich.Helpers.sleeper_id import sleeper_helper
#import pretty_errors

#######################################################
#              Functions which can be called          #
#######################################################

def get_operations():
    print('\nget_operations()')
    """If new functions"""
    operations = {
        1: {'function': plot_history},
        2: { 
            'function': print_missing_dates,
            'input': {
                'data1': '23.11.2021	90636	105780	72519	81244	60461	69466	89202	63287	51934	61385	51388	53627',
                'data2': '3.12.2021	89331	102820	72187	83288	58927	68315	88979	63852	51765	60047	51441	55042'
            }},
        3: {
            'function': main_plot_test, 
            'input': {'manager': 'viktorhelgi'},
            'options':{'manager':sleeper_helper.user_sub_ids}},
        4: {'function': update__keeptradecut_collection}
    }
    return operations


#######################################################
#                  Helper Functions
#######################################################

class SelectionError(Exception):
    """Selected integer must be within the interval [1, len(get_options)]"""
    __module__ = Exception.__module__

def validify_input(index, n_operations) -> int:
    """Assert that the string entered through the cmd is an integer and there is an operation for """
    try:
        index = int(index)
    except ValueError as e:
        raise ValueError('Input must be an integer')
    if not (1 <= index <= n_operations):
        raise SelectionError(f"The selected integer must be within the interval [{1}, {n_operations}].")
    return index

@dataclass
class FunctionHolder:
    """Function-holder for the function the user wants to call"""
    def __init__(self, operation) -> None:
        self.call: Callable[[Optional[Any]], None] = operation['function']
        self.name: str = operation['function'].__name__
        if 'input' in operation.keys():
            self.args: Optional[Dict[str,Any]] = operation['input']   
        else:
            self.args = 0
        if 'options' in operation.keys():
            for arg, options in operation['options'].items():
                show_options(options)
                selected_iarg = validify_input(input(bcol.y + ' >> ' + bcol.reset), len(options))
                self.args[arg] = options[selected_iarg]

    def __str__(self) -> None:
        if len(self.args) == 0:
            return f'\nfunction: {self.name}' + '\narguments: None\n'
        else:
            s_args = ''
            for key, value in self.args.items():
                s_args += f'\n  >> {key} = {repr(value)}'
            return f'\nfunction: {self.name}\narguments:{s_args}\n'

def show_options(options:Union[Dict[int,Any],List[Any]]) -> None:
    """Show what operations can be run with this module.Get selection number with ``input()`` and assert that it is valid. Then return a ``FunctionHolder`` object"""
    
    print(bcol.B.r2, '\nWhat would you like to run/select:', bcol.r)
    if type(options) == dict:
        for k in options:
            option = options[k]
            #if k==3:
            #    print(f'\n {operations[k]["function"]}')
            #    print(dir(operations[k]['function']))
            #    print(operations[k]['function'].__name__)
            if type(option) == str:
                print(f' {k}:{" "*(2-len(str(k)))}{option}')
            else:
                print(f' {k}:{" "*(2-len(str(k)))}{option["function"].__name__}')

    elif type(options)==list or type(options)==type(dict().values()):
        for i, option in enumerate(options):
            print(f' - {1+i}:{" "*(3-len(str(i)))+option}')

    print(bcol.B.y + '\nEnter the number of the operation which you would like to run', bcol.reset)

    

########################################################
#                    Main Functions                    #
########################################################

def main():
    print('\nmain()\n')
    print(main_plot_test)
    # 1. Get data
    operations = get_operations()
    # 2. Show data
    show_options(operations)
    # 3. Get Selection
    selected_ifunc = validify_input(input(bcol.y + ' >> ' + bcol.reset), len(operations))
    # 4. Define Functionholder
    func = FunctionHolder(operation = operations[selected_ifunc])
    if func.args:
            


        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # WWOOOOOOOOOOOOOOOOOWWWWWWWW!!!!!!!!!!!!!!!!!!!!!!
        # Example:
        # def main_plot_test(manager=None):
        #   print(manager) -> 'viktorhelgi'
        #   ...
        # func.args = {'manager': 'viktorhelgi'}
        # main_plot_test(**func.args)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        func.call(**func.args)

    else:
        func.call()
if __name__ == '__main__':
    print('\n' + bcol.BU.r + 'manual_run.py\n' + bcol.reset)
    main()

