"""
    import_combine_data
    import_depth_charts
    import_draft_picks
    import_draft_values
    import_ids
    import_injuries
    import_ngs_data
    import_officials
    import_pbp_data
    import_pfr_passing
    import_qbr
    import_rosters
    import_sc_lines
    import_schedules
    import_seasonal_data
    import_snap_counts
    import_team_desc
    import_weekly_data
    import_win_totals
"""
import nfl_data_py as nfl
import pandas as pd

from HelperFunctions.bcolors import bcol

methods = [
    'import_combine_data', 'import_depth_charts', 'import_draft_picks', 
    'import_draft_values', 'import_ids', 'import_injuries', 'import_ngs_data', 
    'import_officials', 'import_pbp_data', 'import_pfr_passing', 'import_qbr', 
    'import_rosters', 'import_sc_lines', 'import_schedules', 'import_seasonal_data', 
    'import_snap_counts', 'import_team_desc', 'import_weekly_data', 
    'import_win_totals'
]

def save_data(filename='nfl_data_py.xlsx'):
    with pd.ExcelWriter('') as writer:  # doctest: +SKIP
        for method in methods:
            print(f'\n - {method}', end = '\t')
            if 'stat_type' in getattr(nfl,method).__code__.co_varnames:
                for stat_type in ['receiving','passing','rushing']:
                    df = getattr(nfl, method)(stat_type, years = [2021])
                    df.to_excel(writer, sheet_name=f'{method}_{stat_type}')     
            elif 'years' in getattr(nfl,method).__code__.co_varnames:
                df = getattr(nfl,method)(years = [2021])
                df.to_excel(writer, sheet_name=method)
            else:
                df = getattr(nfl,method)()
                df.to_excel(writer, sheet_name=method)

def print_columns_of_imports():
    for method in methods:
        if 'stat_type' in getattr(nfl,method).__code__.co_varnames:
            for stat_type in ['receiving','passing','rushing']:
                df = getattr(nfl, method)(stat_type, years = [2021])
                print(bcol.B.b + f'{method} - input: stat_type = {stat_type}' + bcol.reset)
                for col in df.columns:
                    print(f' - {col}')
        elif 'years' in getattr(nfl,method).__code__.co_varnames:
            df = getattr(nfl,method)(years = [2021])
            print(bcol.B.b + f'{method}' + bcol.reset)
            for col in df.columns:
                print(f' - {col}')
        else:
            df = getattr(nfl,method)()
            print(bcol.B.b + f'{method}' + bcol.reset)
            for col in df.columns:
                print(f' - {col}')
        

print_columns_of_imports()
#data = nfl.import_rosters(years = [2020])
#ids_pos_names = data[['player_name', 'player_id', 'position']]

