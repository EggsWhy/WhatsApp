import streamlit as st
import zipfile
import io

import data_transform, helper
from urlextract import URLExtract 
import emoji
import re
from wordcloud import WordCloud, STOPWORDS

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px


st.sidebar.title("WhatsApp Chat Analyzer")
st.header('Welcome to the WhatsApp Chat Analyzer')
st.write('Just upload your exported whatsapp chat file')
st.write('It might take a while to process')
st.write('')
st.write('')

uploaded_file = st.sidebar.file_uploader("Choose a file", type=["zip", "txt"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1]
    
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue() 
    
    if file_extension == 'zip':
        # Handle zip file
        with io.BytesIO(bytes_data) as z:
            with zipfile.ZipFile(z) as zip_file:
                file_names = zip_file.namelist()
                st.sidebar.write("Files in the zip:")
                st.sidebar.write(file_names)
                
                # Find the .txt file (assuming there's only one .txt file)
                txt_file_name = None
                for file_name in file_names:
                    if file_name.endswith('.txt'):
                        txt_file_name = file_name
                        break
                
                if txt_file_name:
                    # Read the .txt file
                    with zip_file.open(txt_file_name) as txt_file:
                        data = txt_file.read().decode('utf-8')
                        
                else:
                    st.sidebar.error("No .txt file found in the zip archive.")
                    
        
        df = data_transform.transform(data)
                    
                    
    elif file_extension == 'txt':
        # Handle .txt file directly
        data = bytes_data.decode('utf-8')        
        
        df = data_transform.transform(data)
        
        
    #* Test out dataframe here
        
    # Unique users dropdown
    user_list = df['user'].unique().tolist()
    if 'whatsapp notifcation' in user_list:
        user_list.remove('whatsapp notifcation')
        
    user_list.sort()
    user_list.insert(0, "Everyone")
    
    user_selected = st.sidebar.selectbox('Show Specific User Analysis', user_list)
    
    if st.sidebar.button("Show Analysis"):
        
        num_messages, num_words, num_characters, num_media, most_active_user, num_links = helper.fetch_data(df, user_selected)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Total Messages", value=num_messages)
            
            st.metric(label="Total Media",value=num_media)
            
        with col2:
            st.metric(label="Total Words",value=num_words)
            
            st.metric(label="Most Active User", value=most_active_user)

            
        with col3:
            st.metric(label="Total Characters",value=num_characters)
            
            st.metric(label="Total Links", value=num_links)
            
            
        # Bar Chart showing most active users
        if user_selected == 'Everyone':
            st.header('Top 5 Most Active Users')
            st.write('This is based off of messages sent')
            
            graph_data, graph_data_all, x_values, y_values = helper.fetch_active_user_graph(df)
            graph_data = pd.DataFrame(graph_data)
            
            st.bar_chart(data=graph_data, x=None, y=None, y_label='Number of Messsages')
        
            # Most Characters typed
            st.header('Top 5 Most Characters typed')
            st.write('This is based off of characters typed')
            
            characters_data = helper.fetch_characters(df)   
            st.bar_chart(data=characters_data, x='user', x_label='Name' , y='message', y_label='Total Characters') 
            
            # Piechart showing message distrubtion
            st.header('Message Distrubtion')
            
            fig = px.pie(graph_data_all, names=x_values, values=y_values)
            st.plotly_chart(fig)
        
        
        # WordCloud
        st.header('Most used words')
        st.write('Stopwords are filtered out (a,an,and...)')
        wc, word_df = helper.create_worldcloud(df, user_selected)

        st.pyplot(wc)
        
        # Word Count
        st.header('Top 10 Most used Words')
        st.write('If you see <div> it means an emoji')
  
        st.bar_chart(data=word_df, x='Word', y='Count')
        
        
        # Media Count
        if user_selected == 'Everyone':
            st.header('Top 5 Media Senders')
            
            media_df, media_people, media_count = helper.fetch_media_graph(df)
            
            st.bar_chart(data=media_df, x=None, y=None, y_label="Count")
        
        
        # Emoji
        st.header('Top 10 Most used Emojis')
        
        emoji_df = helper.fetch_emoji_graph(df, user_selected)
        st.bar_chart(data=emoji_df, x='Emoji', y='Count')
        
        
        
        # Activity Trend
        st.header('Messaging activity trend')
        st.write('Based off every month')
        
        trend_df, month_df, day_df = helper.fetch_trend_data(df, user_selected)
        fig = px.line(trend_df, x='time', y='message')

        st.plotly_chart(fig)
        
        # Monthly Activity Trend
        st.header('Monthly activity trend')
        st.write('Which month are you most active?')
        
        fig = px.line(month_df, x='month', y='message')
        st.plotly_chart(fig)
        
        # Monthly Activity Trend
        st.header('Daily activity trend')
        st.write('Which day of the week are you most active?')
        
        fig = px.line(day_df, x='day', y='message')
        st.plotly_chart(fig)

        
        st.title('To be continued...')
        st.write('Pls recommend ideas')
        
        
                    
        
            
        
        
        