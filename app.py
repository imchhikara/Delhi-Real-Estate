import pickle
import streamlit as st
import numpy as np
import locale  
  
# loading in the model to predict on the data
pickle_in = open('model.pkl', 'rb')
model = pickle.load(pickle_in)

pickle_in2 = open('df.pkl', 'rb')
df = pickle.load(pickle_in2)

#Our prediction model
def predict_price(location,sqft,bath,bhk,park):
    loc_index = np.where(df.columns==location)[0][0]
    
    x= np.zeros(len(df.columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    x[3] = park
    if loc_index >= 0:
        x[loc_index] =1
        
    return model.predict([x])[0]


html_temp = """
        <div style ="background-color:black;padding:10px">
        <h1 style ="color:yellow;text-align:center;">Delhi Real Estate <i class="glyphicon glyphicon-cloud"></i></h1>
        </div>
        """      
st.markdown(html_temp, unsafe_allow_html = True)
    
with st.form("entry_form", clear_on_submit=False):
    # the following lines create text boxes in which the user can enter 
    # the data required to make the prediction
    location = st.selectbox("Locality", ('Alaknanda', 'Chhattarpur', 'Dishad Garden', 'Dwarka',
       'Geeta Colony', 'Greater Kailash', 'Hauz Khas', 'Kalkaji',
       'Karol Bagh', 'Lajpat Nagar', 'Laxmi Nagar', 'Manglapuri',
       'Mehrauli', 'Moti Nagar', 'Narela', 'New Friends Colony', 'Okhla',
       'Patel Nagar', 'Punjabi Bagh', 'Rohini', 'Safdarjung', 'Saket',
       'Sarita Vihar', 'Shahdara', 'Uttam Nagar', 'Vasant Kunj',
       'Vasundhara'))
    "---"
    bhk = st.number_input('BHK', 1, 4, 2, step=1)
    sqft = st.slider("Area", 500, 4000, 1000, step=1)
    bath = st.number_input('Bathroom', 1, 5, 2,step=1)
    park = st.number_input('Parking', 1, 5, 2, step=1)
    "---"
    submitted = st.form_submit_button("Predict")
    if submitted:
        result = predict_price(location,sqft,bath,bhk,park)
        locale.setlocale(locale.LC_MONETARY, 'en_IN')
        result = locale.currency(result, grouping=True)
        st.success(f"{bhk} BHK in {location} will cost : {result}")