"""/HelperFunctions/traceit.py

How to use this
- Assuming you are calling a function in the root directory.
- And Assuming this file ("traceit.py") is located in the folder "/HelperFunctions/"

Then:

import HelperFunctions.traceit as traceit
import sys
sys.setprofile(traceit.tracefunc)
"""

import sys


WHITE_LIST = {'plot_team_player_values.py','test6.py'}      # Look for these words in the file path.
EXCLUSIONS = {'<'}          # Ignore <listcomp>, etc. in the function name.


def tracefunc(frame, event, arg, indent=[0]):
    ###################
    # event == "call" #
    ###################

    if event == "call":
        tracefunc.stack_level += 1
        unique_id = frame.f_code.co_filename+str(frame.f_lineno)
        if unique_id in tracefunc.memorized:
            return

        # Part of filename MUST be in white list.
        is_file_whitelisted = any(x in frame.f_code.co_filename for x in WHITE_LIST)
        is_file_blacklisted = any(x in frame.f_code.co_name for x in EXCLUSIONS)
        if (is_file_whitelisted and not is_file_blacklisted):
            indent[0] += 2
            #print(dir(frame))
            #print(frame.f_locals)
            if 'self' in frame.f_locals:
                
                #print(dir(frame.f_locals['self'].__class__))
                class_something = frame.f_locals['self'].__class__
                if type(class_something) == str:
                    # The variable "class_something" is a string when we implement functions like
                    # def __getattribute
                    class_name = None
                    func_name  = class_something
                else:
                    class_name = class_something.__name__
                    func_name = class_name + '.' + frame.f_code.co_name
            else:
                func_name = frame.f_code.co_name
            #func_name = frame.f_code.co_name
            #func_name = '{name:->{indent}s}()'.format(indent=tracefunc.stack_level*2, name=func_name)
           
            relative_dir_path = frame.f_code.co_filename.replace("\\", '/').split(sys.path[0].replace("\\", '/'))[1]
            #print(func_name)
            txt = '|{}> {: <30} {} # {}, {}'.format(
                    "-" * (indent[0]-2),
                    func_name, 
                    " "*(10 - indent[0]),
                    relative_dir_path, 
                    frame.f_lineno
                    )
            print(txt)

            tracefunc.memorized.add(unique_id)

    #####################
    # event == "return" #
    #####################
    elif event == "return":
        is_file_whitelisted = any(x in frame.f_code.co_filename for x in WHITE_LIST)
        is_file_blacklisted = any(x in frame.f_code.co_name for x in EXCLUSIONS)
        if (is_file_whitelisted and not is_file_blacklisted):
            indent[0] -= 2
        tracefunc.stack_level -= 1
    

tracefunc.memorized = set()
tracefunc.stack_level = 0
