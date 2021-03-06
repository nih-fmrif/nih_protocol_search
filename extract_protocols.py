
# coding: utf-8

# # Scraping protocol descriptions

# ### Import packages

# In[1]:

from pathlib import Path
import pickle
import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup


# ### Define functions

# In[2]:

def add_link_to_protocol_query(df_protocols):
    query_base = 'https://clinicalstudies.info.nih.gov/cgi/cs/processqry2.pl?search1='
    query_tail = '&searchtype=e&SearchButton99a=Submit+Query'
    results_urls = []
    for prot in df_protocols.protocol_id:
        results_urls.append(query_base + prot + query_tail)
    df_protocols['link_1'] = results_urls
    return df_protocols


def get_pages_at_link_1(df_protocols):
    """Return the search query results webpages for each protocol (labeled link 1)"""
    pages_results = []
    for link in df_protocols.link_1:
        pages_results.append(requests.get(link))
    return pages_results


def scrape_results_of_queries(page_results, df_protocols):
    """With the page of results from each link_1, follow the link and extract all important information at the subsequent page"""
    links = []
    #from IPython.core.debugger import Tracer
    #Tracer()() #this one triggers the debugger
    for ii,page in enumerate(page_results):

        result_soup = BeautifulSoup(page.content, 'html.parser')
        # val = [link_element for  link_element in results_soup.select('html body div p a')][0]
        try:
            link_2 = result_soup.find_all('img')[2].find('a')['href']  
            next_page_soup = BeautifulSoup(requests.get(link_2).content, 'html.parser')
            info_text = '\n'.join(next_page_soup.find_all('img')[2].get_text().splitlines()[:-4])
            link_3 = next_page_soup.find_all('a')[2]['href']
        except:
            link_2, info_text, link_3 = (np.NaN for i in range(3))
            print('no protocol by found:' + page.url)
        df_protocols.loc[ii,'link_2']  = link_2
        df_protocols.loc[ii, 'link_3'] = link_3
        df_protocols.loc[ii, 'info_text'] = info_text
    
    return df_protocols


def get_prot_info_at_link_3(s):
    """Scrape the protocol page at link_3"""
    try:
        
        protocol_page = requests.get(s.link_3)
        df_prot = pd.read_html(protocol_page.text)
        s = pd.concat([s,
                       pd.Series(data=df_prot[0][1].tolist(),index=df_prot[0][0].tolist()),
                       pd.Series(data=df_prot[1].T[1].tolist(),index=df_prot[1].T[0].tolist())],
                      axis = 0)
    except:
        pass
    return s

def tidy_df_scraped(df_scraped):
    df_scraped = (df_scraped.iloc[:,df_scraped.columns == df_scraped.columns].
                  drop(['Number'], axis = 1).
                  set_index('protocol_id').
                  reset_index())
    return df_scraped
    

def scrape_set_of_protocols(input_protocols_df):
    """Given a set of protocols (as a dataframe), search and scrape available info at clinical studies.info.nih.gov """
    df_queries = add_link_to_protocol_query(input_protocols_df)
    page_results = get_pages_at_link_1(df_queries)
    df_scraped = scrape_results_of_queries(page_results, df_queries)
    df_scraped = df_scraped.apply(get_prot_info_at_link_3, axis = 1)
    df_scraped = tidy_df_scraped(df_scraped)

    return df_scraped


# ### Load protocol dataframes

# In[3]:

n_and_m = pd.read_csv('./protocols_unaccounted_n_and_m.csv')
not_n_and_m = pd.read_csv('./protocols_unaccounted_others.csv')
n_and_m.head()


# # Do the scraping
# 

# In[4]:

n_and_m_scraped = scrape_set_of_protocols(n_and_m)


# In[5]:

not_n_and_m_scraped = scrape_set_of_protocols(not_n_and_m)


# # Check the output
# 
# For protocols outside NIMH and NINDS we can check the number of protocols queried and the number of filled values for each category:

# In[6]:

len(not_n_and_m_scraped)


# In[7]:

not_n_and_m_scraped.count()


# 
# For protocols in NIMH and NINDS the number of protocols queried and the number of filled values for each category:

# In[8]:

len(n_and_m)


# In[9]:

n_and_m_scraped.count()


# # Write output

# In[10]:

# had to install some packages
# !conda install -y openpyxl
#!conda install -y jdcal
# !conda install -y et_xmlfile
n_and_m_scraped.to_excel(excel_writer="n_and_m_scraped.xlsx",sheet_name="scraped_protocols",na_rep="NA")


# In[11]:

not_n_and_m_scraped.to_excel(excel_writer="not_n_and_m_scraped.xlsx",sheet_name="scraped_protocols",na_rep="NA")
# can't get this to work well yet:
# not_n_and_m_scraped.to_csv(path_or_buf = 'not_n_and_m_scraped.csv') 

