from flask import Flask, render_template,redirect,request
from flask_mail import Mail,Message
import requests
import json
import os
import datetime

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'testdev582@gmail.com'
app.config['MAIL_PASSWORD'] = 'hardik1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email_id = request.form.get('email-id')
        url = 'http://codeforces.com/api/user.info?handles=' + username
        wvurl = 'http://codeforces.com/api/contest.list?gym=true'
        resp = requests.get(url)
        r = requests.get(wvurl)
        if resp and r:
            user_data = json.loads(resp.text)['result']
            contest_data = json.loads(r.text)['result']
            for contest in contest_data:
                if contest['phase'] == 'BEFORE':
                    break
            if 'relativeTimeSeconds' in contest:
                contest_time = str(datetime.timedelta(seconds=abs(contest['relativeTimeSeconds'])))
            else:
                contest_time = 'Not Available'
            if email_id is not None:
                msg = Message("Upcoming Contest Info",sender=app.config.get("MAIL_USERNAME"),recipients=[''+email_id+''])
                msg.body = contest['name'] + " Contest will start in : " + contest_time
                mail.send(msg)
            return render_template('show.html',user_data = user_data,contest_data=contest,contest_time = contest_time)
        else:
            print("Error in getting response")
            return render_template('index.html')
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)
