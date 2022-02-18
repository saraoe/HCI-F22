'''
Exercise 1:
- Add an element that makes it possible to show and hide the data frame
- Make the slider control a variable, e.g. age, and show the output 
    embedden in a sentence: "I am x years old"
- Place all "controllers" in the sidebar
- Change the selecter so that the user can choose a continent and make the
    plot show life expectancies for all countries in different colors 
'''

import streamlit as st
import pandas as pd
import plotly.express as px

# import data
df = pd.DataFrame(px.data.gapminder())

st.title('Exercise 1')

if st.sidebar.checkbox("Show data frame"):
    st.dataframe(df)

age = st.sidebar.slider('Age', 0,100,50)
st.write(f'I am {age} years old')

continents = df['continent'].unique()
continent = st.sidebar.selectbox('Select a continent', continents)
dfc = df[df['continent']==continent]
fig = px.line(dfc, x="year", y="lifeExp", color='country')
st.plotly_chart(fig)


