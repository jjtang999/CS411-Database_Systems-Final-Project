from flask import Flask, render_template, request
from . import db

app = Flask(__name__)

app.config['DB_HOST'] = '35.202.82.95'
app.config['DB_USER'] = 'root'
app.config['DB_PASSWORD'] = '' # Do not commit the password to the repo
app.config['DB_NAME'] = 'course_explorer'

db.init_app(app)

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