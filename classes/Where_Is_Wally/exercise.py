'''
Create a collaborative human-in-the-loop Wally-detection-system
'''
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import streamlit as st
import plotly.express as px

## read in df
df = pd.read_csv('wally_positions.csv', index_col=0)

## app
st.title('Where is Wally?')

# choose image
image_number = st.selectbox('Select image', sorted([im for im in df['image']]))
img = os.path.join('images',f'{image_number}.jpg')
image = Image.open(img)

# want to see Wally?
zoom = st.checkbox('Want to see where the model detected Wally?')

# define position
subset = df[df['image']==image_number]
pos = subset.iloc[0]['position']
pos = pos[1:len(pos)-1].split(',')
pos = list(map(float, pos))


## plot
# Create figure and axes
fig, ax = plt.subplots()

# Display the image
ax.imshow(image, origin='upper')
# make cross
# ax.plot(pos[0], pos[1], color='green', marker='+', markersize=12)

if zoom:
    rect = patches.Rectangle((pos[0]-50, pos[1]-50), 100, 100, linewidth=4, 
                              edgecolor='g', facecolor='none')
    ax.add_patch(rect)

# remove ticks
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)
st.pyplot(fig)

if zoom:  # zoom in 
    fig2, ax2 = plt.subplots()

    # Display the image
    ax2.imshow(image, origin='upper')

    # ax2 zoom
    ax2.set_xlim((pos[0]+100,pos[0]-100))
    ax2.set_ylim((pos[1]+100,pos[1]-100))

    st.pyplot(fig2)

# feedback
if zoom:
    st.write('*Help us improve the predictions of the model!*')
    feedback = st.radio('Feedback', 
                        ["The model was correct",
                         "The model was wrong but I also couldn't find Wally", 
                         "The model was wrong and I know where Wally really is!"])

    if feedback == "The model was wrong and I know where Wally really is!":
        st.write('**Show us:** \n\n Use the slider to move the square. When Wally is inside the sqaure press *Send feedback*.')
        width, height = image.size
        x = st.slider('side to side', min_value = 0, max_value=width-100)
        y = st.slider('up and down', min_value = 0, max_value=height-100)

        fig3, ax3 = plt.subplots()
        # Display the image
        ax3.imshow(image, origin='upper')
        # ax3.plot(x, y, 'bo')
        rect = patches.Rectangle((x, y), 100, 100, linewidth=4, 
                              edgecolor='g', facecolor='none')
        ax3.add_patch(rect)

        st.pyplot(fig3)

    if st.button('Send feedback'):
        st.write('Thank you for the feedback!')

