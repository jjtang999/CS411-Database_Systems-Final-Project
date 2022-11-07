-- Takes in a Subject and Course Number and returns a table with the instructors that 
-- have taught the course along with the average GPA of their students and the most common
-- grade given.
DELIMITER $$

CREATE PROCEDURE CourseDescription(IN Subject VARCHAR(5), IN Number INT)
BEGIN
    DECLARE currName VARCHAR(255);
    DECLARE currAp INT;
    DECLARE currA INT;
    DECLARE currAm INT;
    DECLARE currBp INT;
    DECLARE currB INT;
    DECLARE currBm INT;
    DECLARE currCp INT;
    DECLARE currC INT;
    DECLARE currCm INT;
    DECLARE currDp INT;
    DECLARE currD INT;
    DECLARE currDm INT;
    DECLARE currF INT;
    DECLARE currW INT;

    DECLARE currGPA REAL;
    DECLARE currGrade VARCHAR(5);

    DECLARE exit_loop BOOLEAN DEFAULT FALSE;
    DECLARE cur CURSOR FOR
    SELECT Name, SUM(Ap) as Ap, SUM(A) as A, SUM(Am) as Am, SUM(Bp) as Bp, SUM(B) as B, SUM(Bm) as Bm, SUM(Cp) as Cp, SUM(C) as C, SUM(Cm) as Cm, SUM(Dp) as Dp, SUM(D) as D, SUM(Dm) as Dm, SUM(F) as F, SUM(W) as W
    FROM CourseOffering c JOIN Faculty f ON(c.PrimaryInstructor = f.Name)
    WHERE CourseSubject = Subject AND CourseNumber = Number
    GROUP BY PrimaryInstructor;
    
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE;
    
    DROP TABLE IF EXISTS NewTable;
    CREATE TABLE NewTable (
        Name VARCHAR(255),
        AvgGPA REAL,
        MCG VARCHAR(5) --  The most common grade
    );


    Open cur;

    cloop: LOOP
        
        Fetch cur into currName, currAp, currA, currAm, currBp, currB, currBm, currCp, currC, currCm, currDp, currD, currDm, currF, currW;
        
        IF (exit_loop) THEN
            LEAVE cloop;
        END IF;
        
        SET currGPA = (4.0 * currAp + 4.0 * currA + 3.7 * currAm + 3.3 * currBp + 3.0 * currB + 2.7 * currBm + 2.3 * currCp + 2.0 * currC + 1.7 * currCm + 1.3 * currDp + 1.0 * currD + 0.7 * currDm) / (currAp + currA + currAm + currBp + currB + currBm + currCp + currC + currCm + currDp + currD + currDm + currF + currW);
        IF (currAp > currA AND currAp > currAm AND currAp > currBp AND currAp > currB AND currAp > currBm AND currAp > currCp AND currAp > currC AND currAp > currCm AND currAp > currDp AND currAp > currD AND currAp > currDm AND currAp > currF AND currAp > currW) THEN
            SET currGrade = "A+";
        ELSEIF (currA > currAp AND currA > currAm AND currA > currBp AND currA > currB AND currA > currBm AND currA > currCp AND currA > currC AND currA > currCm AND currA > currDp AND currA > currD AND currA > currDm AND currA > currF AND currA > currW) THEN
            SET currGrade = "A";
        ELSEIF (currAm > currAp AND currAm > currA AND currAm > currBp AND currAm > currB AND currAm > currBm AND currAm > currCp AND currAm > currC AND currAm > currCm AND currAm > currDp AND currAm > currD AND currAm > currDm AND currAm > currF AND currAm > currW) THEN
            SET currGrade = "A-";
        ELSEIF (currBp > currAp AND currBp > currA AND currBp > currAm AND currBp > currB AND currBp > currBm AND currBp > currCp AND currBp > currC AND currBp > currCm AND currBp > currDp AND currBp > currD AND currBp > currDm AND currBp > currF AND currBp > currW) THEN
            SET currGrade = "B+";
        ELSEIF (currB > currAp AND currB > currA AND currB > currAm AND currB > currBp AND currB > currBm AND currB > currCp AND currB > currC AND currB > currCm AND currB > currDp AND currB > currD AND currB > currDm AND currB > currF AND currB > currW) THEN
            SET currGrade = "B";
        ELSEIF (currBm > currAp AND currBm > currA AND currBm > currAm AND currBm > currBp AND currBm > currB AND currBm > currCp AND currBm > currC AND currBm > currCm AND currBm > currDp AND currBm > currD AND currBm > currDm AND currBm > currF AND currBm > currW) THEN
            SET currGrade = "B-";
        ELSEIF (currCp > currAp AND currCp > currA AND currCp > currAm AND currCp > currBp AND currCp > currB AND currCp > currBm AND currCp > currC AND currCp > currCm AND currCp > currDp AND currCp > currD AND currCp > currDm AND currCp > currF AND currCp > currW) THEN
            SET currGrade = "C+";
        ELSEIF (currC > currAp AND currC > currA AND currC > currAm AND currC > currBp AND currC > currB AND currC > currBm AND currC > currCp AND currC > currCm AND currC > currDp AND currC > currD AND currC > currDm AND currC > currF AND currC > currW) THEN
            SET currGrade = "C";
        ELSEIF (currCm > currAp AND currCm > currA AND currCm > currAm AND currCm > currBp AND currCm > currB AND currCm > currBm AND currCm > currCp AND currCm > currC AND currCm > currDp AND currCm > currD AND currCm > currDm AND currCm > currF AND currCm > currW) THEN
            SET currGrade = "C-";
        ELSEIF (currDp > currAp AND currDp > currA AND currDp > currAm AND currDp > currBp AND currDp > currB AND currDp > currBm AND currDp > currCp AND currDp > currC AND currDp > currCm AND currDp > currD AND currDp > currDm AND currDp > currF AND currDp > currW) THEN
            SET currGrade = "D+";
        ELSEIF (currD > currAp AND currD > currA AND currD > currAm AND currD > currBp AND currD > currB AND currD > currBm AND currD > currCp AND currD > currC AND currD > currCm AND currD > currDp AND currD > currDm AND currD > currF AND currD > currW) THEN
            SET currGrade = "D";
        ELSEIF (currDm > currAp AND currDm > currA AND currDm > currAm AND currDm > currBp AND currDm > currB AND currDm > currBm AND currDm > currCp AND currDm > currC AND currDm > currCm AND currDm > currDp AND currDm > currD AND currDm > currF AND currDm > currW) THEN
            SET currGrade = "D-";
        ELSEIF (currF > currAp AND currF > currA AND currF > currAm AND currF > currBp AND currF > currB AND currF > currBm AND currF > currCp AND currF > currC AND currF > currCm AND currF > currDp AND currF > currD AND currF > currDm AND currF > currW) THEN
            SET currGrade = "F";
        ELSEIF (currW > currAp AND currW > currA AND currW > currAm AND currW > currBp AND currW > currB AND currW > currBm AND currW > currCp AND currW > currC AND currW > currCm AND currW > currDp AND currW > currD AND currW > currDm AND currW > currF) THEN
            SET currGrade = "W";
        END IF;
        
        INSERT IGNORE INTO NewTable VALUES (currName, currGPA, currGrade);
    
    END LOOP cloop;
    close cur;

    SELECT * FROM NewTable ORDER BY AvgGPA DESC;
END$$

DELIMITER ;