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

    df_tour_win = df[['season', 'daynum', 'wteamid', 'lteamid']]
    pd.merge(df_tour_win, ref, how='left', left_on='wteamid', right_on='teamid')

    return df

def run():

    # team names
    ref_teams = clean_names(pd.read_pickle('data/imported/mteams.pkl'))

    # Season results
    df_tour = clean_names(pd.read_pickle('data/imported/mncaatourneydetailedresults.pkl'))

    process_tour_score(df_tour)

    format_tour(df_tour)








    pass


if __name__ == '__main__':

    os.chdir('..')
    pd.set_option('expand_frame_repr', False)

    run()