import pandas as pd
import os
from scripts.helper_functions import clean_names
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


'''
TODO: show winning teams
- Average score difference of the teams in the first round
'''


def process_reg_season_scores(df, ref_teams):
    df = pd.merge(df, ref_teams[['teamid', 'teamname']], how='left', left_on=['wteamid'], right_on='teamid',
                  validate='m:1').rename(columns={'teamname': 'wteamname'})
    df = pd.merge(df, ref_teams[['teamid', 'teamname']], how='left', left_on=['lteamid'], right_on='teamid',
                  validate='m:1').rename(columns={'teamname': 'lteamname'})

    df['wteam_diff'] = df.wscore - df.lscore
    df['lteam_diff'] = df.wteam_diff

    ref_winning = df.groupby(['season', 'wteamname', 'wteamid']).wteam_diff.mean().reset_index().rename(
        columns={'wteamname': 'teamname', 'wteam_diff': 'avg_season_wscore', 'wteamid': 'teamid'}).copy()
    ref_losing = df.groupby(['season', 'lteamname', 'lteamid']).lteam_diff.mean().reset_index().rename(
        columns={'lteamname': 'teamname', 'lteam_diff': 'avg_season_lscore', 'lteamid': 'teamid'}).copy()


    ref = pd.merge(ref_winning, ref_losing, how='left', on=['season', 'teamid', 'teamname'], validate='m:1')

    save_name = 'd_mapping_season_scores'

    print(f'\t Saving: {save_name}')
    ref.to_pickle(f'data/processed/{save_name}.pkl')
    ref.to_csv(f'local/{save_name}.csv')

    return ref


def format_data():

    df = clean_names(pd.read_pickle('data/imported/mregularseasondetailedresults.pkl'))

    # define kpi
    df['kpi'] = np.where(df.wloc == 'H', 1, 0)

    #
    ref_scores = pd.read_pickle('data/processed/d_mapping_season_scores.pkl')

    df_win = df[['season', 'daynum', 'wteamid', ]].copy().rename(columns={'wteamid': 'teamid'})
    df_lose = df[['season', 'daynum', 'lteamid', ]].copy().rename(columns={'lteamid': 'teamid'})

    # set kpi
    df_win['kpi'] = 1
    df_lose['kpi'] = 0

    df = pd.concat([df_win, df_lose])
    df['seed'] = 'season'

    return df


def run():

    # team names
    ref_teams = clean_names(pd.read_pickle('data/imported/mteams.pkl'))

    # Season results
    df_season = clean_names(pd.read_pickle('data/imported/mregularseasoncompactresults.pkl'))

    reg_scores = process_reg_season_scores(df_season, ref_teams)

    df = format_data()









    pass


if __name__ == '__main__':

    os.chdir('..')
    pd.set_option('expand_frame_repr', False)

    run()