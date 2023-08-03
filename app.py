import datetime
from flask import Flask, render_template, redirect, session, request, url_for
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
app.static_folder = 'static'

# Disable caching during development
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Session secret key
app.secret_key = "YOUR_SECRET_KEY"

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'YOUR_USERNAME'
app.config['MYSQL_PASSWORD'] = 'YOUR_PASSWORD'
app.config['MYSQL_DB'] = 'jobshala'

# Initialize MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):  # Use integer index for 'password'
            session['user_id'] = user[0]  # Use integer index for 'id'
            return redirect(url_for('jobs'))
        else:
            return render_template('login.html', error="Invalid email or password")

    return render_template('login.html')

# Route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, hashed_password, email))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
    return redirect(url_for('jobs')) 

@app.route('/jobs')
def jobs():
    user_authenticated = 'user_id' in session
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jobs")
    jobs = cur.fetchall()
    cur.close()
    categories = set(job[1] for job in jobs)
    categorized_jobs = {category: [] for category in categories}

    for job in jobs:
        categorized_jobs[job[1]].append(job)
    
    return render_template('jobs.html', user_authenticated=user_authenticated, categorized_jobs=categorized_jobs, time_ago=time_ago)

@app.route('/job/<int:job_id>')
def job_description(job_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jobs WHERE idjobs = %s", (job_id,))
    job = cur.fetchone()
    cur.close()
    print(job)
    if job:
        return render_template('job_description.html', job=job, time_ago=time_ago)
    else:
        # Handle case when job is not found
        return "Job not found"
    
@app.route('/submit_message', methods=['POST'])
def submit_message():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    
    # Insert the data into the database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO contactform (Name, Email, Message, Time) VALUES (%s, %s, %s, NOW())",
                (name, email, message))
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('index'))

def time_ago(date):
    now = datetime.datetime.now()
    delta = now - date
    if delta.days == 0:
        if delta.seconds < 60:
            return "just now"
        elif delta.seconds < 3600:
            return f"{delta.seconds // 60} minutes ago"
        else:
            return f"{delta.seconds // 3600} hours ago"
    elif delta.days == 1:
        return "yesterday"
    else:
        return f"{delta.days} days ago"
    
if __name__=="__main__":
    app.run(debug=True)