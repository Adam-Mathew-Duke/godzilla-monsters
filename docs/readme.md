# Kaiji Dataframe 1.0 Readme

### Introduction
A Python application that allows users to compare and analyse various characteristics of different monsters from the Godzilla universe.

### Developer Guide
- Customising the UI
- Integrating new data sources
- Optimising performance
   
### User Guideu

- Sidebar
-- Login - for secret users codes (not for security or logins)
Dataframe View - toggle the Comparison and Research sections
Research View - add extra information to each item in the image grid
Research Filters: change the number of records that appear within the image grid.
Credits - View app credits and attributions
Refresh Dataframe button - A catch all to rerun Streamlit if the images do not load correctly from Github

- Comparison Section
Compare any two Kaiju from the dataframe (CSV file)
  
- Research Section (image grid)
View information about each of the Kaiju. Use the options in the sidebar to customise data and layout
  
### Installation Requirements, Dependencies and Libraries
- Developed using Python 3.12.8 on Windows 11
- Pip install streamlit
- Pip install pandas
- A CSV file with the correct file paths set
- Images for each Kaiju with the correct file paths set (each image is 200 x 200 in the app)

### Debugging and Troubleshooting
- Sometimes images will not all load correctly from Github. I could not find a way to catch this error in my code. If you have suggestions please let me know! If all the images do not load press the Refresh Dataframe button in the sidebar or clear the Streamlit cache from the Streamlit hamburger menu.

### Feedback and Ideas
- Your feedback ideas and experience are always welcome. This is my very first medium sized project using Python and Streamlit so any tips or suggestions you have to make my app even better are always very much appreciated.
