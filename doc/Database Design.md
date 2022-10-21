# Query 1: Course taught by well-paid instructors

```SQL
EXPLAIN ANALYZE
SELECT c.CourseSubject, c.CourseNumber, rich.Name
FROM CourseOffering c
JOIN (
	SELECT Name
	FROM Faculty
	WHERE Salary > 50000
    ) AS rich ON c.PrimaryInstructor = rich.Name
WHERE Yr > 2015 AND Term = "FALL"
```

## Indexing
### Index on salary

```SQL
CREATE INDEX salary_idx ON Faculty(Salary);
CREATE INDEX year_idx ON CourseOffering(Yr);
CREATE INDEX term_idx ON CourseOffering(Term);
```
Before Index



# Query 2: Instructors who give at least 5 F's, sorted descending

```SQL
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
```

## Index
Index on number of F's given

```SQL
CREATE INDEX f_index ON CourseOffering(F);
```

## Before Index
```
-> Nested loop inner join  (cost=1395.68 rows=4844) (actual time=2.825..3.473 rows=284 loops=1)
    -> Sort: CourseOffering.F DESC  (cost=507.65 rows=4844) (actual time=2.790..2.820 rows=284 loops=1)
        -> Filter: ((CourseOffering.F > 5) and (CourseOffering.PrimaryInstructor is not null))  (cost=507.65 rows=4844) (actual time=0.097..2.656 rows=284 loops=1)
            -> Table scan on CourseOffering  (cost=507.65 rows=4844) (actual time=0.089..2.329 rows=5080 loops=1)
    -> Filter: (f.`Name` = CourseOffering.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.002..0.002 rows=1 loops=284)
        -> Single-row index lookup on f using PRIMARY (Name=CourseOffering.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.002..0.002 rows=1 loops=284)
```


## After Index
```
-> Nested loop inner join  (cost=227.46 rows=284) (actual time=0.439..2.760 rows=284 loops=1)
    -> Filter: (CourseOffering.PrimaryInstructor is not null)  (cost=128.06 rows=284) (actual time=0.421..2.037 rows=284 loops=1)
        -> Index range scan on CourseOffering using f_index, with index condition: (CourseOffering.F > 5)  (cost=128.06 rows=284) (actual time=0.419..2.013 rows=284 loops=1)
    -> Filter: (f.`Name` = CourseOffering.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.002..0.002 rows=1 loops=284)
        -> Single-row index lookup on f using PRIMARY (Name=CourseOffering.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.002..0.002 rows=1 loops=284)
```

