# Section: 01
# Lecture Name: Ts. Dr. Chan Weng Howe
# Group : 2
# Team member:
# 1. MUHAMMAD AMIR JAMIL BIN JAMLUS (A21EC0202)
# 2. ALYA BALQISS BINTI AZHAR (A21EC0158)
# 3. ALIEYA ZAWANIE BINTI A ZAINI(A21EC0156)
# 4. MUHAMMAD IQMAL BIN SIS (A21EC0080)
# 5. IKMAL BIN KHAIRULEZUAN (A21EC0186)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import mysql.connector
import queries
import altair as alt


# TASK 1: establish connection to MySQL
# You code starts here
conn = mysql.connector.connect(
    host='localhost',
    user='root', # put your username here
    password='Alieya123_', # put your password here
    database='sakila'
)

# Use this function to get scalar values from MySQL
# To use the function, pass in the query variable and connection object.
def getOne_query(query,conn):
    if query != '':
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return list(result)[0]
    else:
        return '--'

# Use this function to get dataframe from MySQL for ploting OR display of lists
# To use the function, pass in the query variable and connection object.
def getMany_query(query, conn):
    if query != '':
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        result = pd.DataFrame(result, columns=cursor.column_names)
        cursor.close()
    else:
        result = pd.DataFrame()
    return result

st. set_page_config(layout="wide")

st.title('DVD Rental Store Information')
tab_overview, tab_customers, tab_film, tab_actors = st.tabs(['Overview','Customer Infomation','Film Information','Actor Information'])

# ---------------------------------------------- Tab 1 ----------------------------------------------

with tab_overview:
    st.header('Overview')
    col11, col12, col13, col14 = st.columns(4)
    with col11:
        st.metric('Total Customers',getOne_query(queries.queryT1, conn))
    with col12:
        st.metric('Total Actors', getOne_query(queries.queryT2, conn))
    with col13:
        st.metric('Total Film', getOne_query(queries.queryT3, conn))
    with col14:
        st.metric('Total Staff', getOne_query(queries.queryT4, conn))
    
    col11, col12 = st.columns(2)
    with col11:
        st.subheader('Inventory by store')
        df = getMany_query(queries.queryT18, conn)
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df, y='inventory_count', x='store_id', color='store_id', height=500)
    
    with col12:
        st.subheader('Revenue by store')
        df = getMany_query(queries.queryT20, conn)
        df['revenue'] = df['revenue'].astype(float)
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df, y='revenue', x='store_id', color='store_id', height=500)
    
    
    st.subheader('Replacement film cost')
    df = getMany_query(queries.queryT19, conn)
    df['replacement_cost']  = pd.to_numeric(df['replacement_cost'])
    df['film']  = df['film'].astype(object)
    if df.empty:
        st.write('No data, please insert query in queries.py')
    else:
         st.bar_chart(df, x='replacement_cost', y='film', color='#FF0000', height=500)

# ---------------------------------------------- Tab 2 ----------------------------------------------

with tab_customers:
    st.header('Customer Information Dashboard')
    
#     st.selectbox(label, options, index=0, format_func=special_internal_function, key=None, help=None, on_change=None, args=None, kwargs=None, *, placeholder="Choose an option", disabled=False, label_visibility="visible")
    
    col11, col12 = st.columns(2)
    with col11: 
        st.subheader('Total customer by store')
        df = getMany_query(queries.queryT5, conn)
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df, y='customer_count', x='store_id', color='store_id', height=500)
    
    with col12:
        st.subheader('Customer by country')
        df = getMany_query(queries.queryT8, conn)
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df, y='total_customers', x='country_id', color='country_id', height=500)
            
    col21, col22 = st.columns(2)
    with col21:
        st.subheader('Customer activation status')
        df = getMany_query(queries.queryT7, conn)
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            df
        
    with col22:
        st.subheader('Country')
        df = getMany_query(queries.queryT9, conn)
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            df
            
    st.subheader('Payment per month')
    df = getMany_query(queries.queryT10, conn)
    df['amount']  = pd.to_numeric(df['amount'])
    if df.empty:
        st.write('No data, please insert query in queries.py')
    else:
        st.line_chart(df, y='amount', x='month', color='#00FF00', height=500)         
        
        
    col31, col32 = st.columns(2)
    with col31:
        st.subheader('Highest total of payment by customer')
        df = getMany_query(queries.queryT6, conn)
        df['total_paid']  = pd.to_numeric(df['total_paid'])
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df, y='total_paid', x='customer_name', color='customer_name', height=500)
        
    with col32:
        st.subheader('Highest Film rent by customer')
        df = getMany_query(queries.queryT11, conn)
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            st.bar_chart(df, y='film', x='customer_name', color='customer_name', height=500)
          
# ---------------------------------------------- Tab 3 ----------------------------------------------


with tab_film:
    st.header('Film Information Dashboard')
    # your code starts here
    colfilm1, colfilm2 = st.columns(2)
    with colfilm1:
        st.subheader('Category Film')
        df = getMany_query(queries.category_count, conn)
        if df.empty:
            st.write('No data, please insert query in queries_a.py')
        else:
            st.bar_chart(df, y='category_count', x='categories',color='categories', height=500)

    with colfilm2:
        st.subheader('Rating Analysis')
        df = getMany_query(queries.rating_count, conn)
        if df.empty:
            st.write('No data, please insert query in queries.py')
        else:
            fig = px.pie(df, values='rating_count', names='rating',
                         labels={'rating': '', 'rating_count': 'Rating Film'})

            # Display the pie chart using st.plotly_chart
            st.plotly_chart(fig, use_container_width=True)

    st.subheader('Rental Rate')
    df = getMany_query(queries.rental_rate, conn)
    if df.empty:
        st.write('No data, please insert query in queries_a.py')
    else:
        fig_bar = px.bar(df, x='rental_rate', y='rate',
                         labels={'rental_rate': 'Rental Rate', 'rate': 'Count'},
                         title='Bar Chart: Rental Rate Distribution',
                         color='rental_rate',  # Color bars based on rental rate
                         hover_name='rate',  # Show count on hover
                         text='rate',  # Show count on the bars
                         )

        # Customize layout
        fig_bar.update_layout(
            xaxis_title='Rental Rate',
            yaxis_title='Count',
            showlegend=False,  # Hide legend for single-color bars
            width = 1400
        )

        # Show the plot using Streamlit
        st.plotly_chart(fig_bar)

    st.subheader('Rental Rate vs Duration')
    df = getMany_query(queries.rate_duration , conn)
    if df.empty:
        st.write('No data, please insert query in queries_a.py')
    else:
        fig_box = px.box(df, x='rental_rate', y='rental_duration',
        labels={'rental_rate': 'Rental Rate', 'rental_duration': 'Rental Duration'},
            title='Box Plot: Rental Duration by Rental Rate',
            color='rental_rate'  # Color boxes based on rental rate
                )
    st.plotly_chart(fig_box,use_container_width=True, height=3000, width=800)

    colfilm21, colfilm22 = st.columns(2)
    with colfilm21:
        st.subheader('Top 10 Film')
        df = pd.read_sql_query(queries.top_category, conn)
        st.dataframe(df, width=800)
    with colfilm22:
        st.subheader('Lowest 10 Film')
        df = pd.read_sql_query(queries.low_category, conn)
        st.dataframe(df,width=800)

# ---------------------------------------------- Tab 4 ----------------------------------------------
with tab_actors:
    st.header('Actor Information Dashboard')

    # Top Actors by Film Count
    st.subheader('Top 10 Actors by Film Count')
    top_actors = getMany_query(queries.queryT12, conn)
    st.bar_chart(top_actors, y='film_count', x='actor_name', color='actor_name', height=500)

    #  Actor-Film Category Relationship
    st.subheader('Film Categories Preferred by Actors')
    # Get the list of all film categories
    all_categories = getMany_query(queries.queryT13, conn)
    all_categories = all_categories['name'].tolist()
    selected_category = st.selectbox('Select Film Category:', all_categories, key='1a')
    actor_category = getMany_query(queries.queryT16, conn)
    selected_category_data = actor_category[actor_category['film_category'] == selected_category]
    st.bar_chart(selected_category_data, y='film_count', x='actor_name', height=800)

    # Number of Movies Each Actor Has Acted In
    st.subheader('Number of Movies Each Actor Has Acted In')
    actor_movie_count = getMany_query(queries.queryT17, conn)
    # Top 10 Actors
    top_10_actors = actor_movie_count.nlargest(10, 'movie_count')
    col1, col2 = st.columns(2)
    col1.subheader('Top 10 Actors by Movie Count')
    col1.dataframe(top_10_actors)
    # Lowest 10 Actors
    lowest_10_actors = actor_movie_count.nsmallest(10, 'movie_count')
    col2.subheader('Lowest 10 Actors by Movie Count')
    col2.dataframe(lowest_10_actors)
    
    #Top 10 Actors by Total Rentals
    st.subheader('Top 10 Total Rentals by Actors')
    top_actors = getMany_query(queries.queryT14, conn)
    col1, col2 = st.columns(2)   
    col1.subheader('Top 10 Actors by Total Rentals')
    col1.dataframe(top_actors)
    col2.subheader('Bar Chart:Top 10 Total Rentals by Actor')
    col2.bar_chart(top_actors.set_index('actor_name'), height=700)     
    #Average Rental Rate by Actor
    st.subheader('Average Rental Rate by Actors')
    # Fetch data from MySQL
    avg_rental_rate = getMany_query(queries.queryT15, conn)
    avg_rental_rate['avg_rental_rate'] = pd.to_numeric(avg_rental_rate['avg_rental_rate'])
    st.bar_chart(avg_rental_rate, x='actor_name', y='avg_rental_rate',color='avg_rental_rate' ,height=700)
    
    



# ---------------------------------------------- Tab 5 ----------------------------------------------






