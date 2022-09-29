#!/usr/bin/env python
# coding: utf-8

# ### 1.Importing all required libraries 

# In[36]:


from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import random
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import validators
from tqdm import tqdm
from colorama import Fore,Back
import itertools
import threading
import sys


# In[37]:


print(Fore.YELLOW+'''
  _   _ _       _          _____                                        ___   ___ ___  ___  
 | \ | (_)     (_)        / ____|                                      |__ \ / _ \__ \|__ \ 
 |  \| |_ _ __  _  __ _  | (___   ___ _ __ __ _ _ __  _ __   ___ _ __     ) | | | | ) |  ) |
 | . ` | | '_ \| |/ _` |  \___ \ / __| '__/ _` | '_ \| '_ \ / _ \ '__|   / /| | | |/ /  / / 
 | |\  | | | | | | (_| |  ____) | (__| | | (_| | |_) | |_) |  __/ |     / /_| |_| / /_ / /_ 
 |_| \_|_|_| |_| |\__,_| |_____/ \___|_|  \__,_| .__/| .__/ \___|_|    |____|\___/____|____|
              _/ |                             | |   | |                                    
             |__/                              |_|   |_|                                    
''')


# In[38]:


print(Fore.YELLOW+'ᴮʸ ᴿᵒʰⁱᵗ ᴮᵃⁱʳʷᵃ | ᴰᵉᵉᵖᵀʰᵒᵘᵍʰᵗˢ ᴱᵈᵘᵀᵉᶜʰ ⱽᵉⁿᵗᵘʳᵉˢ | ²⁰²²')


# In[71]:



#code to handle request and get source code   
def handleRequests(query):
    '''Returns HTML document'''

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"}
    try:
        request = requests.get(query, headers=headers, allow_redirects=False)
        return request.text
    except Exception:
        raise ConnectionError("Error occured while fetching data from the web, please try checking the internet connection.")



# Code to Scroll down site till bottom and get full source code
def ScrollPage():
    time.sleep(2)  # Allow 2 seconds for the web page to open
    scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    i = 1

    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height*1.2:
            break 

#function for loading animation
def loadanimation(page):
    print('*****************************')
    print(f'No of pages scrapped: {page}')
    print('')
    print('TotalJobs       :',len(name_of_job))
    print('Total Company   :',len(company_name))
    print('Total locations :',len(location))
    print('Time posted     :',len(time_posted))
    print('About_links     :',len(company_about))     


# In[53]:


driver = webdriver.Chrome('chromedriver')


# In[40]:


searchkey_url="https://www.linkedin.com/jobs/search/?currentJobId=3279113515&keywords=software%20developer&refresh=true"

print(Fore.GREEN+"Default URL :"+searchkey_url)



print(Fore.GREEN+'x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x')
print("")
print('Enter URL                  [1]')
print('Go With Default Url        [2]')
print('Search Custom Jobs Details [3]')

choice = int(input("Enter Your Choice : "))

if choice == 1:
    searchkey_url= input("Enter URL :")

elif choice == 2:
    print("Default URL :"+searchkey_url)

elif choice == 3:
    custom_search = input('Enter Custom Search :')
    custom_loc=input('Enter location :')
    #opening linkedin site
    driver.get('https://www.linkedin.com/jobs/search?position=1&pageNum=0')
    search_key = driver.find_element_by_xpath('/html/body/div[1]/header/nav/section/section[2]/form/section[1]/input')
    search_key.send_keys(custom_search)
    driver.find_element_by_xpath('/html/body/div[1]/header/nav/section/section[2]/form/section[2]/button').click()
    search_loc = driver.find_element_by_xpath('/html/body/div[1]/header/nav/section/section[2]/form/section[2]/input')
    search_loc.send_keys(custom_loc)
    driver.find_element_by_xpath('/html/body/div[1]/header/nav/section/section[2]/form/button').click()
    searchkey_url=driver.current_url
    print('Current Page URL :',searchkey_url)
    


# In[41]:


time.sleep(2)
driver.get(searchkey_url)
driver.maximize_window()
ScrollPage()
src=driver.page_source
soup=BeautifulSoup(src,"lxml")

links = []
for link in soup.findAll('a',{'class':'base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]'}):
    links.append(link.get('href'))


# In[72]:


name_of_job=[]
company_name=[]
location=[]
time_posted=[]
company_about=[]
company_real_about = []

print(f'Found a total of {len(links)} pages')
print('')
number_of_jobs_detail=int(input('How many pages you wants to scrap??:'))
page=0

for i in tqdm(range(number_of_jobs_detail)):
    urls=links[i]
    data2 =handleRequests(urls)
    soup2=BeautifulSoup(data2,"lxml")
    try:
        n=soup2.find('div', {'class':'top-card-layout__entity-info flex-grow flex-shrink-0 basis-0 babybear:flex-none babybear:w-full babybear:flex-none babybear:w-full'})
        title=n.find('h1',{'class':'top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title'})
        if(title):
            name_of_job.append(title.get_text(" ", strip=True))
        else:
            name_of_job.append('Not Available')
    except Exception:
        pass
    
    
    try:
        com=n.find('span',{'class':'topcard__flavor'})
        if(com):
            company_name.append(com.get_text("",strip=True))
        else:
            company_name.append('Not Available')
    except Exception:
        pass
    
    try:
        loc=n.find('span',{'class':'topcard__flavor topcard__flavor--bullet'})
        if(loc):
            location.append(loc.get_text(" ", strip=True))
        else:
            location.append('Not Available')
    except Exception:
        pass
    
    try:
        q=soup2.find('span',{'class':'posted-time-ago__text topcard__flavor--metadata'})
        if(q):
            time_posted.append(q.get_text(" ", strip=True))
        else:
            time_posted.append('Not Available')
    except Exception:
        pass
    
    try:
        comdetial=n.find('a',{'class':'topcard__org-name-link topcard__flavor--black-link'})
        if(comdetial):
            company_about.append(comdetial.get('href'))
        else:
            company_about.append('Not Available')
    except Exception:
        pass
    
    page +=1


print('')
loadanimation(page)


# In[43]:


for i in range(number_of_jobs_detail):
    url3=company_about[i].split('?')
    company_real_about.append(url3[0]+'/about')


# In[54]:



#opening linkedin site
driver.get("https://linkedin.com/uas/login")

#giving wait time of 3 second so that page can load properly
time.sleep(3)
#reading user id and password from config file
file=open('config.txt')
lines=file.readlines()

email=lines[0]
passwordd=lines[1]


username = driver.find_element_by_id("username")
username.send_keys(email)

time.sleep(1)

pword = driver.find_element_by_id("password")
pword.send_keys(passwordd)


driver.find_element_by_xpath("//button[@type='submit']").click()


# In[55]:


Company_offical_website=[]
for i in tqdm(range(number_of_jobs_detail)):
    url4=company_real_about[i]
    driver.get(url4)
    src3=driver.page_source
    soup3=BeautifulSoup(src3,"lxml")
    website_link=soup3.find('a',{'class':'link-without-visited-state ember-view'})
    industry=soup3.find('a',{'class':'link-without-visited-state ember-view'})
    if(website_link):
        if validators.url(website_link.get('href')) is True:
            Company_offical_website.append(website_link.get('href'))
        else:
            Company_offical_website.append('Not Available')
        
    else:
        Company_offical_website.append('Not Available')

driver.close()


# ### Final : Creating a csv files 

# In[57]:


dict = {"Job Name": name_of_job, "Company Name": company_name,
        "Location": location,"Time Posted":time_posted,"About Links":company_about,'Official Website':Company_offical_website}

df = pd.DataFrame(dict)


# In[58]:



FILE_NAME ='LINKEDIN DATA SCRAPPED BY NINJA SCRAPPER 2022.csv'

df.to_csv('LINKEDIN DATA SCRAPPED BY NINJA SCRAPPER 2022.csv')

print(Fore.GREEN+'CSV File Saved By Name ::',end='')
print(Fore.WHITE+Back.GREEN+FILE_NAME)

