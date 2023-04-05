# Campground Moving To  
  
Campground Moving To, while an odd name, has a very specific use. It takes CSV reports from a campground reservation system and outputs the guests that are moving to new campsites. I'm being purposely vague on the reports and reservation system, but if it looks useful to you, go ahead and use it.

## Live
This app is currently built to run on Streamlit. It can be found here:
[Campground Streamlit](https://campground.streamlit.app/)

## Description
Two separate files are needed from the reservation system, `Due In Report.csv` and `Due Out Report.csv`.
The *Due In Report* is the list of guests that are due to check in that day. The *Due Out Report* is the list of guests that are due to check out that day. Because of restrictions or different situations, often times the guests that are checking out that day, are only moving to a new site and not actually leaving. *Campground Moving To* is comparing those two lists and returning a list with the guests that are just moving to a new site.

Pandas is being used for the data manipulation, and Streamlit for the front-end. I decided on Streamlit just as an experiment to test it out. It's also deployed on the Streamlit cloud.
