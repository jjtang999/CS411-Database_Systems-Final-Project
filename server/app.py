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

    # The stored procedure is described in queries/course_description.sql
    cursor.callproc('CourseDescription', (subject, number))
    for result in cursor.stored_results():
        instructor_data = result.fetchall()

    return render_template('course-description.html', course=course[0], offerings=offerings, instructor_data=instructor_data)

@app.route('/professor-description/<name>')
def professor_description(name): # how to do average GPA? (according to mockup)
    # TODO: Handle errors if subject or number are invalid or do not exist
    name = name.upper()
    data = db.get_db()
    cursor = data.cursor()
    
    professor_query ="""
        SELECT Name, Salary
        FROM Faculty
        WHERE Name = %s
    """
    cursor.execute(professor_query, name)
    professor = cursor.fetchall()

    courses_taught_query = """ 
        SELECT Yr, Term, CourseSubject, CourseNumber, GenEdAbbreviation
        CourseOffering NATURAL JOIN GenEdFulfillment
        WHERE PrimaryInstructor = %s
    """
    cursor.execute(courses_taught_query, name)
    courses_taught = cursor.fetchall()

    return render_template('professor-description.html', professor=professor[0], courses_taught = courses_taught)

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

@app.route('/professor', methods=['GET', 'POST'])
def professor_crud():
    error = success = None
    if request.method == 'POST':
        if request.form['name']:
            if 'delete' in request.form:
                name = request.form['name'].upper()
                data = db.get_db()
                cursor = data.cursor()
                query = """
                    SELECT Name
                    FROM Faculty
                    WHERE Name = %s
                """
                cursor.execute(query, name)
                name = cursor.fetchall()
                # TODO: Check if there is a better way to do this without needing to check if the course exists
                if name: # Delete the professor
                    delete_query = """
                        DELETE FROM Faculty
                        WHERE Name = %s
                    """
                    cursor.execute(delete_query, name)
                    data.commit()
                    success = f'Deleted professor {name}'
                else:
                    error = f'Professor {name} does not exist'
            else:
                name = request.form['name'].upper()
                data = db.get_db()
                cursor = data.cursor()
                query = """
                    SELECT Name
                    FROM Faculty
                    WHERE Name = %s
                """
                cursor.execute(query, name)
                name = cursor.fetchall()
                if name:
                    # Update the professor
                    # TODO: Input validation on the length and type of inputs
                    update_query = """
                        UPDATE Faculty
                        SET Salary = %s, DepartmentCode = %s, CollegeCode = %s
                        WHERE Name = %s
                    """
                    cursor.execute(update_query, (request.form['salary'], request.form['departmentcode'], request.form['collegecode'], name))
                    data.commit()
                    success = f'Updated professor {name}'
                else:
                    # Insert a new professor
                    insert_query = """
                        INSERT INTO Faculty (Name, Salary, DepartmentCode, CollegeCode)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (name, request.form['salary'], request.form['departmentcode'], request.form['collegecode']))
                    data.commit()
                    success = f'Inserted professor {name}'
        else:
            error = 'name is required'
    return render_template('professor.html', success=success, error=error)

# Returns gened abbreviations as a list of strings
def get_gened_abbreviations():
    data = db.get_db()
    cursor = data.cursor()
    query = """
        SELECT Abbreviation FROM GenEd
    """

    cursor.execute(query)
    abbrs = [g[0] for g in cursor.fetchall()]
    abbrs.append("NONE")
    return abbrs

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
        if gened != 'NONE':
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

        filter_str = " AND ".join(filters)

        print(filter_str)

        print(query)
        if len(filters) > 0:
            query += f"""
                WHERE {filter_str}
            """

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
        term = request.form['term'].capitalize()

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

        dictcursor.execute(query, (salary_min, salary_max, year, term))
        results = dictcursor.fetchall()
    return render_template('rich-professor.html', results=results)

@app.route('/professor-search', methods=['GET', 'POST'])
def professor_search():
    response = None
    professor = None
    countAs = None
    countFs = None
    if request.method == 'POST':
        val = []
        where1 =  """"""
        where2 =  """"""
        flag2 = 0
        flag = 0 
        if request.form['name']:
            where1+= """ where Name = %s """
            val.append(request.form['name'])
            flag = 1

        if request.form['salary']:
            if flag == 0:
                where1+=""" where Salary = %s """
            else:
                where1+=""" and Salary = %s """
            flag = 1
            val.append(request.form['salary'])

        if request.form['deptCode']:
            if flag == 0:
                where1+=""" where DepartmentCode = %s """
            else:
                where1+=""" and DepartmentCode = %s """
            flag = 1
            val.append(request.form['deptCode'])

        if request.form['colCode']:
            if flag == 0:
                where1+=""" where CollegeCode = %s """
            else:
                where1+=""" and CollegeCode = %s """
            flag = 1
            val.append(request.form['colCode'])
        
        if request.form['fgt']:
            where2+=""" where F > %s """
            flag2 = 1
            val.append(request.form['fgt'])

        if request.form['ast']:
            if flag2 == 0:
                where2+=""" where A + Ap + Am <  %s """
            else:
                where2+=""" AND A + Ap + Am < %s """
            val.append(request.form['ast'])

        database = db.get_db()
        dbCursor = database.cursor()
        print("vals",val)
        if request.form['fgt'] or request.form['ast']:
            query = """
                    SELECT distinct f.name, f.salary, f.DepartmentCode, f.CollegeCode , failProfs.F
                    FROM Faculty f
                    JOIN (
                        SELECT PrimaryInstructor, F
                        FROM CourseOffering """ + where2 + """
                    ) AS failProfs ON f.Name = failProfs.PrimaryInstructor 
                        """ + where1 + """ ORDER BY failProfs.F DESC """
        else:
            query = """
                    SELECT distinct f.name, f.salary, f.DepartmentCode, f.CollegeCode
                    FROM Faculty f
                    """ + where1 + """ ORDER BY f.salary DESC """

        print(query)
        val = tuple(val)
        print("vals tup",len(val))
        dbCursor.execute(query, val )
        professor = dbCursor.fetchall()

        if professor:
            response = f' Professors match found '
        else:
            response =  f' No matching professor found '
    return render_template('professor_search_menu.html', response = response, professor = professor )
