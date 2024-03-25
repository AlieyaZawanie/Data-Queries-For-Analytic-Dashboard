# Section: 01
# Lecture Name: Ts. Dr. Chan Weng Howe
# Group : 2
# Team member:
# 1. MUHAMMAD AMIR JAMIL BIN JAMLUS (A21EC0202)
# 2. ALYA BALQISS BINTI AZHAR (A21EC0158)
# 3. ALIEYA ZAWANIE BINTI A ZAINI(A21EC0156)
# 4. MUHAMMAD IQMAL BIN SIS (A21EC0080)
# 5. IKMAL BIN KHAIRULEZUAN (A21EC0186)

from turtle import color
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import mysql.connector
import queries_a
import altair as alt

# TASK 1: establish connection to MySQL
# You code starts here
conn = mysql.connector.connect(
    host='localhost',
    user='root', # put your username here
    password='', # put your password here
    database='bikestore'
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

st.title('Bikestore Data Exploration')
tab_overview, tab_orders, tab_customers, tab_staff, tab_items = st.tabs(['Overview','Sales order Dashboard','Customers Dashboard','Staff Dashboard','Item Dashboard'])

# ---------------------------------------------- Tab 1 ----------------------------------------------

with tab_overview:
    st.header('Overview')
    col11, col12, col13, col14 = st.columns(4)
    with col11:
        st.metric('Total Customers',getOne_query(queries_a.queryT1, conn))
    with col12:
        st.metric('Total Products', getOne_query(queries_a.queryT2, conn))
    with col13:
        st.metric('Total Stores', getOne_query(queries_a.queryT3, conn))
    with col14:
        st.metric('Total Orders', getOne_query(queries_a.queryT4, conn))

    col21, col22 = st.columns(2)
    with col21:
        st.subheader('Total Orders by Year')
        df = getMany_query(queries_a.queryT5, conn)
        if df.empty:
            st.write('No data, please insert query in queries_a.py')
        else:
            st.bar_chart(df, y='no_of_orders', x='year', height=500)

    with col22:
        st.subheader('Distribution of Orders by Store')
        df = getMany_query(queries_a.queryT6, conn)
        if df.empty:
            st.write('No data, please insert query in queries_a.py')
        else:
            st.bar_chart(df, y='no_of_orders', x='store', height=500)

# ---------------------------------------------- Tab 2 ----------------------------------------------

with tab_orders:
    st.header('Sales order Dashboard')

    # Create a dropdown menu with options for 'Total Sales Value' and 'Total Sales Quantity'
    option = st.selectbox(
        'PLease choose Sales Value($)/Quantity',
        ('Total Sales Value($)', 'Total Sales Quantity')
    )

    # Use the selected option to determine what data to fetch and display
    if option == 'Total Sales Value($)':
        total_sales_value = getOne_query(queries_a.queryT7, conn)
        st.metric(option, total_sales_value)
    elif option == 'Total Sales Quantity':
        total_sales_quantity = getOne_query(queries_a.queryT8, conn)
        st.metric(option, total_sales_quantity)

    col31, col32 = st.columns(2)
    with col31:
        st.subheader('Total Sales by Year')
        df = getMany_query(queries_a.queryT9, conn)
        if df.empty:
            st.write('No data, please insert query in queries_a.py')
        else:
            st.bar_chart(df, y='CAST(SUM(total_sales)AS FLOAT)', x='year', height=500 , color = 'year')   

    with col32:
        st.subheader('Total Sales by Product')
        df = getMany_query(queries_a.queryT10, conn)
        if df.empty:
            st.write('No data, please insert query in queries_a.py')
        else:
            st.bar_chart(df, y='CAST(SUM(total_sales)AS FLOAT)', x='product_name', height=500 , color = 'product_name')   

    # Create a dropdown menu with options for 'Total Sales Value' and 'Total Sales Quantity'
    option = st.selectbox(
        'Which year?',
        ('2016', '2017', '2018')
    )

    # Use the selected option to determine what data to fetch and display
    if option == '2016':
        st.subheader('Total Orders by Year(2016)')
        df = getMany_query(queries_a.queryT11, conn)
        if df.empty:
            st.write('No data, please insert query in queries_a.py')
        else:
            st.bar_chart(df, y='CAST(SUM(total_sales)AS FLOAT)', x='product_name', height=500 , color = 'product_name') 

    elif option == '2017':
        st.subheader('Total Orders by Year(2017)')
        df = getMany_query(queries_a.queryT12, conn)
        if df.empty:
            st.write('No data, please insert query in queries_a.py')
        else:
            st.bar_chart(df, y='CAST(SUM(total_sales)AS FLOAT)', x='product_name', height=500, color = 'product_name') 

    elif option == '2018':
        st.subheader('Total Orders by Year(2018)')
        df = getMany_query(queries_a.queryT13, conn)
        if df.empty:
            st.write('No data, please insert query in queries_a.py')
        else:
            st.bar_chart(df, y='CAST(SUM(total_sales)AS FLOAT)', x='product_name', height=500, color = 'product_name') 


    st.metric('Product with highest sales',getOne_query(queries_a.queryT14, conn))
# ---------------------------------------------- Tab 3 ----------------------------------------------


with tab_customers:
    st.header('Customer Dashboard')
    

    st.metric('Total Number of Customers',getOne_query(queries_a.queryT15, conn))

    col31, col32 = st.columns(2)
    with col31:
        st.title('Recurring')
        st.metric('Total Number of Recurring Customers & Sales',getOne_query(queries_a.queryT16, conn))   

    with col32:
        st.title('One-Time')

        st.metric('Total Number of One-Time Customers & Sales',getOne_query(queries_a.queryT17, conn)) 
    
    col31, col32 = st.columns(2)
    with col31:
        df = pd.read_sql_query(queries_a.queryT18, conn)
        st.dataframe(df)   

    with col32:
        df2 = pd.read_sql_query(queries_a.queryT19, conn)
        st.dataframe(df2)  

    col31, col32 = st.columns(2)
    with col31:
        st.subheader('Range of Sales($) for Recurring')
        df31 = pd.read_sql_query(queries_a.queryT18, conn)
        fig = px.box(df31, y='ListRecurringCustomers')

        st.plotly_chart(fig)

    with col32:
        st.subheader('Range of Sales($) for One-Time')
        df32 = pd.read_sql_query(queries_a.queryT19, conn)
        fig = px.box(df32, y='ListOneTimeCustomers', color_discrete_sequence=['#90ee90'])

        st.plotly_chart(fig)


    col1, col2 = st.columns(2)

 

    with col1:
        st.header('10 Customers with Highest Sales')
        df30 = pd.read_sql_query(queries_a.queryT20, conn)
        
        
        fig = px.bar(df30, x='Listtop10Customers', y='full_name', text='<b>' + df30['full_name'] + '</b>',
                     color='Listtop10Customers',
                     orientation='h',
                     
                     labels={'full_name': 'Name of customer', 'Listtop10Customers': 'Total Sales',
                             'full_name': 'Name of customer'})

        
        fig.update_layout(
            xaxis_title='Total Sales',
            yaxis_title='Customer',
            yaxis_categoryorder='total ascending',
            height=550,
            width=550
        )

        st.plotly_chart(fig)

    with col2:
        st.subheader('Top 10 Customers & Sales')

        df3 = pd.read_sql_query(queries_a.queryT20, conn)
        st.dataframe(df3)
# ---------------------------------------------- Tab 4 ----------------------------------------------

with tab_staff:
    st.header('Staff Dashboard')
    st.subheader('Total Staff by Store')
    df = getMany_query(queries_a.queryT33, conn)

    if df.empty:
        st.write('No data, please insert query in queries_a.py')
    else:
        # Create a pie chart using plotly.express
        fig = px.pie(df, values='total_staff', names='store_name',
                     labels={'store_name': 'Store', 'total_staff': 'Total Staff'})

        # Display the pie chart using st.plotly_chart
        st.plotly_chart(fig, use_container_width=True)

    col51, col52 = st.columns(2)
    with col51:
        st.subheader('Customer to Staff Ratio by Store')
        df = getMany_query(queries_a.queryT34, conn)
        df['customer_staff_ratio'] = pd.to_numeric(df['customer_staff_ratio'], errors='coerce').astype(float)
        if df.empty:
            st.write('No data, please insert query in queries_a.py')
        else:
            # Create a bar chart
            fig = px.bar(df, x='store_name', y='customer_staff_ratio',
                         text='customer_staff_ratio',
                         color='store_name',
                         labels={'store_name': 'Store', 'customer_staff_ratio': 'Customer-to-Staff Ratio'},
                         height=500, width=650)

            # Customize the layout
            fig.update_layout(
                xaxis_title='Store',
                yaxis_title='Customer-to-Staff Ratio',
                xaxis_categoryorder='total ascending',
            )

            # Display the chart using st.plotly_chart
            st.plotly_chart(fig)

    with col52:
        st.subheader('Customer to Staff Ratio by Year')
        df = getMany_query(queries_a.queryT35, conn)
        if df.empty:
            st.write('No data, please insert query in queries_a.py')
        else:
            # Filter the dataframe to include only the desired years
            years_to_display = [2016, 2017, 2018]
            df_filtered = df[df['years'].isin(years_to_display)]

            # Create a line chart with filtered years
            fig_line_ratio = px.line(df_filtered, x='years', y='customer_staff_ratio',
                                     color='store_name',
                                     labels={'years': 'Years', 'customer_staff_ratio': 'Customer-to-Staff Ratio'},
                                     line_shape='linear',  # Use 'linear' line shape
                                     markers=dict(symbol='circle', size=8))

            # Customize the layout for better readability
            fig_line_ratio.update_layout(
                xaxis_title='Years',
                yaxis_title='Customer-to-Staff Ratio',
                height=500,
                width=700,
                xaxis=dict(
                    tickmode='array',
                    tickvals=years_to_display,
                    dtick=1
                )
            )

            # Display the line chart using st.plotly_chart
            st.plotly_chart(fig_line_ratio)

# ---------------------------------------------- Tab 5 ----------------------------------------------

with tab_items:
    st.header('Item Dashboard')
    col41, col42 = st.columns(2)
    with col41:
        st.metric('Total Products', getOne_query(queries_a.queryT21, conn))
    with col42:
        st.metric('Total Brands', getOne_query(queries_a.queryT22, conn))

    col43, col44 = st.columns(2)
    with col43:
        st.subheader('Distribution of Products by Brands')
        df = getMany_query(queries_a.queryT23, conn)
        if df.empty:
            st.write('No data, please insert query in queries_a.py')
        else:
            # Create a bar chart
            fig = px.bar(df, x='brand_name', y='product_count',
                         text='product_count',
                         color='brand_name',
                         labels={'brand_name': 'Brands', 'product_count': 'Product Count'},
                         height=500, width=650)

            # Customize the layout
            fig.update_layout(
                xaxis_title='Brands',
                yaxis_title='Product Count',
                xaxis_categoryorder='total descending',
            )

            # Display the chart using st.plotly_chart
            st.plotly_chart(fig)

    with col44:
        st.subheader('Sales by Brand')
        df = getMany_query(queries_a.queryT24, conn)
        df['total_sales'] = pd.to_numeric(df['total_sales'], errors='coerce').astype(float)  # Convert to numeric
        df['total_sales'] = df['total_sales'].round(2)

        if df.empty:
            st.write('No data, please insert query in queries_a.py')
        else:
            # Create a pie chart using plotly.express
            fig = px.pie(df, values='total_sales', names='brand_name', title='Sales by Brand',
                         labels={'brand_name': 'Brand', 'total_sales': 'Total Sales'})

            # Display the pie chart using st.plotly_chart
            st.plotly_chart(fig, use_container_width=True)

    col45, col46 = st.columns([4,5])
    with col45:
        st.subheader('Top Product Sales by Brand')
        df = pd.read_sql_query(queries_a.queryT25, conn)

        # Create a horizontal bar chart
        fig = px.bar(df, x='total_sales', y='brand_name', text='<b>' + df['product_name'] + '</b>',
                     color='total_sales',
                     orientation='h',
                     title='Top-Selling Products by Brand',
                     labels={'brand_name': 'Brand', 'total_sales': 'Total Sales',
                             'product_name': 'Top-Selling Product'})

        # Customize the layout
        fig.update_layout(
            xaxis_title='Total Sales',
            yaxis_title='Brand',
            yaxis_categoryorder='total ascending',
            height=600,
            width=600
        )

        # Display the chart using st.plotly_chart
        st.plotly_chart(fig)

    with col46:
        st.subheader('Item by Price Category')
        option = st.selectbox(
            'Which category?',
            ('Overall', 'Low-Priced', 'Medium-Priced', 'High-Priced')
        )

        # Use the selected option to determine what data to fetch and display
        if option == 'Overall':
            st.subheader('Overall Items')
            df = pd.read_sql_query(queries_a.queryT26, conn)
            st.dataframe(df)

        elif option == 'Low-Priced':
            st.subheader('Low-Priced Items')
            df = pd.read_sql_query(queries_a.queryT27, conn)
            st.dataframe(df)

        elif option == 'Medium-Priced':
            st.subheader('Medium-Priced Items')
            df = pd.read_sql_query(queries_a.queryT28, conn)
            st.dataframe(df)

        elif option == 'High-Priced':
            st.subheader('High-Priced Items')
            df = pd.read_sql_query(queries_a.queryT29, conn)
            st.dataframe(df)

    col47, col48, col49 = st.columns([12,11,10])
    with col47:
        st.subheader('Top 5 Low-Priced Items')
        df = pd.read_sql_query(queries_a.queryT30, conn)
        st.dataframe(df)

    with col48:
        st.subheader('Top 5 Medium-Priced Items')
        df = pd.read_sql_query(queries_a.queryT31, conn)
        st.dataframe(df)

    with col49:
        st.subheader('Top 5 High-Priced Items')
        df = pd.read_sql_query(queries_a.queryT32, conn)
        st.dataframe(df)
