
# coding: utf-8

# # Attempt at scraping NIMH protocols

# In[1]:

from IPython.core.debugger import Pdb; ipdb=Pdb()


# In[ ]:

import requests
page = requests.get("https://clinicalstudies.info.nih.gov/cgi/protinstitute.cgi?NIMH.0.html")
# a status code of 200 indicates the page was downloaded successfully
page


# In[ ]:

page.content


# In[ ]:

from bs4 import BeautifulSoup
soup = BeautifulSoup(page.content, 'html.parser')


# In[ ]:

print(soup.prettify())


# In[ ]:

[type(item) for item in list(soup.children)] 


# In[ ]:

# import bs4
# test = list(soup.children)[2]
# list(test.strings)
# type(test) is bs4.element.Tag



# In[ ]:

html = list(soup.children)[4]
#list(html.children)
html


# In[ ]:

body = list(html.children)[1]
body = list(body.children)[2]
body = list(body.children)[2]
#[type(item) for item in body.children]
p = list(body.children)[2]
p.get_text().splitlines()



# In[ ]:

soup2 = BeautifulSoup(page.content, 'html.parser')
all_the_p = soup2.find_all('p')
len(all_the_p)


# In[ ]:

all_text = soup2.find_all('p')[0].get_text()
#print(all_text)
all_text.split('\n\n\n')


# # Another approach using css selectors

# In[ ]:

print(soup.select("dl"))


# # A more manual approach

# In[ ]:

import pandas as pd

n_and_m = pd.read_csv('./protocols_unaccounted_n_and_m.csv')
query = ' OR '.join(n_and_m.protocol_id)

not_n_and_m = pd.read_csv('./protocols_unaccounted_others.csv')
query2 = ' OR '.join(not_n_and_m.protocol_id)
n_and_m


# ### Entered query at clinicalstudies.info.nih.gov:

# In[ ]:

query




# In[ ]:

url = 'https://clinicalstudies.info.nih.gov/cgi/cs/processqry2.pl?search1=01-M-0185+OR+01-M-0232+OR+02-M-0239+OR+03-M-0093+OR+03-M-0108+OR+05-M-0105+OR+06-M-0065+OR+06-M-0102+OR+08-M-0211+OR+09-M-0034+OR+09-M-0171+OR+09-M-0176+OR+10-M-0068+OR+11-M-0058+OR+11-M-0104+OR+13-M-0004+OR+14-M-0085+OR+15-M-0151+OR+15-M-0188+OR+89-M-0160+OR+00-N-0043+OR+00-N-0089+OR+00-N-0140+OR+02-N-0128+OR+04-N-0071+OR+07-N-0063+OR+07-N-0072+OR+07-N-0122+OR+08-N-0027+OR+08-N-0044+OR+08-N-0161+OR+08-N-0215+OR+09-N-0117+OR+09-N-0118+OR+09-N-0182+OR+10-N-0121+OR+10-N-0122+OR+10-N-0212+OR+11-N-0116+OR+11-N-0182+OR+12-N-0033+OR+12-N-0123+OR+13-N-0047+OR+13-N-0104+OR+13-N-0115+OR+13-N-0135+OR+14-N-0069+OR+14-N-0083+OR+16-N-0064+OR+16-N-0072+OR+16-N-0170+OR+93-N-0202&searchtype=e&SearchButton99a=Submit+Query'
# returns 01-M-0185,01-M-0232, 02-M-0239, 03-M-0093 


# ### Entered query2 at clinicalstudies.info.nih.gov:

# In[ ]:


query2


# In[ ]:

url = 'https://clinicalstudies.info.nih.gov/cgi/cs/processqry2.pl?search1=05-AA-0121+OR+08-AA-0137+OR+08-AA-0178+OR+10-AA-0046+OR+11-AA-0010+OR+12-AA-0032+OR+12-AA-0143+OR+13-AA-0043+OR+15-AA-0031+OR+15-AA-0127+OR+15-AA-0203+OR+16-AA-0037+OR+16-AA-0059+OR+16-AA-0080+OR+98-AA-0009+OR+98-AA-0056+OR+03-AR-0173+OR+14-AT-0054+OR+15-AT-0132+OR+01-C-0070+OR+01-C-0157+OR+01-C-0158+OR+03-C-0241+OR+03-C-0277+OR+03-C-0278+OR+03-C-0278E+OR+06-C-0219+OR+08-C-0079+OR+10-C-0219+OR+11-C-0047+OR+11-C-0161+OR+13-C-0152+OR+99-C-0088+OR+10-CC-0115+OR+10-CC-0118+OR+10-CC-0214+OR+11-CC-0120+OR+90-CC-0168+OR+91-CC-0117+OR+98-CC-0019+OR+00-CH-0093+OR+00-CH-0160+OR+11-CH-0239+OR+12-CH-0050+OR+98-CH-0081+OR+10-DC-0211+OR+92-DC-0178+OR+97-DC-0057+OR+11-DK-0168+OR+99-DK-0002+OR+03-E-0099+OR+08-EI-0169+OR+16-EI-0090+OR+02-H-0050+OR+07-H-0030+OR+10-H-0126+OR+13-H-0065+OR+16-H-0144+OR+94-H-0010+OR+11-HG-0207+OR+15-HG-0130+OR+76-HG-0238+OR+94-HG-0105+OR+07-I-0033+OR+09-I-0049+OR+10-I-0148+OR+14-I-0206+OR+93-I-0106+OR+93-I-0119+OR+09-NR-0088&searchtype=e&SearchButton99a=Submit+Query'
# returns 08-AA-0178, and 10-AA-0046


# In[ ]:

# !conda install -y html5lib


# # Failed attempt at url generation
# 

# In[ ]:

query_base = 'https://clinicalstudies.info.nih.gov/cgi/detail.cgi?A_'
pages = []
for prot in n_and_m.protocol_id:
    query_tail = '.html'
    if int(prot[:2]) >17:
        century = '19'
    else:
        century = '20'

    url = query_base + century + prot + query_tail
    print(url)
    pages.append(requests.get(url))


# In[ ]:

pages


# # Using the query page and following the links

# In[ ]:

from pathlib import Path
import pickle
import pandas as pd
import requests
import numpy as np


# In[ ]:

n_and_m = pd.read_csv('./protocols_unaccounted_n_and_m.csv')
not_n_and_m = pd.read_csv('./protocols_unaccounted_others.csv')


# In[173]:

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


def scrape_set_of_protocols(input_protocols_df):
    """Given a set of protocols (as a dataframe), search and scrape available info at clinical studies.info.nih.gov """
    try:
        with Path('page_results').open('rb') as f:
            page_results = pickle.load(f)
    except:
        page_results = get_results_of_queries(input_protocols_df)
        with Path.cwd().joinpath('page_results').open("wb") as f:
            pickle.dump(page_results, f, pickle.HIGHEST_PROTOCOL)

    df_scraped = scrape_results_of_queries(page_results, input_protocols_df)
    df_scraped = df_scraped.apply(get_prot_info_at_link_3, axis = 1)
    return df_scraped


# In[ ]:




# In[176]:

get_ipython().system('git status')


# In[3]:

print('hello')


# In[ ]:



