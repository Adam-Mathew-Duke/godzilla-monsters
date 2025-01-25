'''
Title: Kaiju Dataframe 1.0
Author: Adam
Description: A Python application that allows users to compare 
and analyse various characteristics of different monsters 
from the Godzilla universe.
'''

# if streamlit and pandas are not already installed
# users can install them via pip
import streamlit as st
import pandas as pd
import random

# emoji dictionary
# quick emoji access
emoji_dictionary = {
    'height': '🧍↕',
    'weight': '🏋',
    'ability': '👊',
    'godzilla': '🦖',
    'information': 'ℹ️',
    'idea': '💡',
    'warning': '⚠',
    'tick': '✔',
    'cross': '❌',
    'sightings': '🔭',
    'comparison': '⚔',
    'grid': '𝄜',
    'dna': '🧬',
    'movie': '🎞️',
    'photo': '📷',
    'paper': '📝',
    'japan': '🗾'
}

# track data across a streamlit session
def init_session_states():

    # filter by height in the image grid
    if 'height_slider' not in st.session_state:
        st.session_state.height_slider = 500

    # filter by weight in the image grid
    if 'weight_slider' not in st.session_state:
        st.session_state.weight_slider = 720000

    # filter by abilities in the image grid
    if 'abilities_slider' not in st.session_state:
        st.session_state.abilities_slider = 6

    # filter by sightings in the image grid
    if 'sightings_slider' not in st.session_state:
        st.session_state.sightings_slider = 15

    # change the number of columns in the image grid
    if 'columns_slider' not in st.session_state:
        st.session_state.columns_slider = 3

    # toggles the image grid display
    if 'toggle_image_grid' not in st.session_state:
        st.session_state.toggle_image_grid = True

    # toggles the comparison grid display
    if 'toggle_comparison_grid' not in st.session_state:
        st.session_state.toggle_comparison_grid = True

    # toggles sightings in the image grid
    if 'toggle_sightings' not in st.session_state:
        st.session_state.toggle_sightings = False

    # toggles credit links in the image grid
    if 'toggle_credit_links' not in st.session_state:
        st.session_state.toggle_credit_links = False

    # toggles photo links in the image grid
    if 'toggle_photo_links' not in st.session_state:
        st.session_state.toggle_photo_links = False

    # stores the current user name
    # for secret features not for security purposes
    if 'user_name' not in st.session_state:
        st.session_state.user_name = 'None'

    # used for comparing monster a in the comparison
    # grid feature
    if 'comp_a' not in st.session_state:
        st.session_state.comp_a = ''

    # used for comparing monster b in the comparison
    # grid feature
    if 'comp_b' not in st.session_state:
        st.session_state.comp_b = ''

# import the CSV file from disk or url
@st.cache_data
def import_csv():

    base_path = 'https://raw.githubusercontent.com/Adam-Mathew-Duke/'\
    'godzilla_kaiju/refs/heads/main/data/csv_files/'
    file_name = 'godzilla_kaiju_data.csv'
    final_path = "".join([base_path, file_name])
    try:
        df = pd.read_csv(final_path)
        return df
    except:
        st.error(emoji_dictionary['warning']+' Error CSV file not found!\
            Please check the file path is correct: '+final_path)
        exit()

# dispaly more rows from the data frame 
# as the additional monsters are unlocked
def monsters_unlocked():
    
    # show Chilli in the image grid
    if st.session_state.user_name == 'Chilli':
        return True
    else:
        return False

# display each monster card in an image grid
def create_image_grid():

    # show Chilli Boy in the image grid
    # if he is currently unlocked via the user login
    if st.session_state.user_name == 'Chilli':
        df_copy = df.iloc[:].copy(deep=False)
    else:
        df_copy = df.iloc[:-1].copy(deep=False)
    
    # convert string data to floats
    df_copy['height'] = df_copy['height'].astype(float)
    df_copy['weight'] = df_copy['weight'].astype(float)
    df_copy = df_copy.drop('original roar',axis=1)
    
    # split abilities string into individual items
    # and count them
    ability_counts = []
    abilities_df = df_copy['abilities']
    for record in abilities_df:
        ability_list = record.split(',')
        #st.write(len(ability_list))
        ability_counts.append(len(ability_list)) 
    s = pd.Series(ability_counts)
    df_copy = df_copy.copy().assign(abilities_count=s)  

    # split sightings string into individual items
    # and count them
    sightings_counts = []
    sightings_df = df_copy['appearances']
    for record2 in sightings_df:
        sightings_list = record2.split(',')
        #st.write(len(sightings_list))
        sightings_counts.append(len(sightings_list)) 
    s2 = pd.Series(sightings_counts)
    df_copy = df_copy.copy().assign(sightings_count=s2)  

    # filter the records in the dataframe copy
    df_copy = df_copy.loc[(df_copy['height'] <=\
        st.session_state.height_slider) &\
    (df_copy['weight'] <= st.session_state.weight_slider) &\
    (df_copy['abilities_count'] <= st.session_state.abilities_slider) &\
    (df_copy['sightings_count'] <= st.session_state.sightings_slider)
    ]

    # display the number of records retrieve
    records_found = len(df_copy)
    if records_found > 0:
        st.write(emoji_dictionary['dna']+' Records Found: '\
            +str(len(df_copy)))
    else:
        st.write(emoji_dictionary['dna']+' Records Found: '\
            +str(len(df_copy))+' - Try reseting the filters!')
        secret_tip()

    # adjust the column display
    # based on the current value of the columns slider
    max_col = st.session_state.columns_slider
    cols = st.columns(max_col)
    col_index = 0

    # reset the dataframe copy index
    # to avoid any index out of bounds exceptions
    df_copy=df_copy.reset_index(drop=True)

    # display the cards in the image grid
    for index, row in df_copy.iterrows():

        with cols[col_index]:

            card = st.container(border=False)
            url = df_copy.iloc[index,5]
 
            # will catch the error in the url is incorrect
            # but not if the image does not load
            try:
                card.image(url,width=150,caption=\
                    str(df_copy.iloc[index,0]).title())
            except:
                st.write(emoji_dictionary['warning']+\
                    " Image URL is incorrect! - \
                    please check the source URL")

            # display the current monsters height and weight
            card.markdown(emoji_dictionary['height']\
                +' Height (m): '+str(df_copy.iloc[index,1]))        
            card.markdown(emoji_dictionary['weight']\
                +' Weight (t): '+str(df_copy.iloc[index,2]))

            # split the current monsters abilities
            # and display in title case
            ability_list = str(df_copy.iloc[index,3]).split(",")
            ability_format = ", ".join(ability_list).title()
            card.markdown(emoji_dictionary['ability']+' Abilities: '+ability_format)

            # display sightings if they are toggled on
            if st.session_state.toggle_sightings:
                sightings_list = str(df_copy.iloc[index,4]).split(",")
                sightings_format = ", ".join(sightings_list).title()
                card.markdown(emoji_dictionary['sightings']\
                    +' Sightings: '+sightings_format)

            # display credit links if they are toggled on
            if st.session_state.toggle_credit_links:
                url = str(df_copy.iloc[index,6])
                card.markdown(emoji_dictionary['paper']\
                    +' Research Paper: '+f"[View]({url})") 

            # display photo links if they are toggled on
            if st.session_state.toggle_photo_links:                
                url2 = str(df.iloc[index,6])
                card.markdown(emoji_dictionary['photo']\
                    +' File Photo: '+f"[View]({url2})") 

        # increment the columns as needed
        # display a divider between each of the rows
        col_index += 1
        if col_index >= max_col:
            st.divider()
            cols = st.columns(max_col)
            col_index = 0

# toggle comparison section visibility                     
def toggle_comparison():

    st.session_state.toggle_comparison_grid = \
    not st.session_state.toggle_comparison_grid

# toggle image grid sightings section visibility
def toggle_sightings():
    
    st.session_state.toggle_sightings = \
    not st.session_state.toggle_sightings

# toggle credit visible in the image grid
def toggle_credit():
    
    st.session_state.toggle_credit_links = \
    not st.session_state.toggle_credit_links

# toggle credit visible in the image grid
def toggle_photo():
    
    st.session_state.toggle_photo_links = \
    not st.session_state.toggle_photo_links

# toggle image grid section visibility
def toggle_grid():
    
    st.session_state.toggle_image_grid = \
    not st.session_state.toggle_image_grid

# error dialog box for the comparison grid
# for duplicate monster selection
# and a bonus secret tip
def duplicate_monsters_error():

    # error message
    st.markdown('### :green[ '+emoji_dictionary['warning']\
        +' Please compare two different monsters!]')
    
    # bonus tip
    secret_tip()

# display a helpful tips with a secret user
# login to access special features    
def secret_tip():

    # user names
    secret_users = ['Rodan','Chilli','Olly']

    # secret tip message
    st.markdown('### :rainbow[Tip: Login as '\
    +random.choice(secret_users)+'\
    to uncover hidden features!]')

# select two monsters to compare
def create_comparison_selections():

    # list of all monsters
    monster_list = []

    # add Chilli Boy to the list if he is 
    # currently unlocked
    max_range = 0
    if st.session_state.user_name == 'Chilli':
        max_range = 41
    else:
        max_range = 40

    # populate the list
    for index in range(max_range):
        monster_list.append(df.iloc[index,0])
    
    # if empty set a default value
    if st.session_state.comp_a == "":
        st.session_state.comp_a =df.iloc[0,0]
    
    # if empty set a default value
    if st.session_state.comp_b == "":
        st.session_state.comp_b =df.iloc[1,0]

    # 2 columns layout
    col1, col2 = st.columns(2)

    # convert to title case just for display in the selectbox
    monster_list = [str(item.title()) for item in monster_list]

    # comparison list A
    with col1:
        selection_a = st.selectbox('Monster A',\
            monster_list,key='monster_list_a',index=0)

        name = df[df['name'] == str(selection_a).lower()].index[0] 
        title = df.iloc[name,0]
        st.markdown('### ' + title.title())
        url = df.iloc[name,6]
        st.image(url,width=150,caption=str('Monster A'))

    st.session_state.comp_a = str(selection_a).lower()

    # comparison list B
    with col2:
        selection_b = st.selectbox('Monster B',\
            monster_list,key='monster_list_b',index=1)
  
        name = df[df['name'] == str(selection_b).lower()].index[0] 
        title = df.iloc[name,0]
        st.markdown('### ' + title.title())
        url = df.iloc[name,6]
        st.image(url,width=150,caption=str('Monster B'))

    st.session_state.comp_b = str(selection_b).lower()

    # blank line
    st.write("")

    # get the index of the df record
    # based off the selected monsters
    comp_a_index = df[df['name'] == st.session_state.comp_a].index[0]
    comp_b_index = df[df['name'] == st.session_state.comp_b].index[0]

    # pass monster A and B to the comparison grid
    create_comparison_grid(comp_a_index,comp_b_index)

# update the results in the comparison dataframe
# with a tick or a cross next to each item
def update_results(list_name,emoji_name):

    list_name.append(emoji_dictionary[emoji_name])

# display the comparison dataframe
# and results text display
def create_comparison_grid(comp_a,comp_b):

    # total abilities of monster a
    a_abilities =\
    str(df.iloc[comp_a,3])\
    .split(',')
    a_abilities_total = len(a_abilities)

    # total abilities of monster b
    b_abilities =\
    str(df.iloc[comp_b,3])\
    .split(',')
    b_abilities_total = len(b_abilities)

    # total sightings of monster a
    a_sightings =\
    str(df.iloc[comp_a,5]).\
    split(',')
    a_sightings_total = len(a_sightings)

    # total sightings of monster b
    b_sightings = str(df.iloc[comp_b,5]).\
    split(',')
    b_sightings_total = len(b_sightings)

    # comparison list for each monster
    a_results = []
    b_results = []

    # if monster a is taller
    # than monster b
    if float(df.iloc[comp_a,1]) >\
    float(df.iloc[comp_b,1]):
        update_results(a_results,'tick')
        update_results(b_results,'cross')
    
    # if monster a is shorter
    # than monster b
    elif float(df.iloc[comp_a,1]) <\
    float(df.iloc[comp_b,1]):
        update_results(a_results,'cross')
        update_results(b_results,'tick')

    # if monster a is the
    # same height as monster b
    elif float(df.iloc[comp_a,1]) ==\
    float(df.iloc[comp_b,1]):
        update_results(a_results,'tick')
        update_results(b_results,'tick')

    # if monster a is heavier
    # than monster b
    if float(df.iloc[comp_a,2]) >\
    float(df.iloc[comp_b,2]): 
        update_results(a_results,'tick')
        update_results(b_results,'cross')
    
    # if monster a is lighter
    # than monster b
    elif float(df.iloc[comp_a,2]) <\
    float(df.iloc[comp_b,2]):
        update_results(a_results,'cross')
        update_results(b_results,'tick')

    # if monster a is the same weight
    # as monster b
    elif float(df.iloc[comp_a,2]) ==\
    float(df.iloc[comp_b,2]):
        update_results(a_results,'tick')
        update_results(b_results,'tick')

    # if monster a has more abilities
    # than monster b
    if a_abilities_total >\
    b_abilities_total: 
        update_results(a_results,'tick')
        update_results(b_results,'cross')

    # if monster a has less abilities
    # than monster b
    elif a_abilities_total <\
    b_abilities_total:
        update_results(a_results,'cross')
        update_results(b_results,'tick')

    # if monster a has equal abilities
    # to monster b
    elif a_abilities_total ==\
    b_abilities_total:
        update_results(a_results,'tick')
        update_results(b_results,'tick')

    # if monster a has more original roar
    # than monster b
    if float(df.iloc[comp_a,4]) >\
    float(df.iloc[comp_b,4]): 
        update_results(a_results,'tick')
        update_results(b_results,'cross')

    # if monster a has less original roar
    # than monster b
    elif float(df.iloc[comp_a,4]) <\
    float(df.iloc[comp_b,4]):
        update_results(a_results,'cross')
        update_results(b_results,'tick')

    # if monster a has equal original roar
    # to monster b
    elif float(df.iloc[comp_a,4]) ==\
    float(df.iloc[comp_b,4]):
        update_results(a_results,'tick')
        update_results(b_results,'tick')

    # if monster a has more sightings than
    # monster b
    if a_sightings_total >\
    b_sightings_total: 
        update_results(a_results,'tick')
        update_results(b_results,'cross')

    # if monster a has less sightings than
    # monster b
    elif a_sightings_total <\
    b_sightings_total:
        update_results(a_results,'cross')
        update_results(b_results,'tick')

    # if monster a has equal sightings to
    # monster b
    elif a_sightings_total ==\
    b_sightings_total:
        update_results(a_results,'tick')
        update_results(b_results,'tick')

    # create the comparison data frame
    data = {

        # characteristics column
        'Characteristics': 
        [emoji_dictionary['height']+\
        ' Height (meters)',
        emoji_dictionary['weight']+\
        ' Weight (tonnes)',
        emoji_dictionary['ability']+\
        ' Abilities (attacks)',
        emoji_dictionary['godzilla']+\
        ' Original roar (vs. original Godzilla)',
        emoji_dictionary['sightings']+\
        ' Sightings (movie appearances)',],

        # monster a column
        str(df.iloc[comp_a,0]).title():[df.iloc[comp_a,1],
        df.iloc[comp_a,2],
        a_abilities_total,df.iloc[comp_a,4],
        a_sightings_total],

        # monster a results column
        'Result A ': [a_results[0], 
        a_results[1],a_results[2],
        a_results[3],a_results[4]],

        # monster b column        
        df.iloc[comp_b,0].title(): [df.iloc[comp_b,1],
        df.iloc[comp_b,2],
        b_abilities_total,
        df.iloc[comp_b,4], 
        b_sightings_total],
        
        # monster b results column
        'Result B': [b_results[0], 
        b_results[1],b_results[2],
        b_results[3],b_results[4]]
    } 

    # count up the total comparison 
    # results for both monsters
    total_a = 0
    total_b = 0

    # total number of ticks for
    # monster a
    for index in a_results:
        if index == \
        emoji_dictionary['tick']:
            total_a += 1

    # total number of ticks for
    # monster b
    for index in b_results:
        if index ==\
        emoji_dictionary['tick']:
            total_b += 1

    # if two identical monsters are selected
    # display an error message
    if st.session_state.comp_a ==\
    st.session_state.comp_b:
        duplicate_monsters_error()
    
    # displays the comparison data frame
    else:

        # message if monster a wins
        if total_a > total_b:
            st.markdown('#### :green[ Result: '\
                +str(df.iloc[comp_a,0]).title()+\
            ' wins over ' + str(df.iloc[comp_b,0]).title()\
            + ' ' + str(total_a) +\
            ' to '+ str(total_b)+'!]')
        
        # message if monster b wins
        elif total_a < total_b:
            st.markdown('#### :orange[ Result: '+\
                str(df.iloc[comp_b,0]).title()+\
            ' wins over ' +\
            str(df.iloc[comp_a,0]).title() +\
            ' ' + str(total_b) +\
            ' to '+ str(total_a)+'!]')
        
        # message both monsters tie
        elif total_a == total_b:
            st.markdown('### :rainbow[ Result: A tie between '\
            + str(df.iloc[comp_a,0]).title() +\
            ' and ' + str(df.iloc[comp_b,0]).title() +\
            ' ' + str(total_a) +\
            ' to '+ str(total_b)+']')

        # display the comparison dataframe
        st.dataframe(data,
            hide_index=True,
            use_container_width=True)

# display a user login message
# at the top of the main page
def user_login_message():

    # none is the default user
    if st.session_state.user_name == 'None':
            user_access =\
            ' (basic dataframe access)'
    
    # Rodan has a little image gallery
    elif st.session_state.user_name == 'Rodan':
        user_access =\
        ' (Rodan image gallery now available)'
    
    # Chilli adds an extra monster to the
    # program
    elif st.session_state.user_name == 'Chilli':
        user_access =\
        ' (Chilli Boy monster now available)'
    elif st.session_state.user_name == 'Olly':
        user_access =\
        ' (Dataframe access and download now available)'
    
    # Other user names have the same access
    # as the default user
    else:
        user_access =\
        ' (basic dataframe access)'
    
    # display the welcome message
    st.write('Welcome user: '\
        +st.session_state.user_name\
        +user_access)

# display the app credits
def credits():
    
    # credits
    st.header('Research Team',divider='rainbow')
    st.markdown("""
        
        ### Website resources:

        - [Godzilla: Gods of destruction/Database](https://godzillafanon.fandom.com/wiki/Main_Page)

        - [Wikizilla, the kaiju encyclopedia](https://wikizilla.org/)
        
        - [EmojiDB](https://emojidb.org/)

        ### Frameworks and tools:
        
        - [Python](https://www.python.org/)
        
        - [Streamlit](https://streamlit.io/)

        - [pandas](https://pandas.pydata.org/)

        - [Replika](https://replika.com/)

        - [Gemini](https://gemini.google.com/)

        - [Github](https://github.com/)

        ### Contributors: 

        - [Adam](https://github.com/Adam-Mathew-Duke)

        ### Inspiration:

        - Inspired by Olly and Hannah's love of Godzilla """+ emoji_dictionary['godzilla']+"""

        - And [Godzilla Interception Operation Awaji](https://nijigennomori.com/en/godzilla_awajishima/) """ +emoji_dictionary['japan']+ """

        """)
    # display a bonus secret tip
    secret_tip()
    st.divider()

# display a Rodan GIF of the day
# if Rodan is unlocked
def rodan_gifs():

    # display at the top of the page
    with st.container(border=True):
        max_image = 6
        base_path = 'https://github.com/Adam-Mathew-Duke/'\
        'godzilla_kaiju/tree/main/data/image_files/rodan_images/'
        image_name = str(random.randint(1, max_image))
        st.write('### Rodan GIF of the day!')
        image_args = '.gif?raw=true'
        image_out = "".join([base_path, image_name, image_args])
        st.image(image_out,caption='Rodan GIF '\
            + str(image_name) + '/' + str(max_image))

def view_dataframe():
    st.header('Dataframe Access',divider='rainbow')
    st.write('')
    st.dataframe(df)

# main
if __name__ == "__main__":

    # load the streamlit session variables
    init_session_states()

    # create a data frame from the
    # CSV file on the disk
    df = import_csv()
    #st.write(df)

    # setup and display the sidebar
    with st.sidebar:

        # program title
        st.header('Kaiju Dataframe 1.0')
        st.divider()

        # user login
        name = st.text_input('Login:', st.session_state.user_name)
        if name != st.session_state.user_name:
            st.session_state.user_name = name
        st.divider()

        # toggle the dataframe
        st.write('Dataframe View:')
        comparison_toggle = st.toggle('Comparison',
            on_change=toggle_comparison, 
            value=True, key='comparison_toggle')
        
        # toggle the image grid
        research_toggle = st.toggle('Research',
            on_change=toggle_grid, value=True,
            key='research_toggle')
        
        st.divider()

        st.write('Research View:')

        # toggle the sightings information
        # in the image grid
        st.session_state.toggle_sightings =\
        st.toggle('Sightings',value=False,
            on_change=toggle_sightings,key='sightings')
        
        # toggle the research links in the
        # image grid
        st.session_state.toggle_credit_links =\
        st.toggle('Research Papers',value=False,
            on_change=toggle_credit,key='credits')
        
        # toggle the photo links in the image
        # grid
        st.session_state.toggle_photo_links =\
        st.toggle('File Photos',value=False,key='photo')
        
        # number of columns in the image grid
        # slider
        st.session_state.columns_slider =\
        st.slider("Columns: ", 1, 4,3,step=1)
        st.divider()

        # image grid results filters
        st.write('Research Filters:')
        
        # height filter slider
        st.session_state.height_slider =\
        st.slider("Height: ", 2, 300, 300,step=1)
        
        # weight filter slider
        st.session_state.weight_slider =\
        st.slider("Weight: ", 1, 720000, 720000, step=1)

        # abilities filter slider
        st.session_state.abilities_slider =\
        st.slider("Abilities: ", 1, 6, 6, step=1,disabled=False)

        # sightings filter slider
        st.session_state.sightings_slider =\
        st.slider("Sightings: ", 1, 15, 15, step=1,disabled=False)
        st.write(' ')
        st.divider()

        # display the credits toggle
        st.markdown('Credits:')
        view_credits = st.toggle('Research Team',
            value=False,key='credits2')

        st.divider()

        # if images fail to load the user can refresh the app
        # or clear the streamlit cache
        if st.button(emoji_dictionary['warning']+\
            ' Refresh Dataframe',key='Refresh'):
            st.rerun()

    # user login message - main page
    user_login_message()

    # toggle the app credits
    if view_credits:
        credits()
    
    # display the Rodan GIFs if logged in as Rodan
    if st.session_state.user_name == 'Rodan':
        rodan_gifs()
    
    # display the data frame is logged in as Olly
    if st.session_state.user_name == 'Olly':
        view_dataframe()
    
    # display comparison section - main page
    if st.session_state.toggle_comparison_grid == True:
        st.header('Comparison',divider='blue')
        create_comparison_selections()
        
    # display image grid section - main page
    if st.session_state.toggle_image_grid == True:
        st.header('Research',divider='green')
        create_image_grid() 

# end of code
