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


def avg_diffscore_tournament(df):

    df['score_diff'] = df.wscore - df.lscore

    ref = df.groupby(['season', 'wteamid']).aggregate({'score_diff': 'mean', 'wteamid': 'size'}).rename(
        columns={'score_diff': 'avg_scorediff_wteam', 'wteamid': 'n_wins'}).reset_index()

    # merge it back
    df = pd.merge(df, ref, how='left', on=['season', 'wteamid'], validate='m:1')

    if df.avg_scorediff_wteam.isna().sum() > 0:
        raise ValueError('There are na values')

    return df


def plot_avg_score_tournaments(df, ref_teams):

    print(f'Plotting: d')

    save_loc = 'analysis/avg_scorediff_teams_tournament.pdf'
    Path(os.path.dirname(save_loc)).mkdir(exist_ok=True)

    df = pd.merge(df, ref_teams, left_on='wteamid', right_on='teamid', validate='m:1')

    with PdfPages(save_loc) as pdf:

        for season in np.sort(df.season.unique()):
            df_tmp = df.query('season == @season').copy()
            df_tmp = df_tmp.sort_values('n_wins', ascending=False)[
                ['avg_scorediff_wteam', 'teamname', 'n_wins']].drop_duplicates()
            sns.barplot(x='avg_scorediff_wteam', y='teamname', data=df_tmp)
            plt.title(f'Average score difference sorted by winner {season}')
            plt.tight_layout()
            pdf.savefig()
            plt.close()

    pass


def avg_score_wteam_regseason(df, ref_teams):

    df['score_diff'] = df.wscore - df.lscore
    df = df.groupby(['season', 'wteamid']).score_diff.mean().reset_index()
    df = pd.pivot_table(data=df, values='score_diff', index=['wteamid'], columns='season').reset_index()

    col_old = [x for x in df.columns if x != 'wteamid']
    col_new = ['avg_seasonscore_' + str(x) for x in col_old ]
    rename_col = dict(zip(col_old, col_new))
    df = df.rename(columns=rename_col)

    # Get team names
    df = pd.merge(df, ref_teams, how='left', left_on='wteamid', right_on='teamid')

    return df


def plot_tour_vs_season(df_tour, df_season, ref_teams):

    save_loc = 'analysis/tour_vs_season.pdf'
    df_tour = pd.merge(df_tour, ref_teams, left_on='wteamid', right_on='teamid', validate='m:1')


    with PdfPages(save_loc) as pdf:
        for season in np.sort(df_tour.season.unique()):
            df_tmp = df_tour.query('season == @season').copy()
            df_tmp = df_tmp.sort_values('n_wins', ascending=False)[
                ['avg_scorediff_wteam', 'teamname', 'n_wins']].drop_duplicates()

            df_seas_tmp = df_season.filter(regex=f'teamname|{season - 1}').copy()

            # FInd common teams
            teams = list(df_tmp.teamname.unique())
            df_seas_tmp = df_seas_tmp[df_seas_tmp.teamname.isin(teams)].sort_values(f'avg_seasonscore_{season - 1}', ascending=False)

            fig, axes = plt.subplots(ncols=2)

            sns.barplot(x=f'avg_seasonscore_{season - 1}', y='teamname', data=df_seas_tmp, ax=axes[0])
            axes[0].set_title(f'Season average winning score: {season - 1}')
            sns.barplot(x='avg_scorediff_wteam', y='teamname', data=df_tmp, ax=axes[1])
            axes[1].set_title(f'Tournament average winning score: {season}')

            plt.tight_layout()
            pdf.savefig()
            plt.close()


    pass


def run():
    loc = 'data/imported/mncaatourneydetailedresults.pkl'

    # team names
    ref_teams = clean_names(pd.read_pickle('data/imported/mteams.pkl'))

    # Season results
    df_season = clean_names(pd.read_pickle('data/imported/mregularseasoncompactresults.pkl'))

    df_season = avg_score_wteam_regseason(df_season, ref_teams)
    df_season.to_pickle('data/processed/avg_seasonscore_yearly.pkl')



    df_tour = pd.read_pickle(loc)
    df_tour = clean_names(df_tour)

    df_tour = avg_diffscore_tournament(df_tour)

    # Plot
    plot_avg_score_tournaments(df_tour, ref_teams)
    plot_tour_vs_season(df_tour, df_season, ref_teams)



    pass


if __name__ == '__main__':

    os.chdir('..')
    pd.set_option('expand_frame_repr', False)

    run()