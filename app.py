import os
import re
from flask import Flask, render_template, request, redirect, session, url_for, flash
from ocr import ocr
import csv
import MySQLdb

app = Flask(__name__)
app.secret_key = '12345'

UPLOADS = '/static/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg']) 

# database configuration
db = MySQLdb.connect(
        host = "localhost",
        user = "root",
        passwd = "password",
        db = "ocrapp"
)

def allowed_file(filename):
        return  '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
        return render_template('index.html')

@app.route('/upload', methods=['GET'])
def upload():
        return render_template('upload.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
        if request.method == 'POST':
                if 'file' not in request.files:
                        return render_template('upload.html', msg='No file selected')
                file = request.files['file']

                if file.filename == '':
                        return render_template('upload.html', msg='No file selected')

                if file and allowed_file(file.filename):

                        extracted_text = ocr(file)                     
                        session['extracted_text'] = extracted_text
                        return render_template('submit.html', 
                                                extracted_text=extracted_text,
                                                img_src = UPLOADS + file.filename)
 
@app.route('/new_record', methods=['POST'])
def new_record():
        if request.method == 'POST':
                if request.form['store'] == 'Store customer information':
                        customer_info = session.get("extracted_text", None)

                        #regex for each field in customer information
                        pattern_list = [r'(?<=Date: ).*', 
                                        r'(?<=Customer name: ).*',
                                        r'(?<=ID card number: ).*', 
                                        r'(?<=Email-address: ).*', 
                                        r'(?<=Mobile phone number: ).*',
                                        r'(?<=Customer signature: ).*'
                                        ]
                        
                        pattern = re.compile('|'.join(pattern_list)) #combine the regex in pattern_list with '|' and compile it
                        matches = pattern.findall(customer_info) #find all the matches from extracted text of image
                        myList = [match for match in matches] #matches found stored inside list
                     
                        #print each match inside matches to check if there are any unexpected errors
                        for match in matches: 
                                print(match) 
                        
                        #writes latest customer information inside csv file
                        with open("customer.csv", "w", newline='') as csv_file:
                                wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
                                wr.writerow(myList)

                        cur = db.cursor()
                        csv_data = csv.reader(open('customer.csv'))
                        for row in csv_data:    
                                cur.execute('INSERT IGNORE INTO customers (date, name, id_number, email, mobile_number, signature) VALUES(%s, %s, %s, %s, %s, %s)', row)
                                print("The following row has been added to the database: ", row)
                        
                        db.commit()
                        cur.close()
                        
                return render_template('new_record.html', customer_info=customer_info)
        
@app.route('/records', methods=['GET'])
def records(): 
        if request.method == 'GET':
                cur = db.cursor()
                entries = cur.execute("SELECT * FROM customers")
                data = cur.fetchall()
                if entries > 0:
                        return render_template('records.html', data=data)
                else:
                        msg = "No customer records found!"
                        return render_template('records.html', msg=msg)  
                cur.close()

@app.route('/delete_record/<string:id_number>', methods=['POST'])
def delete_record(id_number):
        if request.method == 'POST':
                cur = db.cursor()
                
                entries = cur.execute("DELETE FROM customers where id_number = %s", [id_number])
                if entries > 0: 
                        flash("Record deleted!")
                db.commit()
                cur.close()
                return redirect(url_for('records'))

if __name__ == '__main__':
    app.run(debug=True)