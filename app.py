from flask import Flask,render_template,request
import pickle
import numpy as np
from flask_mysqldb import MySQL

app=Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flask'
mysql=MySQL(app)

with open("model.pkl",'rb') as file1:
    model=pickle.load(file1)

with open("scaler.pkl",'rb') as file2:
    scaler=pickle.load(file2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data",methods=['GET','POST'])
def data():
    user_data=request.form
    USMER=request.form['USMER']
    MEDICAL_UNIT=request.form['MEDICAL_UNIT']
    SEX=request.form['SEX']
    PATIENT_TYPE=request.form['PATIENT_TYPE']
    PNEUMONIA=request.form['PNEUMONIA']
    AGE=request.form['AGE']
    DIABETES=request.form['DIABETES']
    COPD=request.form['COPD']
    ASTHMA=request.form['ASTHMA']
    INMSUPR=request.form['INMSUPR']
    HIPERTENSION=request.form['HIPERTENSION']
    CARDIOVASCULAR=request.form['CARDIOVASCULAR']
    OBESITY=request.form['OBESITY']
    RENAL_CHRONIC=request.form['RENAL_CHRONIC']
    TOBACCO=request.form['TOBACCO']
    CLASIFFICATION_FINAL=request.form['CLASIFFICATION_FINAL']

    



    scaled_data=scaler.transform([[USMER, MEDICAL_UNIT, SEX, PATIENT_TYPE, PNEUMONIA,AGE,
       DIABETES, COPD, ASTHMA, INMSUPR, HIPERTENSION,
       CARDIOVASCULAR, OBESITY, RENAL_CHRONIC, TOBACCO,
       CLASIFFICATION_FINAL]])
    prediction=model.predict(scaled_data)
    cursor = mysql.connection.cursor()
    query = 'CREATE TABLE IF NOT EXISTS covid(USMER VARCHAR(10),MEDICAL_UNIT VARCHAR(10),SEX VARCHAR(10),PATIENT_TYPE VARCHAR(10),PNEUMONIA VARCHAR(10),AGE VARCHAR(10),DIABETES VARCHAR(10),COPD VARCHAR(10),ASTHMA VARCHAR(10),INMSUPR VARCHAR(10),HIPERTENSION VARCHAR(10),CARDIOVASCULAR VARCHAR(10),OBESITY VARCHAR(10),RENAL_CHRONIC VARCHAR(10),TOBACCO VARCHAR(10),CLASIFFICATION_FINAL VARCHAR(10),result VARCHAR(10))'
    cursor.execute(query)

    cursor.execute('INSERT INTO covid(USMER, MEDICAL_UNIT, SEX, PATIENT_TYPE, PNEUMONIA,AGE,DIABETES, COPD, ASTHMA, INMSUPR, HIPERTENSION,CARDIOVASCULAR, OBESITY, RENAL_CHRONIC, TOBACCO,CLASIFFICATION_FINAL,result) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(USMER, MEDICAL_UNIT, SEX, PATIENT_TYPE, PNEUMONIA,AGE,DIABETES, COPD, ASTHMA, INMSUPR, HIPERTENSION,CARDIOVASCULAR, OBESITY, RENAL_CHRONIC, TOBACCO,CLASIFFICATION_FINAL,prediction[0]))
    cursor.execute('SELECT * FROM covid')
    data=cursor.fetchall()
    mysql.connection.commit()
    cursor.close()

    return render_template("index.html",prediction=prediction,output_data = data)

if __name__ == "__main__":
    app.run(host = '127.0.0.100',debug=True)