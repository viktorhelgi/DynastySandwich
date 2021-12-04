import inspect
import os
from HelperFunctions.bcolors import bcol
from typing import Callable


#def get_path(file_path):
#    cf = currentframe()
#    print(bcol.I.y + ' - Path to line: -> ' + bcol.IU.y + '"{}", line {}'.format(file_path,cf.f_back.f_lineno) + bcol.reset)
    
def get_path():
    current_frame = inspect.currentframe()
    parent_frame = inspect.getouterframes(current_frame)[1].frame
    path_parent_file = inspect.getabsfile(parent_frame)
    #inspect.getabsfile(inspect.getouterframes( inspect.currentframe() )[1].frame)
    print(bcol.I.y + ' - Path to line: -> ' + bcol.IU.y + '"{}", line {}'.format(path_parent_file, current_frame.f_back.f_lineno) + bcol.reset)
    print(inspect.getouterframes(current_frame)[1].function)
    #print(inspect.getabsfile(inspect.getouterframes( inspect.currentframe() )[1].frame))

def print_class_function():
    current_frame = inspect.currentframe()
    parent_frame = inspect.getouterframes(current_frame)[1].frame
    path_parent_file = inspect.getabsfile(parent_frame)
    #inspect.getabsfile(inspect.getouterframes( inspect.currentframe() )[1].frame)
    print(bcol.I.m + '{}:    -> '.format(inspect.getouterframes(current_frame)[1].function) + bcol.IU.y + '"{}", line {}'.format(path_parent_file, current_frame.f_back.f_lineno) + bcol.reset)
    #print(inspect.getabsfile(inspect.getouterframes( inspect.currentframe() )[1].frame))




class PointToFunction:
    #"""
    #    Notice, immediately after the class has been created, then we create
    #"""
    @staticmethod
    def print_func_info(func:Callable, kwargs):
        """Function used to print the information about the function being called"""

        func_name = func.__name__
        func_line = func.__code__.co_firstlineno
        func_path = func.__code__.co_filename
        header_lenght = 140

        text_1a = f'# function name:  {bcol.reset+bcol.B.p}{func_name}{bcol.reset}'
        text_2a = f'# file path:     {bcol.reset+bcol.y  }"{func_path}", line {func_line + 1}'
        text_1b = bcol.b + f'# function name:  {func_name}'
        text_2b = bcol.b + f'# file path:     "{func_path}", line {func_line + 1}'
        text_3 = f'# input arguments: {"" if kwargs else " None"}'

        print(
            bcol.B.b + 
            f'\n{"#"*header_lenght}\n'+
            f'{text_1a}  {bcol.B.b + " "*(header_lenght - len(text_1b)+2)}#\n' +
            f'{text_2a}  {bcol.reset +  bcol.B.b + " "*(header_lenght - len(text_2b)+2)}#\n'
            f'{text_3}{bcol.reset +  bcol.B.b + " "*(header_lenght - len(text_3)-1)}#'
        )
        for arg, val in kwargs.items():
            text_i = f'#   - {arg}: {bcol.B.p+" "*(10-len(arg))}{val + bcol.B.b }'.replace('\t', '  ')
            if len(text_i) <= header_lenght:
                print(f'{text_i}{" "*(header_lenght - len(text_i) + len(bcol.B.b+bcol.B.p)-1)}#')
            else:
                text_i = f'#   - {arg}: {type(val)}'
                print(f'{text_i}{" "*(header_lenght - len(text_i)-1)}')
        print(f'{"#"*header_lenght}' + bcol.reset)

    def __call__(self, func):
        def wrap(**kwargs):
            # print information about the function into the command line
            self.print_func_info(func, kwargs)
            # call the function 
            func(**kwargs)

        out_func = wrap
        out_func.__name__ = func.__name__
        return out_func






def print_header(cls=None, /, *, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False):

    temp = inspect.currentframe()
    line_called = temp.f_back.f_lineno
    outerFrames = inspect.getouterframes(temp)

    file_obj      = outerFrames[1]
    file_frame    = file_obj.frame
    file_line     = file_obj.lineno
    file_func     = file_obj.function
    file_path     = inspect.getabsfile(file_frame)

    print(file_func)
    print(file_obj)

    parent_obj    = outerFrames[2]
    parent_frame  = parent_obj.frame
    parent_line   = file_obj.lineno
    parent_func   = parent_obj.function
    parent_path   = inspect.getabsfile(parent_frame)


    print('\n')
    print(file_func)
    print(parent_func)

    print('\n')
    print(file_obj)
    print(parent_obj)

    if len(outerFrames) == 3:
        header_lenght = 140
        print(
            bcol.B.b + 
            '\n{}'.format('#'*header_lenght),
            #'\n#'+'-'*47+'#',
            '\n# function name: ', bcol.B.p + file_func + bcol.reset + bcol.BI.w + ' (Level: 1)' + bcol.reset +  bcol.B.b + ' '*(header_lenght - len('# function name: {} (Level: 1)'.format(file_func) )-2) + '#',
            '\n# file path:     ', bcol.IU.y + f'"{file_path}", line {file_line}',     bcol.reset +  bcol.B.b + ' '*(header_lenght - len('# file path:     {}'.format(file_path) ) - 3) + '#',
            '\n# parent path:   ', bcol.IU.y + f'"{parent_path}", line {parent_line}', bcol.reset +  bcol.B.b + ' '*(header_lenght - len('# parent path:   {}'.format(parent_path) ) - 3) + '#',
            '\n{}'.format('#'*header_lenght) + bcol.reset
        )
    elif len(outerFrames) == 4:
        header_lenght = 138
        print(
            bcol.b + 
            '\n#{}#'.format('-'*header_lenght),
            '\n# - function name: ', bcol.B.p + file_func + bcol.reset + bcol.BI.w + ' (Level: 2)' + bcol.reset +  bcol.b + ' '*(header_lenght - len('# function name: {} (Level: 1)'.format(file_func) ) -2) + '#',
            '\n# - file path:     ', bcol.IU.y + f'"{file_path}", line {file_line}',     bcol.reset +  bcol.b + ' '*(header_lenght - len('# file path:     {}'.format(file_path) ) - 3) + '#',
            '\n# - parent path:   ', bcol.IU.y + f'"{parent_path}", line {parent_line}', bcol.reset +  bcol.b + ' '*(header_lenght - len('# parent path:   {}'.format(parent_path) ) - 3) + '#',
            '\n#{}#\n'.format('-'*header_lenght) + bcol.reset,

        )
    elif len(outerFrames) == 5:
        header_lenght = 138
        print(
            bcol.b + 
            '\n#{}#'.format('-'*header_lenght),
            '\n#   - function name: ', bcol.B.p + file_func + bcol.reset + bcol.BI.w + ' (Level: 3)' + bcol.reset +  bcol.b + ' '*(header_lenght - len('# function name: {} (Level: 1)'.format(file_func) )-4) + '#',
            '\n#   - file path:     ', bcol.IU.y + f'"{file_path}", line {file_line}',     bcol.reset +  bcol.b + ' '*(header_lenght - len('# file path:     {}'.format(file_path) ) - 5) + '#',
            '\n#   - parent path:   ', bcol.IU.y + f'"{parent_path}", line {parent_line}', bcol.reset +  bcol.b + ' '*(header_lenght - len('# parent path:   {}'.format(parent_path) ) - 5) + '#',
            '\n#{}#\n'.format('-'*header_lenght) + bcol.reset,
        )
    elif len(outerFrames) == 6:
        header_lenght = 138
        print(
            bcol.I.b + 
            '\n#{}#'.format('-'*header_lenght),
            '\n#   - function name: ', bcol.B.p + file_func + bcol.reset + bcol.BI.w + ' (Level: 4)' + bcol.reset +  bcol.I.b + ' '*(header_lenght - len('# function name: {} (Level: 1)'.format(file_func) )-6) + '#',
            '\n#   - file path:     ', bcol.IU.y + f'"{file_path}", line {file_line}',     bcol.reset +  bcol.I.b + ' '*(header_lenght - len('# file path:     {}'.format(file_path) ) - 7) + '#',
            '\n#   - parent path:   ', bcol.IU.y + f'"{parent_path}", line {parent_line}', bcol.reset +  bcol.I.b + ' '*(header_lenght - len('# parent path:   {}'.format(parent_path) ) - 7) + '#',
            '\n#{}#\n'.format('-'*header_lenght) + bcol.reset,
        )
            

    #inspect.getabsfile(inspect.getouterframes( inspect.currentframe() )[1].frame)
    #print(bcol.I.y + ' - Path to line: -> ' + bcol.IU.y + '"{}", line {}'.format(file_path, line_called) + bcol.reset)

    
    

    #print(inspect.getabsfile(inspect.getouterframes( inspect.currentframe() )[1].frame))
    #print('file frame: ', file_frame)
    #print('file function: ', file_func)
    #print('file path: ', file_path)
    #print('')
    #print('parent file frame: ', parent_frame)
    #print('parent function: ', parent_func)
    #print('parent_path: ', parent_path)
    #print('')
    #print(len(outerFrames))

            