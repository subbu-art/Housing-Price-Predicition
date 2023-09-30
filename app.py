from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle
import logging
import json
app = Flask(__name__)


    
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/predict', methods=['POST'])
def predict():
    with open('trained_model.pkl', 'rb') as file:
        model = pickle.load(file)
        # Load the trained model
    if request.method == 'POST':
        feature_names = ['OverallQual_GrLivArea','Overall Qual_p3',
                         'Overall Qual_p2','Overall Qual',
                         'Gr Liv Area',
                         'Gr Liv Area_p2',
                         'Yr Sold']
        features = [float(request.form[feature_name]) for feature_name in feature_names]
        data_dict = {feature_name: value for feature_name, value in zip(feature_names, features)}
        data_df = pd.DataFrame([data_dict])
        app.logger.info(data_df)
        prediction = model.predict(data_df)
        predict_data = {'SalePrice':prediction}
        pred_data_df = pd.DataFrame([predict_data])
        X,y = read_csv(data_df, pred_data_df)
        online_mode(model, X, y)
        return json.dumps(prediction[0])
def online_mode(model, X, y):
    with open('trained_model.pkl', 'wb') as file:
        pickle.dump(model, file)
        model.fit(X, y)
    
        
def read_csv(data_df, pred_data_df):
    df = pd.read_csv("oml_df.csv")
    new_data = pd.concat([data_df, pred_data_df], axis =1)
    new_df = pd.concat([df, new_data],axis = 0)
    
    X = new_df.drop('SalePrice', axis=1)
    y = new_df['SalePrice']
    
    return X, y



if __name__ == '__main__':
    app.run(debug=True)
