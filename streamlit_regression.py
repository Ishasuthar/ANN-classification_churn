import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler, LabelEncoder,OneHotEncoder
import pandas as pd
import pickle


### Load the trained model,scaler,pickle,onehot
model =load_model('regression_model.h5')

## load the encoder and scalaer
with open('onehot_encoder_geo.pkl','rb') as file:
    onehot_encoder_geo= pickle.load(file)

with open('label_encoder_gender.pkl','rb') as file:
    label_encoder_gender= pickle.load(file)

with open('scaler.pkl','rb') as file:
    scaler= pickle.load(file)

##streamlit app
st.title('Estimated Salary Prediction')

# User Input

geography= st.selectbox('Geography',onehot_encoder_geo.categories_[0])
gender=st.selectbox('Gender',label_encoder_gender.classes_)
age=st.slider('Age',18,92)
balance=st.number_input('Balance')
credit_score=st.number_input('Credit Score')
exited=st.selectbox('Exited',[0,1])
tenure=st.slider('Tenure',0,10)
num_of_products=st.slider('Number of products',1,4)
has_cr_card=st.selectbox('Has Credit Card',[1,0])
is_active_member=st.selectbox('Is Active Member',[0,1])


## prepare the input data

input_data= pd.DataFrame({
    'CreditScore':[credit_score],
    'Geography':[geography],
    'Gender':[label_encoder_gender.transform([gender])[0]],
    'Age':[age],
    'Tenure':[tenure],
    'Balance':[balance],
    'NumOfProducts':[num_of_products],
    'HasCrCard':[has_cr_card],
    'IsActiveMember':[is_active_member],
    'Exited':[exited]
    })


## geography

geo_encoded=onehot_encoder_geo.transform([[geography]]).toarray()
geo_encoded_df=pd.DataFrame(geo_encoded,columns=onehot_encoder_geo.get_feature_names_out(['Geography']))
input_data=pd.concat([input_data.drop("Geography",axis=1), geo_encoded_df], axis=1)

##scale the input data
input_data_scaled=scaler.transform(input_data)

## Predict churn
prediction= model.predict(input_data_scaled)
predicted_salary= prediction[0][0]

st.write(f'Predicted Estimated Salary:${predicted_salary:.2f}')

