#!/usr/bin/env python
# coding: utf-8

# # Analyzing what affects the number of cab rides in a given 2 year period to decide which company to invest in.

# In[1]:


#Importing pandas
import pandas as pd
#Importing numpy
import numpy as np
# Importing matplotlib
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
#Importing seaborn
import seaborn as sns


# ## Part 1:- Data Glacier datasets EDA

# In[2]:


#Importing the datasets provided by Data Glacier
#Importing cab data
df1 = pd.read_csv('Cab_Data.csv')
#Importing city data
df2 = pd.read_csv('City.csv')
#Importing customer ID data
df3 = pd.read_csv('Customer_ID.csv')
#Importing transaction ID data
df4 = pd.read_csv('Transaction_ID.csv')
#Creating a list for these dataframes
dgdfs = [df1, df2, df3, df4]
#Naming what these dataframes contain
dgdfnames = ["All the data", "Data about the cities", "Data about the customers", "Data for the transactions"]


# In[3]:


#Looking at the shape of the dataframes
datashape = [x.shape for x in dgdfs]
for (x,y) in zip(dgdfnames, datashape):
    print(x + " : " + str(y))


# The main dataframe has 359392 rows and 7 columns. There are 20 rows and 3 columns for the city data, 49171 rows and 4 columns in the customer data and 440098 and 3 columns in the data about each transaction. 

# In[4]:


#Looking at the shape of the dataframes
datasize = [x.memory_usage(deep=True).sum() for x in dgdfs]
for (x,y) in zip(dgdfnames, datasize):
    print(x + " : " + str(y))


# The observations above are in binary bytes. Thus, I will convert them to a human readable format and then pass in this list.

# In[5]:


#This function is defined to convert a size in bytes to a human-readable format in KB, MB, or GB

def convert_size(size_bytes):

    KB = 1024
    MB = KB ** 2
    GB = KB ** 3

    if size_bytes >= GB:
        size_str = f"{size_bytes / GB:.2f} GB"
    elif size_bytes >= MB:
        size_str = f"{size_bytes / MB:.2f} MB"
    elif size_bytes >= KB:
        size_str = f"{size_bytes / KB:.2f} KB"
    else:
        size_str = f"{size_bytes} bytes"
    return size_str


# In[6]:


for x in datasize:
    finaldatasize = convert_size(x)
    print(finaldatasize)


# The dataset with all the data has a size of 59.92 MB, the city dataset has a size of 4.03 KB, the customer dataset has a size of 4.03 MB and the transactions dataset has a size of 32.32 MB.

# In[7]:


#Printing out the column names for each dataframe
datacolumns = [x.columns for x in dgdfs]
for (x,y) in zip(dgdfnames, datacolumns):
    print(x + " : " + str(y))


# The column names are 'Transaction ID', 'Date of Travel', 'Company', 'City', 'KM Travelled',  'Price Charged' and 'Cost of Trip' 
# for the main dataframe, City', 'Population' and 'Users' for the data about cities, 'Customer ID', 'Gender', 'Age' and 'Income (USD/Month)' for the data about customers and 'Transaction ID', 'Customer ID', 'Payment_Mode' for the data about transactions.

# In[8]:


#Looking at some general information for these columns in these dataframes
datainfo = [x.info() for x in dgdfs]
print(datainfo)


# By looking into these tables, we can see that df1 is the raw data for every single ride and the next three tables are related to the first table by including specific information on the cities, customers and transactions of these rides. 

# There is not a single null value in the entire dataframe. In the main dataframe, there are 7 variables, 2 of which are categorical variables('Company' and 'City'), 2 int64 variables('Transaction ID' and 'Date of Travel') and finally 3 float64 variables('KM Travelled', 'Cost of Trip' and 'Price Charged'). In the city dataframe, all the columns are categorical. In the customer dataframe, everything is of the int64 data type except gender which is categorical and the same is true for the transaction dataframe where the categorical variable is the Payment_Mode. We will need to convert the Date of Travel column from an int64 datatype to a date datatype.

# In[9]:


#These lines of code are used to convert the 'Date of Travel' column from an int64 data type to a date data type
#Importing the datetime model
import datetime

#Creating a function to convert the dates from int64 to date objects
def to_date(x):

    # Add the number of days to January 1, 1900 to get the corresponding date
    date_obj = datetime.datetime(1900, 1, 1) + datetime.timedelta(x - 2)
    return date_obj

#Creating an empty list
y = []

#This loop converts the date values from an int64 list to a list of date objects
for x in df1['Date of Travel']:
    a = to_date(x)
    y.append(a)
    
#Dropping the date of travel column    
df1 = df1.drop(columns='Date of Travel', axis=1)

#Adding a new column to the dataframe
df1['Date of Travel'] = pd.Series(y)

#Replacing the old data frame with a new one
dgdfs.pop(0)
dgdfs.insert(0, df1)

#Viewing the dataframe
print(df1)


# In[10]:


#Taking a high-level look at all the data's first twenty rows for all twenty rows
dataskim = [x.head(n=20) for x in dgdfs]
for (x,y) in zip(dgdfnames, dataskim):
    print(x + " : " + str(y))


# In[11]:


#Looking at basic summary statistics
datastats = [x.describe() for x in dgdfs]
for (x,y) in zip(dgdfnames, datastats):
    print(x + " : " + str(y))


# Here are the most interesting insights from the numerical data we did not already know:-
# 1) The median km travelled is 22.4 whereas the mean is 22.6 in addition to a standard deviation of 12.2.
# 2) The median price charged is $386.4, the mean is 423.4 and the numbers have a standard deviation of 274.4. This suggests the highest prices are a lot further from the mean than the lowest prices(2048 vs 15.6)
# 3) The cost of the trip is much more uniformly distributed with there being a mean of 286.2, a median of 282.5 and a standard deviation of 158.
# 4) New York City has the highest population with 8405837 people and 302149 users.
# 5) The average age of the customers is 35.4 and the median is 33. The standard deviation is 12.6.
# 6) The average income is 15015.6 with a median of 14656 and a standard deviation of 8002.2.
# 7) The customer IDs range from 1 to 60000.

# In[12]:


#Taking a high-level look at all the data's first twenty rows for all twenty rows
datastats = [x.describe(include="object") for x in dgdfs]
for (x,y) in zip(dgdfnames, datastats):
    print(x + " : " + str(y))


# Interesting insights:-
# 1) Yellow cabs have the highest number of users with 274681 and New York City had 99885 users.
# 2) There are more males than females(26562 vs 22609).
# 3) More transactions are done in card than cash(177907).

# In[13]:


#Looking at the total number of values of each column
for (x,y) in zip(dgdfs, datacolumns):
    for z in y:
        a = x[[z]].value_counts()
        print(a)


# Interesting insights:-
# 1) All transactions had a unique ID.
# 2) The most common date of travel was 2018-01-05 with 2022 unique results.
# 3) Chicago, LA, DC and Boston were the next highest users of cabs.
# 4) The most common price charged was $298.32.
# 5) The trip cost $362.88.
# 6) 20 year olds were the most common users of taxis followed by 34, 39 and 23 year olds in this data.

# In[14]:


#Looking at the percentage of each value in each column
for (x,y) in zip(dgdfs, datacolumns):
    for z in y:
        a = x[[z]].value_counts(normalize = True)
        print(a)


# Interesting insights:-
# 1) 76.4% of users used yellow cabs.
# 2) 27.8% of users rode in New York City.
# 3) 0.43% of users travelled 33.6 km.
# 4) 0.005% of users were charged $298.32 or $191.72 which were the most common prices.
# 5) 0.052% and 0.051% of trips cost $362.88 or $479.808 which were the most common observations.
# 6) 54% of riders were men.
# 7) 3.33% of riders were 20 years old.
# 8) The most common income was $8497 which had 0.02 percent of incomes.

# ## Part 2:- External datasets EDA

# In[15]:


#Importing external datasets
#Importing cab data
df5 = pd.read_csv('inflationrate.csv')
#Importing city data
df6 = pd.read_csv('macroeconomics.csv')
#Importing customer ID data
df7 = pd.read_csv('US Holiday Dates (2004-2021).csv')
#Creating a list for these dataframes
extdfs = [df5, df6, df7]
#Naming what these dataframes contain
extdfnames = ["Inflation data", "Macroeconomic data", "Holiday data"]


# In[16]:


#Looking at the shape of the dataframes
datashape = [x.shape for x in extdfs]
for (x,y) in zip(extdfnames, datashape):
    print(x + " : " + str(y))


# The inflation data has 123 rows and 3 columns. The macroeconomic data has 499 rows and 8 columns. The holiday data has 342 rows and 6 columns.

# In[17]:


#Looking at the size of the dataframes
datasize = [x.memory_usage(deep=True).sum() for x in extdfs]
for (x,y) in zip(extdfnames, datasize):
    print(x + " : " + str(y))


# In[18]:


#Converting the file size to kB.
for x in datasize:
    finaldatasize = convert_size(x)
    print(finaldatasize)


# Inflation data has a file size of 9.61 kB, the macroeconomic data is 59.21 kB and the holiday data is 77.13 kB.

# In[19]:


#Printing out the column names for each dataframe
datacolumns = [x.columns for x in extdfs]
for (x,y) in zip(extdfnames, datacolumns):
    print(x + " : " + str(y))


# The inflation data has columns 'Month', 'Monthly Inflation Rate', and 'Annual Inflation Rate'. The macroeconomic data has columns 'date', 'CPI', 'Mortgage_rate', 'Unemp_rate', 'NASDAQ', 'disposable_income', 'Personal_consumption_expenditure', 'personal_savings' and the holiday data has columns 'Date', 'Holiday', 'WeekDay', 'Month', 'Day', and 'Year'.

# In[20]:


#Looking at some general information for these columns in these dataframes
datainfo = [x.info() for x in extdfs]
print(datainfo)


# In[21]:


#Taking a high-level look at all the data's first twenty rows for all twenty rows
dataskim = [x.head(n=20) for x in extdfs]
for (x,y) in zip(extdfnames, dataskim):
    print(x + " : " + str(y))


# In[22]:


#Looking at basic summary statistics
datastats = [x.describe() for x in extdfs]
for (x,y) in zip(extdfnames, datastats):
    print(x + " : " + str(y))


# Key statstics:-
# 1) Inflation data:- The monthly inflation rate has a mean of 0.22% and a median of 0.20%. It dipped to a minimum of  -0.80% and peaked at 1.20%. The annual inflation rate had an average of 2.57% and a median of 1.805. It ranged from -0.20% to 9.10% and had 2.31% as a measure of spread.
# 2) Macroeconomic data:- The mean values for the CPI = 178.8%, mortgage rate = 7.42%, Unemployment rate = 6.18%%, disposable income = $9801, and personal consumption expenditure = $7626. The median values are CPI = 177.4, mortgage rate = 6.83%, Unemployment rate = 5.70%, disposable income = $1884.73 and personal consumption expenditure = $7626. The ranges and standard deviations are shown above also.
# 3) The mean value of the results were early July, halfway through 2012 and late on the 15th day of the month. The range was from New Year's day in 2012 to the last day of 2021.

# In[23]:


#Looking at basic summary statistics
datastats = [x.describe(include = 'object') for x in extdfs]
for (x,y) in zip(extdfnames, datastats):
    print(x + " : " + str(y))


# There are 18 seperate holidays with Monday being the most common day for a holiday. 6 values also have two federal holidays on the same day like 04/08/2007.

# In[24]:


#Looking at the total number of values of each column
for (x,y) in zip(extdfs, datacolumns):
    for z in y:
        a = x[[z]].value_counts()
        print(a)


# In[ ]:




