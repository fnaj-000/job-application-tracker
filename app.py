from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Root1234!',  # Replace with your actual MySQL password
        database='job_tracker'
    )

@app.route('/')
def dashboard():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT COUNT(*) as count FROM applications')
        stats = cursor.fetchone()
        conn.close()
    except Exception as e:
        stats = {'count': 0}
        print(f"Database error: {e}")
        
    return render_template('dashboard.html', stats=stats)

@app.route('/companies')
def companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM companies')
    companies_list = cursor.fetchall()
    conn.close()
    return render_template('companies.html', companies=companies_list)

@app.route('/companies/add', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        company_name = request.form['company_name']
        industry = request.form['industry']
        website = request.form['website']
        city = request.form['city']
        state = request.form['state']
        notes = request.form['notes']
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO companies (company_name, industry, website, city, state, notes) VALUES (%s, %s, %s, %s, %s, %s)',
            (company_name, industry, website, city, state, notes)
        )
        conn.commit()
        conn.close()
        return redirect('/companies')
        
    return render_template('add_company.html')

@app.route('/jobs')
def jobs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT jobs.*, companies.company_name 
        FROM jobs 
        LEFT JOIN companies ON jobs.company_id = companies.company_id
    ''')
    jobs_list = cursor.fetchall()
    conn.close()
    return render_template('jobs.html', jobs=jobs_list)

@app.route('/jobs/add', methods=['GET', 'POST'])
def add_job():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        company_id = request.form['company_id']
        job_title = request.form['job_title']
        location = request.form['location']
        job_type = request.form['job_type']
        salary_range = request.form['salary_range']
        status = request.form['status']
        job_description = request.form['job_description']
        
        cursor.execute(
            '''INSERT INTO jobs (company_id, job_title, location, job_type, salary_range, status, job_description) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)''',
            (company_id, job_title, location, job_type, salary_range, status, job_description)
        )
        conn.commit()
        conn.close()
        return redirect('/jobs')
        
    cursor.execute('SELECT * FROM companies')
    companies_list = cursor.fetchall()
    conn.close()
    return render_template('add_job.html', companies=companies_list)

@app.route('/applications')
def applications():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT applications.*, jobs.job_title, companies.company_name 
        FROM applications 
        LEFT JOIN jobs ON applications.job_id = jobs.job_id
        LEFT JOIN companies ON jobs.company_id = companies.company_id
    ''')
    applications_list = cursor.fetchall()
    conn.close()
    return render_template('applications.html', applications=applications_list)

@app.route('/applications/add', methods=['GET', 'POST'])
def add_application():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        job_id = request.form['job_id']
        application_date = request.form['application_date']
        status = request.form['status']
        notes = request.form['notes']
        
        cursor.execute(
            '''INSERT INTO applications (job_id, application_date, status, notes) 
               VALUES (%s, %s, %s, %s)''',
            (job_id, application_date, status, notes)
        )
        conn.commit()
        conn.close()
        return redirect('/applications')
        
    cursor.execute('SELECT * FROM jobs')
    jobs_list = cursor.fetchall()
    conn.close()
    return render_template('add_application.html', jobs=jobs_list)

@app.route('/contacts')
def contacts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT contacts.*, companies.company_name 
        FROM contacts 
        LEFT JOIN companies ON contacts.company_id = companies.company_id
    ''')
    contacts_list = cursor.fetchall()
    conn.close()
    return render_template('contacts.html', contacts=contacts_list)

@app.route('/contacts/add', methods=['GET', 'POST'])
def add_contact():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        company_id = request.form['company_id']
        contact_name = request.form['contact_name']
        title = request.form['title']
        email = request.form['email']
        phone = request.form['phone']
        notes = request.form['notes']
        
        cursor.execute(
            '''INSERT INTO contacts (company_id, contact_name, title, email, phone, notes) 
               VALUES (%s, %s, %s, %s, %s, %s)''',
            (company_id, contact_name, title, email, phone, notes)
        )
        conn.commit()
        conn.close()
        return redirect('/contacts')
        
    cursor.execute('SELECT * FROM companies')
    companies_list = cursor.fetchall()
    conn.close()
    return render_template('add_contact.html', companies=companies_list)

@app.route('/job-match')
def job_match():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    # Ranking logic using only confirmed existing columns (job_type)
    cursor.execute('''
        SELECT jobs.*, companies.company_name,
        (
            CASE WHEN jobs.job_type LIKE '%Remote%' THEN 50 
                 WHEN jobs.job_type LIKE '%Full-time%' THEN 40 
                 ELSE 20 END
        ) AS match_score
        FROM jobs 
        LEFT JOIN companies ON jobs.company_id = companies.company_id
        ORDER BY match_score DESC
    ''')
    ranked_jobs = cursor.fetchall()
    conn.close()
    return render_template('job_match.html', jobs=ranked_jobs)

if __name__ == '__main__':
    app.run(debug=True)