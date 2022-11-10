from flask import Flask, render_template, request
from . import db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['DB_HOST'] = '35.202.82.95'
app.config['DB_USER'] = 'root'
app.config['DB_PASSWORD'] = os.getenv('DB_PASSWORD') # Do not commit the password to the repo
app.config['DB_NAME'] = 'course_explorer'

db.init_app(app)

@app.route('/')
def front_page():
    return render_template('front-page.html')

@app.route('/course-description/<subject>/<number>')
def course_description(subject, number):
    # TODO: Handle errors if subject or number are invalid or do not exist
    subject = subject.upper()
    number = int(number)
    data = db.get_db()
    cursor = data.cursor()
    
    course_query ="""
        SELECT Subject, Number, Name
        FROM Course
        WHERE Subject = %s AND Number = %s
    """
    cursor.execute(course_query, (subject, number))
    course = cursor.fetchall()

    offerings_query = """
        SELECT Yr, Term, SectionNumber, PrimaryInstructor, StartTime, EndTime, DaysOfWeek, Buliding, Room
        FROM CourseOffering
        WHERE CourseSubject = %s AND CourseNumber = %s
    """
    cursor.execute(offerings_query, (subject, number))
    offerings = cursor.fetchall()

    cursor.callproc('CourseDescription', (subject, number))
    for result in cursor.stored_results():
        instructor_data = result.fetchall()

    return render_template('course-description.html', course=course[0], offerings=offerings, instructor_data=instructor_data)

@app.route('/course', methods=['GET', 'POST'])
def course_crud():
    error = success = None
    if request.method == 'POST':
        if request.form['subject'] and request.form['number']:
            if 'delete' in request.form:
                subject = request.form['subject'].upper()
                number = int(request.form['number'])
                data = db.get_db()
                cursor = data.cursor()
                query = """
                    SELECT Subject, Number
                    FROM Course
                    WHERE Subject = %s AND Number = %s
                """
                cursor.execute(query, (subject, number))
                course = cursor.fetchall()
                # TODO: Check if there is a better way to do this without needing to check if the course exists
                if course:
                    # Delete the course
                    delete_query = """
                        DELETE FROM Course
                        WHERE Subject = %s AND Number = %s
                    """
                    cursor.execute(delete_query, (subject, number))
                    data.commit()
                    success = f'Deleted course {subject} {number}'
                else:
                    error = f'Course {subject} {number} does not exist'
            else:
                subject = request.form['subject'].upper()
                number = int(request.form['number'])
                data = db.get_db()
                cursor = data.cursor()
                query = """
                    SELECT Subject, Number
                    FROM Course
                    WHERE Subject = %s AND Number = %s
                """
                cursor.execute(query, (subject, number))
                course = cursor.fetchall()
                if course:
                    # Update the course
                    # TODO: Input validation on the length and type of inputs
                    update_query = """
                        UPDATE Course
                        SET Name = %s, Description = %s, CreditHours = %s
                        WHERE Subject = %s AND Number = %s
                    """
                    cursor.execute(update_query, (request.form['name'], request.form['description'], request.form['credits'], subject, number))
                    data.commit()
                    success = f'Updated course {subject} {number}'
                else:
                    # Insert a new course
                    insert_query = """
                        INSERT INTO Course (Subject, Number, Name, Description, CreditHours)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (subject, number, request.form['name'], request.form['description'], request.form['credits']))
                    data.commit()
                    success = f'Inserted course {subject} {number}'
        else:
            error = 'Subject and number are required'
    return render_template('course.html', success=success, error=error)

# Returns gened abbreviations as a list of strings
def get_gened_abbreviations():
    data = db.get_db()
    cursor = data.cursor()
    query = """
        SELECT Abbreviation FROM GenEd
    """

    cursor.execute(query)
    return [g[0] for g in cursor.fetchall()]

@app.route('/course-search', methods=['GET', 'POST'])
def course_search():    
    courses = []
    gened_types = get_gened_abbreviations()

    if request.method == 'POST':
        filters = []
        filter_vals = []

        subject = request.form['subject'].upper()
        if subject != '':
            filters.append('Subject = %s')
            filter_vals.append(subject)

        number = request.form['number']
        if number != '':
            filters.append('Number = %s')
            filter_vals.append(number)

        gened = request.form['gened']
        if gened != '':
            filters.append('GenEdAbbreviation = %s')
            filter_vals.append(gened)

        data = db.get_db()
        dictcursor = data.cursor(dictionary=True)

        query = """
            SELECT DISTINCT *
            FROM Course
            LEFT JOIN GenEdFulfillment g ON
                Course.Subject = g.CourseSubject AND
                Course.Number = g.CourseNumber
        """

        print(filters)
        filter_str = " AND ".join(filters)
        if len(filters) > 0:
            query += f"""
                WHERE {filter_str}
            """

        print(query)

        dictcursor.execute(query, filter_vals)
        courses = dictcursor.fetchall()
    
    return render_template('course-search.html', results=courses, geneds=gened_types)

@app.route('/rich-professor', methods=['GET', 'POST'])
def rich_professor():
    results = []
    if request.method == 'POST':
        data = db.get_db()
        dictcursor = data.cursor(dictionary=True)

        year = int(request.form['year'])
        salary_min = int(request.form['salary_min'])
        salary_max = int(request.form['salary_max'])

        query = """
            SELECT c.CourseSubject, c.CourseNumber, rich.Name, rich.Salary
            FROM CourseOffering c
            JOIN (
                SELECT Name, Salary
                FROM Faculty
                WHERE Salary >= %s AND Salary <= %s
                ) AS rich ON c.PrimaryInstructor = rich.Name
            WHERE Yr = %s AND Term = %s
            ORDER BY rich.Salary DESC
        """

        dictcursor.execute(query, (salary_min, salary_max, year))
        results = dictcursor.fetchall()
    return render_template('rich-professor.html', results=results)

@app.route('/professor-search', methods=['GET', 'POST'])
def professor_search():
    response = None
    professor = None
    if request.method == 'POST':
        print(request.form['name'])
        if request.form['name']:
            # profName = request.form['name'][0].upper() + request.form['name'][1:].lower()
            profName = request.form['name']
            database = db.get_db()
            dbCursor = database.cursor()
            query = """
                SELECT Name, Salary, DepartmentCode, CollegeCode
                FROM Faculty 
                WHERE Name = %s 
            """
            dbCursor.execute(query, [profName] )
            professor = dbCursor.fetchall()
            print("Professor sql output: ",professor)
            # Checking if query was successfull 
            if professor:
                response = f'Professor {profName} found '
            else:
                response =  f'Professor {profName} does not exist'
        else:
            response = 'Professor Name is required'
    return render_template('professor_search_menu.html', response = response, professor = professor )
