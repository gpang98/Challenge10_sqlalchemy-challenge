# Challenge10_sqlalchemy-challenge


All the codes are taken from lecture notes and ChatGPT.

The GitHub repositry folder is organized thus way:
1. SursfUp folder
    - Resources folder - contain the hawaii.sqlit, and 2 csv files.
    - cimiate_starter_Final.ipynb - this is the final version of the Jupyter Notebook codes
    - climate_starte.ypynb - this was the original started codes given for the Challenge
    
    
    
2. .gitignore and README files

Part 1: Analyse and Explore the Climate Data
Using the climate_starter.ipynb, the codes were constructed to output the required result.

1.1 Precipitation Analysis:
1. Find the most recent date in the dataset.
- latest date is 23-08-2023

2-6. Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
- As displayed in the required histogram

7. Summary statistics are derived for given fo the precipitation data and displayed as per requirement.

1.3 Station Analysis
1. Total number of stations = 9
2. Most-active stations = USC00519281 with 2772 recordings.
3. Histogram of the Temperature for the last 12 months

Part 2: Design Your Climate App

Using flask to design the Climate App as required for the following routes.

        "/api/v1.0/precipitation",
        "/api/v1.0/stations",
        "/api/v1.0/tobs",
        "/api/v1.0/<start>",
        "/api/v1.0/<start>/<end>"