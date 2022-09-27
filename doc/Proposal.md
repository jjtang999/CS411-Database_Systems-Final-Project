# Project Proposal
## Title:  UIUC Course Explorer 2.0
## Project Summary
Our project aims to provide a webpage full of more detailed information students can use when deciding to register for (or just generally examine) courses here at the university. We aim to provide detailed information on the professors, gpa’s, and times for many courses here at the university. We will also include information about courses that satisfy general education requirements. Students will be able to use our webpage to do in depth analysis on the classes they want to take.

If a student is struggling to fill a general education requirement, they could use our application to search for classes that satisfy their requirements. After finding a list of suitable courses, they can investigate information relating to the professor, including average GPA given for the course (and in general). They can also look at interesting correlations within the course data, such as how course start time and professor’s salary affects the average GPA.

## Description
Our application will be a web application that has two main parts, a course selection interface and a professor interface. The course interface will have a main table for listing courses and it will provide methods to filter and sort courses by attributes such as average GPA, start time, general education requirements, and term offered. There will also be a way to view all the information about a specific course in the list. The professor interface will provide similar functionality. Users will be able to filter and sort the list of professors by attributes like department, salary, and average GPA given. The user can also choose to select a professor individually to find out more about them.

The application will also provide an interface for updating the database. This is important for when new courses are added or information on the professors changes. All CRUD functionality will be available for the courses and the professors.


## Usefulness
Every student at UIUC is familiar with the Course Explorer, a powerful tool that helps students plan out their courses for a given semester. Students also regularly use other online resources like Wade Fagen-Ulmschneider’s Grade Disparity and RateMyProfessor. Although, individually, these websites are invaluable, they each serve a different purpose, and students are required to access each resource independently to make informed decisions.

UIUC Course Explorer 2.0 unifies the multitude of course resources, allowing students to take advantage of historical course and faculty data to make the most of their college career. Through our application, students can gain insight into trends regarding course GPA, graduation requirements, departments, and faculty at UIUC. For example, students looking to fulfill their Advanced Composition requirement may be interested in finding courses offered during a particular semester, on a particular day, within a particular range of average GPAs. Although Course Explorer offers information about course terms and timings and the GenEd by GPA visualization offers information about course grades, there is no application that combines both functionalities.


## Realness
We will retrieve our data from Wade Fagen-Ulmchneider’s Useful Datasets (https://github.com/wadefagen/datasets). This Github repository contains directories corresponding to many datasets, four of which are of interest to us. We will be using the graybook, gpa, geneds, and course catalog datasets. The graybook dataset includes information about every faculty member at the university. The gpa dataset contains information about the grades that students recieved in classes, along with the professors that taught each class. The geneds dataset marks classes with the general education requirements they fulfill. Lastly, the course catalog dataset contains information on all the courses offered, including the start and end time, the course description, and the term(s) it was offered.

Each directory contains multiple CSV files with data from different years. The CSV format will make it easy for us to begin working with the data. We can get the data by cloning the repository and migrating the CSV files to our SQL database. We will have to perform some manipulation to extract out common information into separate tables. We will provide more detail on the table structure in stage 2.

## Functionality

Our project will provide four major units of functionality: A course search menu, an in-depth course information space, a professor search menu, and an in-depth professor information space. The course search menu will have search functionality for name and number, and filter options for general education requirements, department, term, days of the week, and subject.
There will aslo be sort options for average GPA, number, start time, and end time.
The in-depth course information space will allow users to view all times the course has been offered, professors that have taught the course, and GPA statistics for each offering.

The professor search menu will have search functionality for name, and filter options for college, and department. There will also be sort options for salary, average GPA given, and number of students taught.
The in-depth professor information space will allow users to view courses the professor taught, GPA data for each course taught, and the professor's salary.


There will also be interfaces for performing CRUD operations on the professor and course information.

## UI Mockup
[https://github.com/cs411-alawini/fa22-cs411-Q-team042-StoredProcedures/blob/main/doc/UI%20Mockup-2.pdf](https://github.com/cs411-alawini/fa22-cs411-Q-team042-StoredProcedures/blob/main/doc/UI%20Mockup-2.pdf)

## Project Work Distribution
We will distribute the tasks defined in step 8 evenly among the four members of our group. Kshitij will complete the course search menu. Ryan will complete the course information page and the CRUD operations on courses. Ayush will complete the professor search menu. Justin will complete the professor information page and the CRUD operations for professors. Each member will be responsible for building the frontend and backend for their section.

For the course and professor search menu, Kshitij and Ayush will be responsible for creating a search form that can be submitted to yield a list of matching courses and professors. Every course and professor in the list will be linked to a corresponding course and professor information page. Ryan and Justin will be responsible for creating relevant data regarding courses and professors in an appropriate format. Additionally, Ryan and Justin will implement Create, Update, and Delete operations in the backend.

The entire group will work together on creating the tables and importing the CSV data into a SQL database. This will ensure that everybody has an understanding of our database schema and the relationships. 
