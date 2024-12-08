from flask import Flask, render_template, request
from pymysql import connections
import os
import requests

app = Flask(__name__)

# Read environment variables set by Kubernetes ConfigMap
IMAGE_URL = os.environ.get("IMAGE_URL", "https://gp-12-finalproject-clo835.s3.us-east-1.amazonaws.com/sample1.jpeg")
GROUP_NAME = os.environ.get("GROUP_NAME", "GROUP12")

# Debugging to check if environment variables are loaded
print(f"GROUP_NAME: {GROUP_NAME}")
print(f"IMAGE_URL: {IMAGE_URL}")

# MySQL database connection details
DBHOST = os.environ.get("DBHOST", "localhost")
DBUSER = os.environ.get("DBUSER", "root")
DBPWD = os.environ.get("DBPWD", "password")
DATABASE = os.environ.get("DATABASE", "employees")
DBPORT = int(os.environ.get("DBPORT", 3306))

# MySQL connection setup
db_conn = connections.Connection(
    host=DBHOST,
    port=DBPORT,
    user=DBUSER,
    password=DBPWD,
    db=DATABASE
)

# Directory for storing downloaded images
DOWNLOADS_PATH = "static/downloads"
if not os.path.exists(DOWNLOADS_PATH):
    os.makedirs(DOWNLOADS_PATH)

# Download the image from the provided URL (if needed)
IMAGE_PATH = os.path.join(DOWNLOADS_PATH, "sample1.jpeg")
response = requests.get(IMAGE_URL)
if response.status_code == 200:
    with open(IMAGE_PATH, "wb") as f:
        f.write(response.content)
    print("Image downloaded successfully.")
else:
    print(f"Failed to download image. Status code: {response.status_code}")

# Define the background image path for templates
BACKGROUND_IMAGE_PATH = "/static/downloads/sample1.jpeg"
print(f"Background image path: {BACKGROUND_IMAGE_PATH}")

# Flask routes
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', background_image=BACKGROUND_IMAGE_PATH, GROUP_NAME=GROUP_NAME)

@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', background_image=BACKGROUND_IMAGE_PATH, GROUP_NAME=GROUP_NAME)

@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = f"{first_name} {last_name}"
    finally:
        cursor.close()

    return render_template('addempoutput.html', name=emp_name, background_image=BACKGROUND_IMAGE_PATH, GROUP_NAME=GROUP_NAME)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", background_image=BACKGROUND_IMAGE_PATH, GROUP_NAME=GROUP_NAME)

@app.route("/fetchdata", methods=['POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location FROM employee WHERE emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql, (emp_id,))
        result = cursor.fetchone()
        if result:
            output["emp_id"] = result[0]
            output["first_name"] = result[1]
            output["last_name"] = result[2]
            output["primary_skills"] = result[3]
            output["location"] = result[4]
        else:
            return "Employee not found."
    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"],
                           location=output["location"], background_image=BACKGROUND_IMAGE_PATH, GROUP_NAME=GROUP_NAME)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81, debug=True)
