import streamlit as st
import pandas as pd
import numpy as np
import joblib
import pickle


from PIL import Image

header = Image.open('Images/Airbnb_logo.png')
st.image(header)

st.sidebar.title('Milan Airbnb Recommendations')

st.sidebar.caption('By [Anat Jacobson](https://github.com/anat-jacobson/)')
st.sidebar.caption('Github repository [here](https://github.com/anat-jacobson/)')
st.sidebar.caption('Presentation [here](https://github.com/anat-jacobson/)')

st.title('Milan Airbnb Recommendation System')
st.header('')

side_button = st.sidebar.button('See more!')
if side_button:
    st.sidebar.write('Sidebar button was pressed')

export_review = pd.read_csv('Data/export_review.csv', index_col=0)

export_listings = pd.read_csv('Data/export_listings.csv', index_col = 'listing_id')

final_df_export = pd.read_csv('Data/final_df_export.csv', index_col= 'listing_id')


#import model
model = pickle.load(open('model.sav', 'rb'))

#function
def rec_airbnbs_info():
    
    user = int(input('reviewer_id: '))
    n_recs = int(input('How many airbnb recommendations do you want? '))
    
    have_reviewed = list(export_review.loc[user, 'listing_id'])
    not_reviewed = final_df_export.copy()
    not_reviewed = not_reviewed.drop_duplicates(subset=['listing_id'])
    not_reviewed = not_reviewed.set_index('listing_id')
    not_reviewed = not_reviewed.drop(have_reviewed)
    
    not_reviewed = not_reviewed.reset_index()

    not_reviewed['est_rating'] = not_reviewed['listing_id'].apply(lambda x: model.predict(user, x).est)
    not_reviewed = not_reviewed.sort_values(by = 'est_rating', ascending = False)
    not_reviewed = not_reviewed.drop(columns=['id'])
    not_reviewed = not_reviewed.merge(export_listings, on = 'listing_id', how = 'left')
    not_reviewed = not_reviewed.drop(columns = ['property_type', 'neighbourhood_cleansed', 'neighborhood_overview',
                                'host_identity_verified', 'neighborhood_overview', 'name', 'reviewer_name',
                                'date', 'reviewer_id', 'comments', 'language', 'polarity', 'rec_scale',
                                'host_location', 'host_name', 'host_response_rate', 'host_acceptance_rate', 
                                'review_scores_rating','review_scores_accuracy', 'review_scores_cleanliness',
                                 'review_scores_checkin', 'review_scores_communication', 'review_scores_location',
                                 'review_scores_value', 'beds'])
    not_reviewed = not_reviewed.rename(columns={'listing_id':'Listing Id',
                               'est_rating':'Predicted Rating','host_is_superhost':'Superhost?', 'room_type':'Room Type',
                                           'accommodates':'Accommodates', 'amenities':'Amenities', 
                                         'bedrooms':'Number of Bedrooms', 'bedrooms':'Number of beds', 
                                                'instant_bookable': 'Bookable instantly?', 
                                                'host_response_time': 'Response time of host',
                                                'description': 'Description'})
    return not_reviewed.head(n_recs)


st.sidebar.subheader('Content based recommendation system')
st.sidebar.write('Existing airbnb users looking for milan airbnbs they might enjoy.')

st.title("Milan Airbnbs")
st.subheader("Sidebar for Options")

airbnb_listings = ['Existing Reviewers', 'Similar Airbnbs']
listing = st.sidebar.radio('Navigation', airbnb_listings)