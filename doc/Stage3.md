# Query 1: Course taught by well-paid instructors

EXPLAIN ANALYZE
SELECT c.Yr
FROM CourseOffering c
JOIN (
	SELECT Name
	FROM Faculty
	WHERE Salary > 100000
    ) AS rich ON c.PrimaryInstructor = rich.Name

## Index
Index on salary

CREATE INDEX salary_idx ON Faculty(Salary);

## Before Index
# EXPLAIN
-> Nested loop inner join  (cost=2168.04 rows=8003) (actual time=0.117..11.451 rows=3087 loops=1)
    -> Filter: (Faculty.Salary > 100000)  (cost=656.50 rows=2108) (actual time=0.074..2.270 rows=2082 loops=1)
        -> Table scan on Faculty  (cost=656.50 rows=6325) (actual time=0.071..1.747 rows=6427 loops=1)
    -> Filter: (c.PrimaryInstructor = Faculty.`Name`)  (cost=0.34 rows=4) (actual time=0.003..0.004 rows=1 loops=2082)
        -> Index lookup on c using PrimaryInstructor (PrimaryInstructor=Faculty.`Name`)  (cost=0.34 rows=4) (actual time=0.003..0.004 rows=1 loops=2082)


## AFter Index
-> Nested loop inner join  (cost=2203.05 rows=1594) (actual time=0.079..12.650 rows=3087 loops=1)
    -> Filter: (c.PrimaryInstructor is not null)  (cost=507.65 rows=4844) (actual time=0.062..2.669 rows=5080 loops=1)
        -> Table scan on c  (cost=507.65 rows=4844) (actual time=0.061..2.288 rows=5080 loops=1)
    -> Filter: ((c.PrimaryInstructor = Faculty.`Name`) and (Faculty.Salary > 100000))  (cost=0.25 rows=0) (actual time=0.002..0.002 rows=1 loops=5080)
        -> Single-row index lookup on Faculty using PRIMARY (Name=c.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.001..0.001 rows=1 loops=5080)




# Query 2: Instructors who give at least 5 F's, sorted descending

DROP INDEX f_index ON CourseOffering;

EXPLAIN ANALYZE
SELECT f.name, f.salary, failProfs.F
FROM Faculty f
JOIN (
	SELECT PrimaryInstructor, F
	FROM CourseOffering
	WHERE F > 5
    ) AS failProfs ON f.Name = failProfs.PrimaryInstructor
ORDER BY failProfs.F DESC

## Index
Index on number of F's given

DROP INDEX f_index ON CourseOffering;

## Before Index
-> Nested loop inner join  (cost=1395.68 rows=4844) (actual time=2.825..3.473 rows=284 loops=1)
    -> Sort: CourseOffering.F DESC  (cost=507.65 rows=4844) (actual time=2.790..2.820 rows=284 loops=1)
        -> Filter: ((CourseOffering.F > 5) and (CourseOffering.PrimaryInstructor is not null))  (cost=507.65 rows=4844) (actual time=0.097..2.656 rows=284 loops=1)
            -> Table scan on CourseOffering  (cost=507.65 rows=4844) (actual time=0.089..2.329 rows=5080 loops=1)
    -> Filter: (f.`Name` = CourseOffering.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.002..0.002 rows=1 loops=284)
        -> Single-row index lookup on f using PRIMARY (Name=CourseOffering.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.002..0.002 rows=1 loops=284)


## After Index
-> Nested loop inner join  (cost=227.46 rows=284) (actual time=0.439..2.760 rows=284 loops=1)
    -> Filter: (CourseOffering.PrimaryInstructor is not null)  (cost=128.06 rows=284) (actual time=0.421..2.037 rows=284 loops=1)
        -> Index range scan on CourseOffering using f_index, with index condition: (CourseOffering.F > 5)  (cost=128.06 rows=284) (actual time=0.419..2.013 rows=284 loops=1)
    -> Filter: (f.`Name` = CourseOffering.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.002..0.002 rows=1 loops=284)
        -> Single-row index lookup on f using PRIMARY (Name=CourseOffering.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.002..0.002 rows=1 loops=284)

