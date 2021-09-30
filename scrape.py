import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
import json
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import re

# Windows users
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

mvp_url = 'https://www.baseball-reference.com/awards/mvp.shtml'
war_url = 'https://www.espn.com/mlb/war/leaders/_/type/seasonal/year/'

"""
    Scrape a web page and return data
    param: target_url - The URL to fetch data from (string)
    return: DataFrame containing data from page
"""
def getHtml(target_url: str) -> DataFrame:
    df = pd.read_html(target_url)

    mvp_list = pd.DataFrame(df[0])

    mvp_df = pd.DataFrame({
        'Year Won': np.array(mvp_list[( 'Unnamed: 0_level_0', 'Year')].values),
        'Name': np.array(mvp_list[( 'Unnamed: 2_level_0', 'Name')].values),
        'Team': np.array(mvp_list[( 'Unnamed: 3_level_0', 'Tm')].values),
        'WAR': np.array(mvp_list[( 'Unnamed: 4_level_0', 'WAR')].values)
    })

    mvp_df = mvp_df.dropna()
    mvp_df['Year Won'] = mvp_df['Year Won'].astype(str).apply(lambda x: x.replace('.0','')).astype(int)

    return mvp_df


## Main

mvp_df = getHtml(mvp_url)

mvp_df['Next Year'].apply(lambda x: x + 1)

new_df = mvp_df.loc[mvp_df['Year Won']>=1998]

next_war = []
for row in new_df.index:
    i = 51
    year = mvp_df['Next Year'][row]
    name = mvp_df['Name'][row]
    year_url = f'{war_url}{year}'
    war = ''
    print(f'{name} {year}')
    while i <= 201:
    #Can be while true?
        year_html = pd.read_html(year_url)
        year_df = pd.DataFrame(year_html[0])
        if year_df.loc[year_df[1] == name][2].empty and i != 151:
            year_url = f'https://www.espn.com/mlb/war/leaders/_/year/{year}/type/seasonal/alltime/false/count/{i}'
            i= i + 50
            print(f'{year} {i}')
        elif year_df.loc[year_df[1] == name][2].empty and i == 151:
            next_war.append(war)
            print(f'{year} {year}')
            break
        else:
            war = year_df.loc[year_df[1] == name][2].values[0]
            next_war.append(war)
            break

new_df['Next War'] = next_war