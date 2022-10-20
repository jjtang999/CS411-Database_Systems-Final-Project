SELECT c.CourseSubject, c.CourseNumber, rich.Name
FROM CourseOffering c
JOIN (
	SELECT Name
	FROM Faculty
	WHERE Salary > 100000
    ) AS rich ON c.PrimaryInstructor = rich.Name