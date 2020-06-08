import pandas as pd
import numpy as np

# CSVs From pick 224
# PLayers stats from their draft years. The 2009-2015 drafts are included in this dataset.


def create_chl_dataframe(chl_csv):
    chl_stats_df = pd.read_csv(chl_csv)
    # Creating a new dataframe that just consists of certain columns from the chl_stats_df
    chl_stats_trunc_df = pd.DataFrame()
    chl_stats_trunc_df['Name'] = chl_stats_df['NAME']
    chl_stats_trunc_df['CHL_GP'] = chl_stats_df['GP']
    chl_stats_trunc_df['CHL_Points'] = chl_stats_df['TP']
    chl_stats_trunc_df['CHL_PointsPG'] = chl_stats_df['TP/GP']
    chl_stats_trunc_df['CHL_EV_P1/GP'] = chl_stats_df['EV P1/GP']
    chl_stats_trunc_df['CHL_EV_P1/60'] = chl_stats_df['P1/e60']
    chl_stats_trunc_df['CHL_EV_RelGF%'] = chl_stats_df['EV GF%Rel']
    chl_stats_trunc_df['CHL_Age_Dec31'] = chl_stats_df['AGE DEC 31']

    return chl_stats_trunc_df


def create_nhl_dataframe(nhl_csv):
    nhl_stats_df = pd.read_csv(nhl_csv)

    # Removing the unecessary information from the Player Column
    nhl_stats_df['Player'] = nhl_stats_df['Player'].str.lower()
    nhl_stats_df['Player'] = nhl_stats_df['Player'].str.split('\\')
    nhl_stats_df['Player_temp'] = nhl_stats_df['Player'].str[0]
    nhl_stats_df['Player'] = nhl_stats_df['Player_temp']
    nhl_stats_df = nhl_stats_df.drop(['Player_temp'], axis=1)
    nhl_stats_df['Player'] = nhl_stats_df['Player'].str.title()

    # Rename 'Player' column to match the column name from the OHL dataframe
    nhl_stats_df = nhl_stats_df.rename(columns={"Player": "Name"})

    # dropping unecessary columns from the nhl_2015_df
    nhl_stats_df = nhl_stats_df.drop(
        ['To', 'Age', 'PIM', 'GP.1', 'W', 'L', 'T/O', 'SV%', 'GAA', 'PS'], axis=1)

    # Creating a new column for NHL points per game
    nhl_stats_df['NHL_PointsPG'] = nhl_stats_df['PTS']/nhl_stats_df['GP']

    return nhl_stats_df


def merge_dataframes(ohl_df, whl_df, qmjhl_df, nhl_df):

    # Concatenating all the CHL dataframes into one to prep for a merge
    chl_df = pd.concat([ohl_df, whl_df, qmjhl_df])

    # Merging the NHL dataframe with the CHL dataframe so that we have both their junior league
    # and NHL stats in one dataframe
    overall_stats_df = pd.merge(nhl_df, chl_df)

    overall_stats_df.to_csv('nhl_f_combined_junior_pro_stats.csv')

    return overall_stats_df


ohl_df = create_chl_dataframe('ohl_f_09-15.csv')
# print(ohl_df.head())
whl_df = create_chl_dataframe('whl_f_09-15.csv')
# print(whl_df.head())
qmjhl_df = create_chl_dataframe('qmjhl_f_09-15.csv')
# print(qmjhl_df.head())
nhl_df = create_nhl_dataframe('nhl_stats_2009-2015_drafts.csv')
# print(nhl_df.head())
overall_df = merge_dataframes(ohl_df, whl_df, qmjhl_df, nhl_df)
# print(overall_df.head())

# create truncated csv file for 2020 draft class
(create_chl_dataframe('chl_f_2020.csv')).to_csv('chl_f_2020_trunc.csv')
