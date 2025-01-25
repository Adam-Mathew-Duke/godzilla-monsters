# Kaiji Dataframe 1.0 Readme

### Introduction
A Python application that allows users to compare and analyse various characteristics of different monsters from the Godzilla universe.

### Developer guide
  
- Integrating new data sources
  - Changing the base_path and the file_name variables to import your own CSV files.
  - Changing the image URLs in the CSV file allows you to use different images.
  
- Optimising performance
  - Using @st.cache_data above selected functions is helpful.
   
### User guide

- Sidebar components
  - Login - for secret users codes (not for security or logins)
  - Dataframe View - toggle the Comparison and Research sections
  - Research View - add extra information to each item in the image grid
  - Research Filters: change the number of records that appear within the image grid.
  - Credits - View app credits and attributions
  - Refresh Dataframe button - A catch all to rerun Streamlit if the images do not load correctly from Github

- Main components
  - Comparison section: Compare any two Kaiju from the dataframe (CSV file)
  - Research Section (image grid): View information about each of the Kaiju. Use the options in the sidebar to customise data and layout
  
### Installation Requirements, Dependencies and Libraries
- Python 3.12
- Pip install streamlit
- Pip install pandas
- A CSV file with the correct file paths set
- Images for each Kaiju with the correct file paths set (each image is 200 x 200 in the app)

### Debugging and Troubleshooting

- st.imag
  - If all images do not load from Github refresh the Streamlit cache. Or click the Refresh Dataframe button in the app's sidebar to re-run the Streamlit app.

### Feedback
- Your feedback and suggestions are important to me and always welcome.
