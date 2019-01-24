#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: Investigate a Movie Review Dataset
# 
# 

# In[1]:



import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# Load your data and print out a few lines. Perform operations to inspect data
df = pd.read_csv('tmdb-movies.csv')
df.head(5)


# In[3]:


#1. drop off columns won't be used at this analysis project, and check N/A
df = df.drop(['cast','homepage','tagline','keywords','overview','budget_adj','revenue_adj','imdb_id'],axis=1)
df.info()


# In[4]:


#2. drop off whole row if director is n/a
df = df.dropna(subset=['director']) 


# In[5]:


#3. create dataframe for analysis generes
df_genres = df.dropna(subset=['genres']) 
#split column genres by |
df_genres_split = df_genres['genres'].str.split("|", expand=True)


# In[6]:


#4. Creat dataframe for analysis release date
df_release_date_split =  df['release_date'].str.split("/",  expand=True)


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# ### Research Question 1: Popularity

# In[7]:


#1.take a look at Popularity
plt.hist(df['popularity'],density=1,bins=30)
df["popularity"].describe()


# In[8]:


#2. Popularity Vs revenue
plt.scatter(df['popularity'],df['revenue'],s=4)
plt.xlabel('Popularity')
plt.ylabel('revenue')
plt.xlim((0,20))
plt.ylim((0,1000000000))


# In[9]:


#3. Popularity Vs Budget
plt.scatter(df['popularity'],df['budget'],s=4)
plt.xlabel('Popularity')
plt.ylabel('Budget')
plt.xlim((0,20))


# In[10]:


#4. Popularity Vs runtime
plt.scatter(df['popularity'],df['runtime'],s=4)
plt.xlabel('Popularity')
plt.ylabel('runtime')


# ### Research Question 2  (Vote average)

# In[12]:


#1. inspection for vote average
df['vote_average'].describe()
plt.hist(df['vote_average'],density=1,bins=30)


# In[13]:


#2. Popularity Vs vote average
plt.scatter(df['popularity'],df['vote_average'],s=4)
plt.xlabel('Popularity')
plt.ylabel('vote_average')


# In[14]:


#3. budget Vs vote average
plt.scatter(df['budget'],df['vote_average'],s=4)
plt.xlabel('budget')
plt.ylabel('vote_average')


# In[15]:


#4. relese month Vs. Vote average
import numpy as np
df_release_date_split['vote_average']= df['vote_average']
df_month_voteavg=pd.DataFrame(df_release_date_split.groupby(0).mean()['vote_average'])   #transfer series to dataframe
df_month_voteavg['month']=df_month_voteavg.index  #generate column instead of index
df_month_voteavg['month'] = df_month_voteavg['month'].astype(int) # change datatype object into int
df_month_voteavg = df_month_voteavg.sort_values(by=['month'])


# In[16]:


#add count
df_month_count = pd.DataFrame(df_release_date_split.groupby(df_release_date_split[0]).count()[1])
df_month_count['month']=df_month_count.index.astype(int)
df_month_count = df_month_count.sort_values(by=['month'])
df_month_voteavg['film count'] = df_month_count[1]


# In[17]:


df_month_voteavg


# In[18]:


fig = plt.figure() # Create matplotlib figure

ax = fig.add_subplot(111) # Create matplotlib axes
ax2 = ax.twinx() # Create another axes that shares the same x-axis as ax.



df_month_voteavg['vote_average'].plot(kind='line', color='red', ax=ax2,label = 'vote_average')
df_month_voteavg['film count'].plot(kind='bar', color='blue', ax=ax,label = 'film count')

ax.set_ylabel('file count')
ax2.set_ylabel('vote_average')
ax.set_xlabel('month')
ax.legend()


# In[19]:


#5. relese year Vs. Vote average
#inspect how many years 
df.groupby(df['release_year']).count()['id']
#decide we only use the data after year 2000
df_release_year = df[df['release_year']>=1990]
#average vote for every year

df_release_year.groupby(df_release_year['release_year']).mean()['vote_average'].plot(kind='line', color='blue')
plt.ylabel('vote_average')


# In[20]:


### Research Question 3: Director Analysis


# In[21]:


#5 most high productive director
df_top5_director_pro = df.groupby(df['director']).count()['id'].reset_index().sort_values('id', ascending=False).head(5) #.reset_index()make it back to df
df_top5_director_pro.rename(columns={'id':'#_of_movie'},inplace=True)

df_direct_vote_avg = df.groupby('director').mean()['vote_average'].reset_index()
#make a table                                                                    
df_top5_director_avg = df_direct_vote_avg[(df_direct_vote_avg['director'] == 'Woody Allen')
                  | (df_direct_vote_avg['director'] == 'Clint Eastwood') 
                  | (df_direct_vote_avg['director'] == 'Steven Spielberg')
                  | (df_direct_vote_avg['director'] == 'Martin Scorsese') 
                  | (df_direct_vote_avg['director'] == 'Ridley Scott') ]
df_top5_director_avg['number_of_movie']=df_top5_director_pro['#_of_movie']
df_top5_director_avg.sort_values(['vote_average'])


# In[22]:


### Research Question 4: Genres Analysis
#1.column 0
df_genres_split['vote_average']=df['vote_average']
df_genres_split_vote_avg0 = df_genres_split.groupby(df_genres_split[0]).sum().reset_index()
df_genres_split_count = df_genres_split.groupby([0]).size().reset_index(drop=True).reset_index()
df_genres_split_vote_avg0['count']=df_genres_split_count[0]
df_genres_split_vote_avg0 = df_genres_split_vote_avg0.rename(columns={'vote_average':'vote_average0','count':'count0',0:'name'})
#2.Column 1
df_genres_split_vote_avg1 = df_genres_split.groupby(df_genres_split[1]).sum().reset_index()
df_genres_split_count1 = df_genres_split.groupby([1]).size().reset_index(drop=True).reset_index()
df_genres_split_vote_avg1['count']=df_genres_split_count1[0]
df_genres_split_vote_avg1 = df_genres_split_vote_avg1.rename(columns={'vote_average':'vote_average1','count':'count1',1:'name'})
#3.Column 2 
df_genres_split_vote_avg2 = df_genres_split.groupby(df_genres_split[2]).sum().reset_index()
df_genres_split_count2 = df_genres_split.groupby([2]).size().reset_index(drop=True).reset_index()
df_genres_split_vote_avg2['count']=df_genres_split_count2[0]
df_genres_split_vote_avg2 = df_genres_split_vote_avg2.rename(columns={'vote_average':'vote_average2','count':'count2',2:'name'})
#4.Column 3
df_genres_split_vote_avg3 = df_genres_split.groupby(df_genres_split[3]).sum().reset_index()
df_genres_split_count3 = df_genres_split.groupby([3]).size().reset_index(drop=True).reset_index()
df_genres_split_vote_avg3['count']=df_genres_split_count3[0]
df_genres_split_vote_avg3 = df_genres_split_vote_avg3.rename(columns={'vote_average':'vote_average3','count':'count3',3:'name'})
#5.Column 4
df_genres_split_vote_avg4 = df_genres_split.groupby(df_genres_split[4]).sum().reset_index()
df_genres_split_count4 = df_genres_split.groupby([4]).size().reset_index(drop=True).reset_index()
df_genres_split_vote_avg4['count']=df_genres_split_count4[0]
df_genres_split_vote_avg4 = df_genres_split_vote_avg4.rename(columns={'vote_average':'vote_average4','count':'count4',4:'name'})


# In[23]:


dfs_genres = [df_genres_split_vote_avg0,df_genres_split_vote_avg1,df_genres_split_vote_avg2,df_genres_split_vote_avg3,df_genres_split_vote_avg4]
from functools import reduce
df_genres_final = reduce(lambda left,right:pd.merge(left,right,on='name'),dfs_genres)

df_genres_avg = (df_genres_final['vote_average0']+
                df_genres_final['vote_average1']+
                df_genres_final['vote_average2']+
                df_genres_final['vote_average3']+
                df_genres_final['vote_average4']).divide((df_genres_final['count0']+df_genres_final['count1']+df_genres_final['count2']+df_genres_final['count3']+
                df_genres_final['count4']))
df_genres_final['Average_vote_avg'] = df_genres_avg
df_genres_final['Total_count'] = df_genres_final['count0']+df_genres_final['count1']+df_genres_final['count2']+df_genres_final['count3']+df_genres_final['count4']
df_genres_final.sort_values(by='Average_vote_avg',ascending=False)[['name','Average_vote_avg','Total_count']]


# In[24]:


df.info()


# In[25]:


#Population
#1. The distribution of Population is a right-skewed distribution, which represents the majority 
#of the popularity is at the lower score side. 
#2. Popularity Vs revenue: Popularity and Revenue have positive relation.
#3. Popularity Vs Budget: Popularity and Budget have positive relation.
#4. Popularity Vs runtime: They don't have significant relation
#Vote Average
#1. The distribution of Vote Average is more like a normal standtard distribution, The majority of the vote average is between 5-7
#2. Popularity Vs vote average： There are a weak positive relation between them
#3. budget Vs vote average: There are a weak positive relation between them
#4. relese month Vs. Vote average： i.According to the plot, month Sep. has the largest volumn of movie released, and has a relative high vote_average. 
#                                  ii.March to April, June to August and September to October jump dramatically. 
#5. relese year Vs. Vote average: I only consider movies released after 1990. According to the plot, audiences' vote_average has been decreasing fluctuatly.
# Director Analysis
#1. Top 5 directors with the most production: Woody Allen, Ridley Scott, Clint Eastwood, Steven Speilberg, Martin Scorsese
#2. Among these 5 directors, Woody Allen has directed the most amount of movives but with a lowest vote_average. Martin Scorsese has directed the least amount of movives but has the highest vote_average
#Genres Analysis
#1. Music and History have the highest Average Vote across the past several years, but with a relative low production.
#2. Drama genres performs well, considering the relative high average vote and big production. 
#3. Sciece Fiction and Horror genres movies scored the lowest.
#4. War genres has the most market potential, considering the low production and good average vote reputation.


# In[ ]:





# <a id='conclusions'></a>
# ## Conclusions
# 
# > **Tip**: Finally, summarize your findings and the results that have been performed. Make sure that you are clear with regards to the limitations of your exploration. If you haven't done any statistical tests, do not imply any statistical conclusions. And make sure you avoid implying causation from correlation!
# 
# > **Tip**: Once you are satisfied with your work here, check over your report to make sure that it is satisfies all the areas of the rubric (found on the project submission page at the end of the lesson). You should also probably remove all of the "Tips" like this one so that the presentation is as polished as possible.
# 
# ## Submitting your Project 
# 
# > Before you submit your project, you need to create a .html or .pdf version of this notebook in the workspace here. To do that, run the code cell below. If it worked correctly, you should get a return code of 0, and you should see the generated .html file in the workspace directory (click on the orange Jupyter icon in the upper left).
# 
# > Alternatively, you can download this report as .html via the **File** > **Download as** submenu, and then manually upload it into the workspace directory by clicking on the orange Jupyter icon in the upper left, then using the Upload button.
# 
# > Once you've done this, you can submit your project by clicking on the "Submit Project" button in the lower right here. This will create and submit a zip file with this .ipynb doc and the .html or .pdf version you created. Congratulations!
# 

# In[26]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




