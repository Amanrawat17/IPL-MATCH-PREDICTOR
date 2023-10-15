from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained ML pipeline (replace 'pipe.pkl' with the actual file name)
with open('pipe.pkl', 'rb') as file:
    model_pipeline = pickle.load(file)

# Define options for batting team, bowling team, and venue
teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore', 'Kolkata Knight Riders',
         'Kings XI Punjab', 'Chennai Super Kings', 'Rajasthan Royals', 'Delhi Capitals']

venues = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi', 'Chandigarh', 'Jaipur', 'Chennai',
          'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala', 'Visakhapatnam', 'Pune', 'Raipur',
          'Ranchi', 'Abu Dhabi', 'Sharjah', 'Mohali', 'Bengaluru']

@app.route('/')
def home():
    return render_template('index.html', teams=teams, cities=venues)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the form data from the request
    batting_team = request.form['batting_team']
    bowling_team = request.form['bowling_team']
    venue = request.form['selected_city']
    target = float(request.form['target'])  # Convert to float
    score = float(request.form['score'])  # Convert to float
    overs = float(request.form['overs'])  # Convert to float
    wickets = float(request.form['wickets'])  # Convert to float

    # Create a DataFrame with the input data
  # Create a DataFrame with the input data
    data = pd.DataFrame({
    'teamA': [batting_team],  # Use 'teamA' instead of 'batting_team'
    'teamB': [bowling_team],  # Use 'teamB' instead of 'bowling_team'
    'venue': [venue],         # Use 'venue' instead of 'city'
    'target': [target],
    'score': [score],
    'overs': [overs],
    'wickets': [wickets]
})


    # Calculate the missing columns
    data['runs_left'] = data['target'] - data['score']
    data['balls_left'] = 120 - data['overs'] * 6  # Assuming 20 overs match
    data['crr'] = data['score'] / (20 - data['overs'])  # Calculate current run rate
    data['rrr'] = data['runs_left'] / data['balls_left']  # Calculate required run rate
    data['total_runs_x'] = data['score'] + data['runs_left']

    # Perform any necessary preprocessing (e.g., encoding categorical variables)
    # ...

    # Make the prediction using the loaded model pipeline
    prediction = model_pipeline.predict(data)

    # Display the prediction result
    return render_template('result.html', batting_team=batting_team, bowling_team=bowling_team, venue=venue, prediction=prediction[0])

if __name__ == '__main__':
    app.run(debug=True)
