'''
In study groups, revisit the Eisenberg data. Choose a particular subset of
variables that you think are interesting and tell a story
Create a new dashboard that …
- That visualizes the data in clear, easily understandable, and aesthetically pleasing way
- That allow the user maximal oppertunities to engage with and explore the data
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_integer_dtype 

# dataset
df = pd.read_csv('Eisenberg_2019_data_compiled.csv')

cont_vars = []
discrete_vars = []
for col in df.columns[1:]:
    if is_numeric_dtype(df[col]) and not is_integer_dtype(df[col]):
        cont_vars.append(col)
    if is_string_dtype(df[col]) or is_integer_dtype(df[col]):
        discrete_vars.append(col)


## app starts ##
st.title('Eisenberg Dataset')
st.write(f'''The dataset includes {len(df.columns)} variables. There are {len(cont_vars)} continuous variables and {len(discrete_vars)} discrete variables. \n\n
You can explore the dataset using the options in the sidebar on the left.''')

st.sidebar.write('Explore the Eisenberg Dataset:')

if st.sidebar.checkbox("Show data frame"):
    st.dataframe(df)


# st.sidebar.write('**Plots**')
plot_type = st.sidebar.radio('Choose plot', ['Linear Regression', 'Bar plot', 'Histogram'])

# if st.sidebar.checkbox('Linear Regression'):
if plot_type == 'Linear Regression':
    st.header('Linear Regression')
    st.sidebar.write('**Select variables for linear regression**')
    x_lin = st.sidebar.selectbox('x variable for linear regression', 
                        options=[col for col in cont_vars])
    y_lin = st.sidebar.selectbox('y variable for linear regression', 
                        options=[col for col in cont_vars])


    fig1, ax1 = plt.subplots(1)
    ax = sns.regplot(x=x_lin, y=y_lin, data=df)
    st.pyplot(fig1)

# if st.sidebar.checkbox('Bar plot'):
if plot_type == 'Bar plot':
    st.header('Barplot')
    st.sidebar.write('**Select variables for bar plot**')
    x_bar = st.sidebar.selectbox('x variable for barplot', 
                        options=[col for col in discrete_vars])
    y_bar = st.sidebar.selectbox('y variable for barplot', 
                        options=[col for col in cont_vars+discrete_vars])

    fig2, ax2 = plt.subplots(1)
    ax2 = sns.barplot(x=x_bar, y=y_bar, data=df)
    st.pyplot(fig2)

if plot_type == 'Histogram':
    st.header('Histogram')
    st.sidebar.write('**Select variable for histogram**')
    var_hist = st.sidebar.selectbox('variable for histogram', 
                        options=[col for col in list(df.columns)[1:]])

    fig3, ax3 = plt.subplots(1)
    ax3 = sns.histplot(x=var_hist, data=df)
    st.pyplot(fig3)