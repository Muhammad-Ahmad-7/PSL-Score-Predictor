from flask import Flask, render_template, request
import pandas as pd
import pickle
import sklearn

model = pickle.load(open("model.pkl", "rb"))
col_transformer = pickle.load(open("transformer.pkl", "rb"))
app = Flask(__name__)

def predicted_score(batting_team, bowling_team, stadium, over_number, current_run, wickets_left, runs_till_5_over):
    data_frame = pd.DataFrame([[stadium, batting_team, bowling_team, over_number, current_run, wickets_left, runs_till_5_over]],columns=['venue', 'Team', 'Opposition', 'Over Number', 'current_run', 'wickets_left', 'runs_till_5_over'])
    
    data_frame_transform = col_transformer.transform(data_frame)
    
    return int(model.predict(data_frame_transform)[0])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        batting_team = request.form['batting-team']
        bowling_team = request.form['bowling-team']
        stadium = request.form['stadium']
        over_number = int(request.form['over-number'])
        current_run = int(request.form['current-run'])
        wickets_left = int(request.form['wickets-left'])
        runs_till_5_over = int(request.form['runs-till-5-over'])

        print("Batting Team:", batting_team)
        print("Bowling Team:", bowling_team)
        print("Stadium:", stadium)
        print("Over Number:", over_number)
        print("Current Run:", current_run)
        print("Wickets Left:", wickets_left)
        print("Last 5 Over Runs:", runs_till_5_over)

        # Predictions
        final_score = predicted_score(batting_team, bowling_team, stadium, over_number, current_run, wickets_left, runs_till_5_over)

        return render_template("index.html", 
            batting_team=batting_team, 
            bowling_team=bowling_team, 
            stadium=stadium, 
            over_number=over_number, 
            current_run=current_run, 
            wickets_left=wickets_left, 
            runs_till_5_over=runs_till_5_over, 
            final_score=final_score)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run()