# Using Web Scraping to get a list of Care Based Organizations (CBOs) 

#Community-based organizations such as area agencies on aging (AAAs) and centers for independent 
#living (CILs) have served for decades as cost-effective, trusted, and proven resources for 
# addressing the health-related social needs of older adults and people with disabilities, 
#including long-term care needs.

# Importing key libraries
import requests
import re
import pandas as pd
import time
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import Tag


# Creating lists to store values for relevant columns
CBO_Name = []
CBO_Description = []
CBO_Location = []
CBO_Contact = []
CBO_Website = []
start_time = time.time()


# Reading data from an url
url = "https://www.dshs.wa.gov/esa/community-partnership-program/community-based-organizations-cbos-alphabet"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

#Subsetting for all CBOs heading
tag = soup.find_all("h3")

for  i in range(len(tag)-1):
    Name = tag[i].get_text()
    Description  = tag[i].next_sibling.next_sibling.get_text()
 #   Location  = tag[i].next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string
    try:
        Website = tag[i+1].previous_sibling.previous_sibling.a['href']
    except :
        Website = 'NA'
    try:
        if Website == 'NA':
            Contact = tag[i+1].previous_sibling.previous_sibling.string
            Location = tag[i+1].previous_sibling.previous_sibling.previous_sibling.previous_sibling.string

        else :
            Contact  = tag[i+1].previous_sibling.previous_sibling.previous_sibling.previous_sibling.string
            Location  = tag[i+1].previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.string
    except :
        Contact = 'NA'       
        Location = 'NA'

# Appending values in the initialied list
    CBO_Name.append(Name)
    CBO_Description.append(Description)
    CBO_Location.append(Location)
    CBO_Contact.append(Contact)
    CBO_Website.append(Website)

# Creating the final dataframe containing all key columns       
df=pd.DataFrame(CBO_Name,columns=['CBO_Name'])
df['CBO_Description']=CBO_Description
df['CBO_Location']=CBO_Location
df['CBO_Contact']=CBO_Contact
df['CBO_Website']=CBO_Website

# Writing dataframe to local
writer = pd.ExcelWriter('C:/Users/Pushpa/Desktop/Courses_Sem1/Python/Course Project/CBO_List_v4.xlsx')
df.to_excel(writer,'Sheet1',index = False)
writer.save()