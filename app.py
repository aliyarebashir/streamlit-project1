import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import streamlit.components.v1 as components

st.set_page_config(page_title="Deja vu Dashboard", page_icon="gem", layout="centered")
path=os.path.dirname(__file__)
path=os.path.join(path,"dataonline.csv")
@st.cache_data
def load_data(data_path):
    dataframe = pd.read_csv(data_path, encoding="ISO-8859-1", low_memory=False)
    dataframe["Revenue"] = dataframe["UnitPrice"] * dataframe["Quantity"]
    dataframe["InvoiceDate"] = pd.to_datetime(dataframe['InvoiceDate'])
    dataframe["Month"] = dataframe["InvoiceDate"].dt.month
    dataframe["Year"] = dataframe["InvoiceDate"].dt.year
    return dataframe
st.sidebar.header("Deja vu stores")
data=st.sidebar.file_uploader("Upload Dataset",type=["csv","xlxs"])
if data is not None:
    df = load_data(data)
else:
   df=load_data(path)

values=['Bussiness snapshot',"Analysis","About"]
selection=st.sidebar.selectbox("Key performance index(KPI)",options=values)
st.sidebar.write('''Retail analytics is the process of providing analytical data on inventory levels, 
supply chain movement, consumer demand, sales, etc. ... The analytics on demand and supply data can be 
used for maintaining procurement level and also inform marketing strategies.''')
if selection=="Analysis":
    st.subheader("Display data")
    st.write(df.head(5))
    checkbox=st.checkbox("Show shape")
    if checkbox:
        st.write("Data shape")
        st.write('The dataset has {:,} rows and {:,} columns'.format(df.shape[0],df.shape[1]))
        st.markdown("Describe Statistic")
        st.write(df.describe())
elif selection=="Bussiness snapshot":
    st.title("Display data")
    st.write(df.head(5))
    col1,col2=st.columns(2)
    with col1:
        st.subheader("Monthly Revenue overview")
        monthly_Revenue=df.groupby(['Month','Year'])["Revenue"].sum().reset_index()
        plt.figure(figsize=(15, 10))
        sns.barplot(x="Month", y="Revenue", hue="Year", data=monthly_Revenue)
        plt.xlabel("Months",color="blue")
        plt.ylabel("Revenue",color="blue")
        plt.title("Monthly Revenue",color="blue")
        plt.legend(loc="upper left")
        plt.xticks(color="green")
        plt.yticks(color="green")
        st.pyplot(plt)
    with col2:
        st.subheader("Monthly items sold overview")
        monthly_items = df.groupby(['Month', 'Year'])['Quantity'].sum().reset_index()
        plt.figure(figsize=(15, 10))
        sns.barplot(x="Month", y="Quantity", data=monthly_items)
        plt.xlabel("MONTH", color="blue")
        plt.ylabel("QUANTITIES", color="blue")
        plt.title("Monthly items sold", color="blue")
        plt.xticks(color="green")
        plt.yticks(color="green")
        plt.legend(loc="upper left")
        plt.show()
        st.pyplot(plt)
    col3,col4 =st.columns(2)
    with col4:
        st.subheader("Average Revenue Overview")
        average_revenue = df.groupby(['Month', 'Year'])['Revenue'].mean().reset_index(name="Average Revenue")
        plt.figure(figsize=(15, 10))
        sns.barplot(x="Month", y="Average Revenue", hue="Year", data=average_revenue)
        plt.xlabel("MONTH", color="blue")
        plt.ylabel("CustomerID", color="blue")
        plt.title("Monthly items sold", color="blue")
        plt.xticks(color="green")
        plt.yticks(color="green")
        plt.legend(loc="upper left", title="Year")
        st.pyplot(plt)
    with col3:
        st.subheader('Monthly Active Customers')
        monthly_active_customers = df.groupby(['Month', 'Year'])['CustomerID'].nunique().reset_index()
        plt.figure(figsize=(15, 10))
        sns.barplot(x="Month", y="CustomerID", hue="Year", data=monthly_active_customers)
        plt.xlabel("MONTH", color="blue")
        plt.ylabel("CustomerID", color="blue")
        plt.title("Monthly items sold", color="blue")
        plt.xticks(color="green")
        plt.yticks(color="green")
        plt.legend(loc="upper left", title="Year")
        st.pyplot(plt)
    col5,col6=st.columns(2)
    with col5:
        st.subheader("Customer Growth (2011)")
        df_active = df.groupby(["Month", "Year"])["CustomerID"].nunique().reset_index()
        df_active_2011 = df_active[df_active['Year'] != 2010]
        plt.figure(figsize=(15, 10))
        sns.regplot(x="Month", y="CustomerID", data=df_active_2011)
        plt.title("Customer Growth 2011")
        plt.ylabel("Customers")
        plt.xlabel("Months")
        st.pyplot(plt)
    with col6:
        st.subheader("New vs Existing Users")
        df_first_purchase = df.groupby("CustomerID")["InvoiceDate"].min().reset_index(name="FirstPurchaseDate")
        df = pd.merge(df, df_first_purchase, on="CustomerID")
        df["UserType"] = "New"
        df.loc[df["InvoiceDate"] > df["FirstPurchaseDate"], "UserType"] = "Existing"
        df_new_revenue = df.groupby(["Month", "Year", "UserType"])["Revenue"].sum().reset_index()
        sns.lineplot(x="Month", y="Revenue", hue="UserType", data=df_new_revenue)
        plt.title("New vs Existing Customer Revenue Overview")
        plt.xlabel("Month")
        plt.ylabel("Revenue")
        st.pyplot(plt)

footer_temp = """
<!-- CSS  -->
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" 
type="text/css" rel="stylesheet" media="screen,projection"/>
<link href="static/css/style.css" type="text/css" rel="stylesheet" media="screen,projection"/>
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.5.0/css/all.css" 
integrity="sha384-B4dIYHKNBt8Bc12p+WXckhzcICo0wtJAoU8YZTY5qE0Id1GSseTk6S+L3BlXeVIU" crossorigin="anonymous">
<footer class="page-footer grey darken-4">
<div class="container" id="aboutapp">
<div class="row">
<div class="col l6 s12">
<h5 class="white-text">Retail Analysis App</h5>
<h6 class="grey-text text-lighten-4">This is Africa Data School Streamlit Class practical.</h6>
<p class="grey-text text-lighten-4">April 2023 Cohort</p>
</div>
<div class="col l3 s12">
<h5 class="white-text">Connect With Us</h5>
<ul>
<a href="https://www.facebook.com/AfricaDataSchool/" target="_blank" class="white-text">
<i class="fab fa-facebook fa-4x"></i>
</a>
<a href="https://www.linkedin.com/company/africa-data-school" target="_blank" class="white-text">
<i class="fab fa-linkedin fa-4x"></i>
</a>
<a href="https://www.youtube.com/watch?v=ZRdlQwNTJ7o" target="_blank" class="white-text">
<i class="fab fa-youtube-square fa-4x"></i>
</a>
<a href="https://github.com/Africa-Data-School" target="_blank" class="white-text">
<i class="fab fa-github-square fa-4x"></i>
</a>
</ul>
</div>
</div>
</div>
<div class="footer-copyright">
<div class="container">
Made by <a class="white-text text-lighten-3" href="https://africadataschool.com/">Regan </a><br/>
<a class="white-text text-lighten-3" href="https://africadataschool.com/"></a>
</div>
</div>
</footer>
"""

if selection == 'About':
    st.header("About App")
    components.html(footer_temp, height=500)