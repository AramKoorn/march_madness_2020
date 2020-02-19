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

def process_tour_score(df):

    ref_win = df.groupby('wteamid').wscore.mean().reset_index().rename(columns={'wscore': 'avg_wscore_tour'})
    ref_lose = df.groupby('lteamid').lscore.mean().reset_index().rename(columns={'lscore': 'avg_lscore_tour'})

    ref_tour_scores = pd.merge(ref_win, ref_lose, left_on='wteamid', right_on='lteamid', how='left')

    ref_tour_scores = ref_tour_scores.rename(columns={'wteamid': 'teamid'}).drop(columns='lteamid')

    pd.to_pickle(ref_tour_scores, 'data/processed/d_mapping_tour_scores.pkl')

    return df


def format_tour(df):

    ref = pd.read_pickle('data/processed/d_mapping_tour_scores.pkl')


    df_tour_win = df[['season', 'daynum', 'wteamid','lteamid' ]].copy()
    df_tour_lose = df[['season', 'daynum', 'wteamid', 'lteamid']].copy()

    #
    df_tour_win['teamid'] = df_tour_win.wteamid
    df_tour_lose['teamid'] = df_tour_lose.lteamid

    # kpi
    df_tour_win['kpi'] = 1
    df_tour_lose['kpi'] = 0

    # concat
    df = pd.concat([df_tour_win, df_tour_lose])

    # Merge seeds
    ref_seeds = pd.read_pickle('data/imported/mncaatourneyseeds.pkl')
    ref_seeds = clean_names(ref_seeds)

    df = pd.merge(df, ref_seeds, how='left', left_on=['season', 'wteamid'], right_on=['season', 'teamid'], validate='m:1').rename(columns={'seed': 'wseed'})
    df = pd.merge(df, ref_seeds, how='left', left_on=['season', 'lteamid'], right_on=['season', 'teamid'], validate='m:1').rename(columns={'seed': 'lseed'})

    df['seed_winner'] = df['wseed'].apply(lambda x: x[1:3]).astype('int')
    df['seed_loser'] = df['lseed'].apply(lambda x: x[1:3]).astype('int')

    df['seed_difference'] = np.where(df.wteamid == df.teamid, df.seed_winner - df.seed_loser,
                                     df.seed_loser - df.seed_winner)


    return df

def run():

    # team names
    ref_teams = clean_names(pd.read_pickle('data/imported/mteams.pkl'))

    # Season results
    df_tour = clean_names(pd.read_pickle('data/imported/mncaatourneydetailedresults.pkl'))

    process_tour_score(df_tour.copy())

    df_tour = format_tour(df_tour)
    pd.to_pickle(df_tour, 'data/processed/tour_features.pkl')








    pass


if __name__ == '__main__':

    os.chdir('..')
    pd.set_option('expand_frame_repr', False)

    run()