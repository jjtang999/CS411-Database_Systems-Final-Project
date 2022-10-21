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
### Index on salary and year

```SQL
CREATE INDEX salary_idx ON Faculty(Salary);
CREATE INDEX year_idx ON CourseOffering(Yr);
```
### Index on Term
```SQL
CREATE INDEX term_idx ON CourseOffering(Term);
```

## Before Indexing
```
-> Nested loop inner join  (cost=572.27 rows=81) (actual time=0.118..7.459 rows=1577 loops=1)
    -> Filter: ((c.Term = 'FALL') and (c.Yr > 2015) and (c.PrimaryInstructor is not null))  (cost=487.50 rows=242) (actual time=0.104..3.517 rows=1668 loops=1)
        -> Index range scan on c using PRIMARY  (cost=487.50 rows=2422) (actual time=0.097..2.735 rows=5080 loops=1)
    -> Filter: ((c.PrimaryInstructor = Faculty.`Name`) and (Faculty.Salary > 50000))  (cost=0.25 rows=0) (actual time=0.002..0.002 rows=1 loops=1668)
        -> Single-row index lookup on Faculty using PRIMARY (Name=c.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.002..0.002 rows=1 loops=1668)

```

## After Indexing by Salary and Year
```
-> Nested loop inner join  (cost=572.27 rows=121) (actual time=0.156..7.177 rows=1577 loops=1)
    -> Filter: ((c.Term = 'FALL') and (c.Yr > 2015) and (c.PrimaryInstructor is not null))  (cost=487.50 rows=242) (actual time=0.141..3.484 rows=1668 loops=1)
        -> Index range scan on c using PRIMARY  (cost=487.50 rows=2422) (actual time=0.132..2.713 rows=5080 loops=1)
    -> Filter: ((c.PrimaryInstructor = Faculty.`Name`) and (Faculty.Salary > 50000))  (cost=0.25 rows=0) (actual time=0.002..0.002 rows=1 loops=1668)
        -> Single-row index lookup on Faculty using PRIMARY (Name=c.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.001..0.002 rows=1 loops=1668)

```
## After Indexing by Term  
```
-> Nested loop inner join  (cost=911.35 rows=404) (actual time=0.281..7.475 rows=1577 loops=1)
    -> Filter: ((c.Term = 'FALL') and (c.Yr > 2015) and (c.PrimaryInstructor is not null))  (cost=487.50 rows=1211) (actual time=0.125..3.541 rows=1668 loops=1)
        -> Index range scan on c using PRIMARY  (cost=487.50 rows=2422) (actual time=0.118..2.741 rows=5080 loops=1)
    -> Filter: ((c.PrimaryInstructor = Faculty.`Name`) and (Faculty.Salary > 50000))  (cost=0.25 rows=0) (actual time=0.002..0.002 rows=1 loops=1668)
        -> Single-row index lookup on Faculty using PRIMARY (Name=c.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.002..0.002 rows=1 loops=1668)

```

## Optimized Indexing
```
-> Nested loop inner join  (cost=572.27 rows=121) (actual time=0.156..7.177 rows=1577 loops=1)
    -> Filter: ((c.Term = 'FALL') and (c.Yr > 2015) and (c.PrimaryInstructor is not null))  (cost=487.50 rows=242) (actual time=0.141..3.484 rows=1668 loops=1)
        -> Index range scan on c using PRIMARY  (cost=487.50 rows=2422) (actual time=0.132..2.713 rows=5080 loops=1)
    -> Filter: ((c.PrimaryInstructor = Faculty.`Name`) and (Faculty.Salary > 50000))  (cost=0.25 rows=0) (actual time=0.002..0.002 rows=1 loops=1668)
        -> Single-row index lookup on Faculty using PRIMARY (Name=c.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.001..0.002 rows=1 loops=1668)
```

## Query 1 Final Output 
```
'BADM','445','Kurtz, Jeffrey M'
'ACCY','200','Silhan, Peter A'
'ACCY','415','Ciconte, William'
'ACCY','502','Schwartz, Rachel'
'CEE','201','Meidani, Hadi'
'CEE','202','Sivapalan, Murugesu'
'ACE','222','Stoddard, Paul B'
'CEE','310','Tutumluer, Erol'
'ACE','251','Michelson, Hope C'
'CEE','320','Golparvar Fard, Mani'
'CEE','350','Konar, Megan'
'CEE','360','Cha, Eun Jeong'
'CEE','406','Tutumluer, Erol'
'CEE','416','Benekohal, Rahim F'
'CEE','421','El-Rayes, Khaled A'
```

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

## Before Indexing
```
-> Nested loop inner join  (cost=1395.68 rows=4844) (actual time=2.825..3.473 rows=284 loops=1)
    -> Sort: CourseOffering.F DESC  (cost=507.65 rows=4844) (actual time=2.790..2.820 rows=284 loops=1)
        -> Filter: ((CourseOffering.F > 5) and (CourseOffering.PrimaryInstructor is not null))  (cost=507.65 rows=4844) (actual time=0.097..2.656 rows=284 loops=1)
            -> Table scan on CourseOffering  (cost=507.65 rows=4844) (actual time=0.089..2.329 rows=5080 loops=1)
    -> Filter: (f.`Name` = CourseOffering.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.002..0.002 rows=1 loops=284)
        -> Single-row index lookup on f using PRIMARY (Name=CourseOffering.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.002..0.002 rows=1 loops=284)
```

## After Indexing by F
```
-> Nested loop inner join  (cost=227.46 rows=284) (actual time=0.439..2.760 rows=284 loops=1)
    -> Filter: (CourseOffering.PrimaryInstructor is not null)  (cost=128.06 rows=284) (actual time=0.421..2.037 rows=284 loops=1)
        -> Index range scan on CourseOffering using f_index, with index condition: (CourseOffering.F > 5)  (cost=128.06 rows=284) (actual time=0.419..2.013 rows=284 loops=1)
    -> Filter: (f.`Name` = CourseOffering.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.002..0.002 rows=1 loops=284)
        -> Single-row index lookup on f using PRIMARY (Name=CourseOffering.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.002..0.002 rows=1 loops=284)
```
## Optimized Indexing:
```
-> Nested loop inner join  (cost=227.46 rows=284) (actual time=0.439..2.760 rows=284 loops=1)
    -> Filter: (CourseOffering.PrimaryInstructor is not null)  (cost=128.06 rows=284) (actual time=0.421..2.037 rows=284 loops=1)
        -> Index range scan on CourseOffering using f_index, with index condition: (CourseOffering.F > 5)  (cost=128.06 rows=284) (actual time=0.419..2.013 rows=284 loops=1)
    -> Filter: (f.`Name` = CourseOffering.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.002..0.002 rows=1 loops=284)
        -> Single-row index lookup on f using PRIMARY (Name=CourseOffering.PrimaryInstructor)  (cost=0.25 rows=1) (actual time=0.002..0.002 rows=1 loops=284)
```
## Query 2 Final Output
```
'Ray, Christian R','88201.58','46'
'Chen, Liqing','87550','39'
'Leveritt, John M','51510','34'
'Richards, Alicia','47318','34'
'Petrickova, Sarka','51680','33'
'Marville, Kelly','71516.93','31'
'Marville, Kelly','71516.93','30'
'Carey, Yvonne A','60855','30'
'Sydnor, Synthia','81645','30'
'Sydnor, Synthia','81645','29'
'Yang, Wendy','99000','29'
'Vazquez, Jose J','102700.02','29'
'Fraterrigo, Jennifer M','89413.64','28'
'Malhi, Ripan S','110102','28'
'Fraterrigo, Jennifer M','89413.64','28'
```
