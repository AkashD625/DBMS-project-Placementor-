from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'BUHDHCUE'

def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='pmsaccounts'
    )

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/admin_home')
def admin_home():
    if 'username' in session and session.get('usertype') == 'yes':
        username = session['username']
        return render_template('admin-home.html', username=username)
    else:
        return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    usertype = request.form['user-type']
    username = request.form['username']
    password = request.form['password']

    try:
        connection = create_connection()
        cursor = connection.cursor()

        select_query = "SELECT * FROM accountcreation WHERE username = %s AND password = %s AND usertype = %s"
        cursor.execute(select_query, (username, password, usertype))
        account = cursor.fetchone()
        if account:
            session['username'] = username
            session['usertype'] = usertype

            if usertype == 'yes':
                return render_template('admin-home.html')
            else:
                flash('Not Admin')
                return render_template('student-home.html', username=username)
        else:
            flash('Wrong username or password. Please create an account.')

    except mysql.connector.Error as e:
        flash(f"Database Error: {e}")
        return redirect(url_for('index'))

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return render_template('login.html')

@app.route('/student_home')
def student_home():
    if 'username' in session:
        username = session['username']
        return render_template('student-home.html', username=username)
    else:
        return redirect(url_for('index'))

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        enroll = request.form.get('enroll')

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('create_account'))

        try:
            connection = create_connection()
            cursor = connection.cursor()

            insert_query = "INSERT INTO accountcreation (email, username, password, usertype) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (email, username, password, enroll))
            connection.commit()

            flash('Account created successfully!')
            return redirect(url_for('index'))

        except mysql.connector.Error as e:
            flash(f"Database Error: {e}")
            return redirect(url_for('index'))

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    return render_template('index.html')

@app.route('/add_company', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        company_name = request.form['companyName']

        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO comapanyname (name) VALUES (%s)", (company_name,))
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for('add_company'))

    return render_template('ad-add-comp.html')

@app.route('/account_holders')
def account_holders():
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM accountcreation")
        accounts = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('account-holders.html', accounts=accounts)
    except mysql.connector.Error as err:
        flash(f"Database error: {err}")

    return redirect(url_for('admin_home'))

@app.route('/remove_account/<username>', methods=['POST'])
def remove_account(username):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM accountcreation WHERE username = %s", (username,))
        connection.commit()
        cursor.close()
        connection.close()
        flash('Account removed successfully!')
    except mysql.connector.Error as err:
        flash(f"Database error: {err}")

    return redirect(url_for('account_holders'))

@app.route('/indexs')
def indexs():
    return render_template('company-details.html')

@app.route('/submit', methods=['POST'])
def submit():
    connection = create_connection()
    name = request.form['name']
    title = request.form['title']
    company_details = request.form['company']
    cgpa = request.form['type']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    cursor = connection.cursor()
    sql = "INSERT INTO companydetails (company_name, company_type, company_details, cgpa_required, job_post, required_skills, message) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (name, title, company_details, cgpa, email, phone, message))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('indexs'))

@app.route('/ind')
def ind():
    return render_template('student-home.html', username='John Doe')


# @app.route('/student_form')
# def student_form():
#     return render_template('student_form.html')

@app.route('/search', methods=['POST'])
def search():
    # name = request.form['name']
    cgpa = request.form['cgpa']
    skills = request.form.getlist('skills')
    connection = create_connection()
    cursor = connection.cursor()
    
    skills_placeholder = ','.join(['%s'] * len(skills))
    query = f"SELECT company_name, job_post FROM companydetails WHERE cgpa_required <= %s AND FIND_IN_SET(required_skills, %s)"
    cursor.execute(query, [cgpa] + skills)
    results = cursor.fetchall()
    # cursor.close()
    # connection.close()
    
    return render_template('company-result.html', results=results)


@app.route('/student_sort')
def student_sort():
    return render_template('student-sort.html')
# @app.route('/student-sort', methods=['GET', 'POST'])
# def student_sort():
#     companies = []
#     if request.method == 'POST':
#         name = request.form['name']
#         cgpa = request.form['cgpa']
#         skills = request.form['skills']

#         connection = create_connection()
#         cursor = connection.cursor()

#         query = """
#         SELECT company_name, company_type, job_post 
#         FROM companydetails 
#         WHERE cgpa_required <= %s AND required_skills LIKE %s
#         """
#         cursor.execute(query, (cgpa, f"%{skills}%"))
#         companies = cursor.fetchall()
#         cursor.close()
#         connection.close()

#     return render_template('student-sort.html', companies=companies)


@app.route('/company_list')
def company_list():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT company_name, company_details FROM companydetails")
    companies = cursor.fetchall()
    return render_template('com_details.html', companies=companies)

@app.route('/student2')
def student2():
    return render_template('student-home.html')

# @app.route('/search_form')
# def search_form():
#     connection = create_connection()
#     cursor = connection.cursor()
#     cursor.execute("SELECT company_name, required_skills FROM companydetails")
#     companies = cursor.fetchall()
#     return render_template('student-sort.html', companies=companies)
@app.route('/search_form')
def search_form():
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT company_name, required_skills FROM companydetails")
        companies = cursor.fetchall()
    except Exception as e:
        print("An error occurred:", e)
        companies = []  # Fallback in case of error
    finally:
        cursor.close()
        connection.close()  # Ensure the connection is closed

    return render_template('student-sort.html', companies=companies)



@app.route('/com_job')
def com_job():
    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT company_name, job_post FROM companydetails")
        companies = cursor.fetchall()
    except Exception as e:
        print("An error occurred:", e)
        companies = []  # Fallback in case of error
    finally:
        cursor.close()
        connection.close()  # Ensure the connection is closed

    return render_template('com_job.html', companies=companies)


@app.route('/priv_details')
def priv_details():
    return render_template('enter_prevdetails.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form['name']
    company = request.form['company']
    year = request.form['year']
    package = request.form['package']

    connection = create_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO prev_student_details (name, company, year, package) VALUES (%s, %s, %s, %s)",
                       (name, company, year, package))
        connection.commit()
    except Exception as e:
        print("An error occurred:", e)
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('priv_details'))

@app.route('/student_home22')
def student_home22():
       return redirect(url_for('admin_home'))






@app.route('/prev_details')
def prev_details():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT name, company, year, package FROM prev_student_details')
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    print(data) 
    return render_template('show_prev.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)