#!/usr/bin/env python
# coding: utf-8

# # RFM Analysis Using Python #

# RFM Analysis is used to understand and segment customers based on their buying behaviour. RFM stands for recency, frequency, and monetary value, which are three key metrics that provide information about customer engagement, loyalty, and value to a business.

# RFM Analysis is a widely utilized concept in the field of Data Science, particularly within the marketing domain. It enables professionals to gain insights into customer behavior and segment customers based on their buying patterns.
# 
# By employing RFM Analysis, businesses can evaluate the following aspects of their customers:
# 
# 1. Recency: This metric captures the date of a customer's most recent purchase. It provides valuable information about how recently a customer has engaged with the business.
# 
# 2. Frequency: Frequency assesses the rate at which customers make purchases. It sheds light on how often customers engage with the business and make transactions.
# 
# 3. Monetary value: The monetary value metric quantifies the amount spent by customers on their purchases. It helps businesses understand the financial contribution of each customer.
# 
# Recency, Frequency, and Monetary value are key indicators that contribute to understanding customer engagement, loyalty, and overall value to a business. Analyzing these metrics empowers businesses to make informed decisions regarding customer segmentation and tailor their marketing strategies accordingly.

# ## Info About the Dataset ##

# We will use a dataset which includes Customer ID's , Transaction data & Transaction amounts.Transaction Data includes Purcahse Date, Product Info , Order ID and Loacation.With the above value we can calculate RFM values for different customers and will analyze their patterns & behaviours.

# In[17]:


#Importing the Necessary Libraries
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
pio.templates.default = "plotly_white"



# In[18]:


data = pd.read_csv("rfm_data.csv")
print(data.head())


# 1. To calculate the recency value, we subtract the purchase date from the current date using the `datetime.now().date()` function. This gives us the number of days since the customer's last purchase, indicating how recently they made a purchase.
# 
# 2. To calculate the frequency value, we group the data by 'CustomerID' and count the number of unique 'OrderID' values. This tells us the total number of purchases made by each customer, representing their frequency of purchases.
# 
# 3. To calculate the monetary value, we group the data by 'CustomerID' and sum the 'TransactionAmount' values. This provides us with the total amount spent by each customer, representing their monetary contribution.

# In[3]:


#We will calculate the Recency, Frequency, and Monetary values of the customers.


from datetime import datetime

# Convert 'PurchaseDate' to datetime to simplify calculations
data['PurchaseDate'] = pd.to_datetime(data['PurchaseDate'])

# Calculate Recency
data['Recency'] = (datetime.now().date() - data['PurchaseDate'].dt.date).dt.days

# Calculate Frequency
frequency_data = data.groupby('CustomerID')['OrderID'].count().reset_index()
frequency_data.rename(columns={'OrderID': 'Frequency'}, inplace=True)
# Merging into the original dataset
data = data.merge(frequency_data, on='CustomerID', how='left')

# Calculate Monetary Value
monetary_data = data.groupby('CustomerID')['TransactionAmount'].sum().reset_index()
monetary_data.rename(columns={'TransactionAmount': 'MonetaryValue'}, inplace=True)
# Merging the data into the original dataframe
data = data.merge(monetary_data, on='CustomerID', how='left')


# In[4]:


#We now have the RFM Scores for different customers the resulting data are as follows:
data.head()
print(data.head())


# ## Calculating RFM Scores ##
# 

# To calculate the RFM scores, we implemented a scoring system for recency, frequency, and monetary value. The scores were assigned within a predefined range for each metric.
# 
# For recency, we assigned scores from 5 to 1, where a higher score indicates a more recent purchase. This means that customers who made purchases more recently received higher recency scores.
# 
# For frequency, we assigned scores from 1 to 5, where a higher score indicates a higher purchase frequency. Customers who made more frequent purchases received higher frequency scores.
# 
# Regarding monetary value, we assigned scores from 1 to 5, where a higher score indicates a higher amount spent by the customer.
# 
# To perform this scoring process, we utilized the `pd.cut()` function. This function allowed us to divide the recency, frequency, and monetary values into bins. We defined five bins for each metric and assigned the corresponding scores to each bin.

# In[5]:


#  scoring criteria for each RFM value
recency_scores = [5, 4, 3, 2, 1]  
frequency_scores = [1, 2, 3, 4, 5]  
monetary_scores = [1, 2, 3, 4, 5]  

# Calculate RFM scores
data['RecencyScore'] = pd.cut(data['Recency'], bins=5, labels=recency_scores)
data['FrequencyScore'] = pd.cut(data['Frequency'], bins=5, labels=frequency_scores)
data['MonetaryScore'] = pd.cut(data['MonetaryValue'], bins=5, labels=monetary_scores)


# In[6]:


# Converting RFM scores to numeric type
data['RecencyScore'] = data['RecencyScore'].astype(int)
data['FrequencyScore'] = data['FrequencyScore'].astype(int)
data['MonetaryScore'] = data['MonetaryScore'].astype(int)


# In[7]:


data.head()


# ## Segmenting RFM Values ##
# 

# After calculating the RFM scores, we will create RFM segments based on the scores. We will divide RFM scores into three segments, namely “Low-Value”, “Mid-Value”, and “High-Value”. Segmentation is done using the pd.qcut() function, which evenly distributes scores between segments.

# In[8]:


# Calculate RFM score by summimg up the individual scores
data['RFM_Score'] = data['RecencyScore'] + data['FrequencyScore'] + data['MonetaryScore']

# Create RFM segments based on the RFM score
segment_labels = ['Low-Value', 'Mid-Value', 'High-Value']
data['Value Segment'] = pd.qcut(data['RFM_Score'], q=3, labels=segment_labels)


# In[9]:


data.tail()


# The segments that we derived aboveknown as RFM value segments, which categorize customers based on their RFM scores into groups such as "low value," "medium value," and "high value."
# 
# These segments are determined by dividing the RFM scores into distinct ranges or groups, allowing for a more detailed analysis of customer RFM characteristics. The RFM value segment provides insights into the relative value of customers in terms of recency, frequency, and monetary aspects.
# 
# After that we will proceed to create and analyze RFM customer segments, which are broader classifications based on the RFM scores. These segments, such as "Champions," "Potential Loyalists," and "Can't Lose," offer a strategic perspective on customer behavior and characteristics in relation to recency, frequency, and monetary aspects.
# 
# These segments provide a deeper understanding of customer engagement and loyalty, allowing businesses to tailor their strategies accordingly.

# In[10]:


# RFM Segment Distribution
segment_counts = data['Value Segment'].value_counts().reset_index()
segment_counts.columns = ['Value Segment', 'Count']

pastel_colors = px.colors.qualitative.Pastel

# Create the bar chart
fig_segment_dist = px.bar(segment_counts, x='Value Segment', y='Count', 
                          color='Value Segment', color_discrete_sequence=pastel_colors,
                          title='RFM Value Segment Distribution')

# Update the layout
fig_segment_dist.update_layout(xaxis_title='RFM Value Segment',
                              yaxis_title='Count',
                              showlegend=False)

# Show the figure
fig_segment_dist.show()


# In[11]:


# Create a new column for RFM Customer Segments
data['RFM Customer Segments'] = ''

# Assign RFM segments based on the RFM score
data.loc[data['RFM_Score'] >= 9, 'RFM Customer Segments'] = 'Champions'
data.loc[(data['RFM_Score'] >= 6) & (data['RFM_Score'] < 9), 'RFM Customer Segments'] = 'Potential Loyalists'
data.loc[(data['RFM_Score'] >= 5) & (data['RFM_Score'] < 6), 'RFM Customer Segments'] = 'At Risk Customers'
data.loc[(data['RFM_Score'] >= 4) & (data['RFM_Score'] < 5), 'RFM Customer Segments'] = "Can Lose"
data.loc[(data['RFM_Score'] >= 3) & (data['RFM_Score'] < 4), 'RFM Customer Segments'] = "Lost"

# Print the updated data with RFM segments
print(data[['CustomerID', 'RFM Customer Segments']])


# In[12]:


segment_product_counts = data.groupby(['Value Segment', 'RFM Customer Segments']).size().reset_index(name='Count')

segment_product_counts = segment_product_counts.sort_values('Count', ascending=False)

fig_treemap_segment_product = px.treemap(segment_product_counts, 
                                         path=['Value Segment', 'RFM Customer Segments'], 
                                         values='Count',
                                         color='Value Segment', color_discrete_sequence=px.colors.qualitative.Pastel,
                                         title='RFM Customer Segments by Value')
fig_treemap_segment_product.show()


# In[13]:


# Filtering the data to include only the customers in the Champions segment for better visualization purposes
champions_segment = data[data['RFM Customer Segments'] == 'Champions']

fig = go.Figure()
fig.add_trace(go.Box(y=champions_segment['RecencyScore'], name='Recency'))
fig.add_trace(go.Box(y=champions_segment['FrequencyScore'], name='Frequency'))
fig.add_trace(go.Box(y=champions_segment['MonetaryScore'], name='Monetary'))

fig.update_layout(title='Distribution of RFM Values within Champions Segment',
                  yaxis_title='RFM Value',
                  showlegend=True)

fig.show()


# In[14]:


correlation_matrix = champions_segment[['RecencyScore', 'FrequencyScore', 'MonetaryScore']].corr()

# Visualize the correlation matrix using a heatmap
fig_heatmap = go.Figure(data=go.Heatmap(
                   z=correlation_matrix.values,
                   x=correlation_matrix.columns,
                   y=correlation_matrix.columns,
                   colorscale='RdBu',
                   colorbar=dict(title='Correlation')))

fig_heatmap.update_layout(title='Correlation Matrix of RFM Values within Champions Segment')

fig_heatmap.show()


# Now we will visualize the number of customer in every  RFM Segments.

# In[15]:


import plotly.colors

pastel_colors = plotly.colors.qualitative.Pastel

segment_counts = data['RFM Customer Segments'].value_counts()

# Create a bar chart to compare segment counts
fig = go.Figure(data=[go.Bar(x=segment_counts.index, y=segment_counts.values,
                            marker=dict(color=pastel_colors))])

# Set the color of the Champions segment as a different color
champions_color = 'rgb(158, 202, 225)'
fig.update_traces(marker_color=[champions_color if segment == 'Champions' else pastel_colors[i]
                                for i, segment in enumerate(segment_counts.index)],
                  marker_line_color='rgb(8, 48, 107)',
                  marker_line_width=1.5, opacity=0.6)

# Update the layout
fig.update_layout(title='Comparison of RFM Segments',
                  xaxis_title='RFM Segments',
                  yaxis_title='Number of Customers',
                  showlegend=False)

fig.show()


# We Will have a look at the recency, frequency, and monetary scores of all the segments:

# In[16]:


# Calculate the average Recency, Frequency, and Monetary scores for each segment
segment_scores = data.groupby('RFM Customer Segments')['RecencyScore', 'FrequencyScore', 'MonetaryScore'].mean().reset_index()

# Create a grouped bar chart to compare segment scores
fig = go.Figure()

# Add bars for Recency score
fig.add_trace(go.Bar(
    x=segment_scores['RFM Customer Segments'],
    y=segment_scores['RecencyScore'],
    name='Recency Score',
    marker_color='rgb(158,202,225)'
))

# Add bars for Frequency score
fig.add_trace(go.Bar(
    x=segment_scores['RFM Customer Segments'],
    y=segment_scores['FrequencyScore'],
    name='Frequency Score',
    marker_color='rgb(94,158,217)'
))

# Add bars for Monetary score
fig.add_trace(go.Bar(
    x=segment_scores['RFM Customer Segments'],
    y=segment_scores['MonetaryScore'],
    name='Monetary Score',
    marker_color='rgb(32,102,148)'
))

# Update the layout
fig.update_layout(
    title='Comparison of RFM Segments based on Recency, Frequency, and Monetary Scores',
    xaxis_title='RFM Segments',
    yaxis_title='Score',
    barmode='group',
    showlegend=True
)

fig.show()


# we can conclude from the analysis that RFM Analysis is a valuable technique employed to analyze and categorize customers based on their purchasing behavior.Recency, frequency, and monetary value, which are three essential metrics that offer insights into customer engagement, loyalty, and value for a business.

# In[ ]:




