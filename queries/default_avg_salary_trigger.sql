DELIMITER //
CREATE TRIGGER default_avg_salary
    BEFORE INSERT ON Faculty
    FOR EACH ROW
    BEGIN
        SET @max_salary = (
            SELECT MAX(Salary)
            FROM Faculty
            WHERE DepartmentCode = new.DepartmentCode
        );

        IF new.Salary > 2 * @max_salary THEN
            SET new.Salary = 2 * @max_salary;
		END IF;
END; //
DELIMITER ;