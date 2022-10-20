CREATE DATABASE course_explorer;

CREATE TABLE Course (
    Subject VARCHAR(5),
    Number INT,
    Name VARCHAR(255),
    Description TEXT,
    CreditHours VARCHAR(15),
    PRIMARY KEY(Subject, Number)
);

CREATE TABLE Faculty(
    Name VARCHAR(225) NOT NULL PRIMARY KEY,
    Salary REAL,
    DepartmentCode INT,
    CollegeCode VARCHAR(5),

    FOREIGN KEY (DepartmentCode) REFERENCES Department(DepartmentCode),
    FOREIGN KEY (CollegeCode) REFERENCES College(CollegeCode)
);

CREATE TABLE College (
    CollegeCode VARCHAR(5) NOT NULL PRIMARY KEY,
    CollegeName VARCHAR(225)
);

CREATE TABLE Department (
    DepartmentCode INT NOT NULL PRIMARY KEY,
    DepartmentName VARCHAR(255)
);

CREATE TABLE GenEd (
    Abbreviation VARCHAR(5) NOT NULL PRIMARY KEY
);

CREATE TABLE CourseOffering(
    Yr INT,
    Term VARCHAR(10),
    CourseSubject VARCHAR(5),
    CourseNumber INT,
    Ap INT,
    A INT,
    Am INT,
    Bp INT,
    B INT,
    Bm INT,
    Cp INT,
    C INT,
    Cm INT,
    Dp INT,
    D INT,
    Dm INT,
    F INT,
    W INT,
    PrimaryInstructor VARCHAR(255),
    CRN INT,
    SectionNumber VARCHAR(5),
    StartTime TIME,
    EndTime TIME,
    DaysOfWeek VARCHAR(10),
    Buliding VARCHAR(255),
    Room VARCHAR(10),

    PRIMARY KEY (Yr, Term, CRN),
    FOREIGN KEY (CourseSubject, CourseNumber) REFERENCES Course(Subject, Number)
    FOREIGN KEY (PrimaryInstructor) REFERENCES Faculty(Name)
);



CREATE TABLE GenEdFulfillment(
    CourseNumber INT,
    CourseSubject VARCHAR(5),
    GenEdAbbreviation VARCHAR(5),

    FOREIGN KEY (CourseSubject, CourseNumber) REFERENCES Course(Subject, Number),
    FOREIGN KEY (GenEdAbbreviation) REFERENCES GenEd(Abbreviation)
);