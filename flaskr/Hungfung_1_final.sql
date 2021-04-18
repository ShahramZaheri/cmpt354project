/*create tables*/

CREATE TABLE Employee(
    EmployeeID char(7) NOT NULL,
    SIN int(9) NOT NULL,
    DateofBirth DATE NOT NULL,
    DateofHire DATE NOT NULL,
    Fname CHARACTER(100) NOT NULL,
    Mname CHARACTER(100) ,
    Lname CHARACTER(100) NOT NULL,
    Address CHARACTER(100) NOT NULL,
    PRIMARY KEY (EmployeeID)
    );
   
CREATE TABLE exEmployees(
    EmployeeID char(7) NOT NULL,
    SIN int(9) NOT NULL,
    DateofBirth DATE NOT NULL,
    DateofHire DATE NOT NULL,
    Fname CHARACTER(100) NOT NULL,
    Mname CHARACTER(100) ,
    Lname CHARACTER(100) NOT NULL,
    Address CHARACTER(100),
    TerminationDate DATE NOT NULL
    );

CREATE TABLE Vacation (
	ID char(7) NOT NULL,
    TotalVacationEarned int(100) NOT NULL,
    PercentageofGrossPay float NOT NULL,
    YearlyCarryOver int NOT NULL,
    TotalVacationPaid float NOT NULL,
    PRIMARY KEY (TotalVacationEarned, ID),
    FOREIGN KEY (ID) REFERENCES Employee(EmployeeID)
    ON DELETE CASCADE
    );


CREATE TABLE EmergencyContact(
    ContactName CHARACTER(100) NOT NULL,
    PhoneNumber char(20) NOT NULL,
    Relation CHARACTER(100) NOT NULL,
    ID CHARACTER(7) NOT NULL,
    PRIMARY KEY (ContactName, ID),
    FOREIGN KEY (ID) REFERENCES Employee(EmployeeID)
    ON DELETE CASCADE
  );
    
CREATE TABLE Office(
    ID char(7) NOT NULL,
    Salary int(9) NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (ID) REFERENCES Employee(EmployeeID)
    ON DELETE CASCADE
    );
    
CREATE TABLE Operations(
    ID char(7) NOT NULL,
    WagePerHour float(9) NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (ID) REFERENCES Employee(EmployeeID)
    ON DELETE CASCADE
    );

CREATE TABLE Payroll(
    ChequeNumber char(10) NOT NULL,
    PayrollDate Date NOT NULL,
    GrossPay float(20) NOT NULL,
    CPP float NOT NULL,
    EI float NOT NULL,
    FederalTax float NOT NULL,
    ProvincialTax float NOT NULL,
    ID char(7) NOT NULL,
    PRIMARY KEY (ChequeNumber),
    FOREIGN KEY (ID) REFERENCES Employee(EmployeeID)
    ON DELETE CASCADE
    );

CREATE TABLE Shift(
	ID char(10) NOT NULL,
    ShiftID char(10) NOT NULL,
    StartTime time NOT NULL,
    EndTime time NOT NULL,
    DateofShift date NOT NULL,
    PRIMARY KEY (ShiftID),
    FOREIGN KEY (ID) REFERENCES Employee(EmployeeID)
    ON DELETE CASCADE
    );




CREATE TABLE Phone(
    PhoneNumber CHAR(20) NOT NULL,
    ID char(7) NOT NULL,
    PRIMARY KEY(PhoneNumber, ID),
    FOREIGN KEY (ID) REFERENCES Employee(EmployeeID)
    ON DELETE CASCADE
);






/*insert values*/

INSERT INTO Employee (EmployeeID, SIN, DateofBirth, DateofHire, Fname, Mname, Lname, Address)
VALUES (0001, 897586446, '1987-01-09', '2018-04-26', 'Jack', 'Young', 'Ma', '8990 Alpha Street'),
	   (0002, 397486256, '1987-04-28', '2010-03-23', 'Emma', 'Yye', 'Zhang', '8990 Beta Street'),
	   (0003, 296586884, '1980-09-01', '2012-05-16', 'Alan', 'Zhu', 'Kit', '1990 Nova Street'),
	   (0004, 697086464, '1970-03-21', '2013-01-04', 'Wilson', 'Stephan', 'Kit', '3090 Crew Street'),
       (0005, 197526335, '1990-02-09', '2015-07-07', 'Sharon', 'Yao', 'Wang', '1990 Walter Street');




INSERT INTO EmergencyContact  (ContactName, PhoneNumber, Relation, ID)
VALUES ('Belle Lu', '(889) 908-1728','Sister',0001),
       ('Wang Zhu', '(883) 902-1123','Wife',0002),
       ('Ling Che', '(183) 202-1098','Cousin',0003),
       ('Lee Hwang','(113) 204-1323','Friend',0004),
       ('Christopher Wayne','(522) 041-3623','Father',0005);


INSERT INTO Office (ID, Salary)
VALUES (0001, 60000),
       (0002, 50000);

INSERT INTO Operations(ID, WagePerHour)
VALUES (0003, 20),
       (0004, 18),
       (0005, 17);

INSERT INTO Payroll(ChequeNumber, PayrollDate, GrossPay, CPP, EI, FederalTax, ProvincialTax, ID)
VALUES (10001,'2021-03-25',5000,12,23,15,16,0001),
	   (10002,'2021-03-15',6000,12,23,15,16,0002),
       (10003,'2021-03-05',5000,12,23,15,16,0001),
       (10004,'2021-02-20',5000,12,23,15,16,0001),
       (10005,'2021-02-05',5000,12,23,15,16,0001),
       (10006,'2021-01-15',5000,12,23,15,16,0001),
       (10007,'2021-01-01',5000,12,23,15,16,0001),
       (10008,'2020-12-15',5000,12,23,15,16,0001),
       (10009,'2020-12-01',5000,12,23,15,16,0001),
       (10010,'2020-11-10',5000,12,23,15,16,0001),
       (10011,'2020-03-15',6000,12,23,15,16,0002),
       (100031,'2020-03-05',5000,12,23,15,16,0004),
       (100041,'2020-02-20',5000,12,23,15,16,0004),
       (100051,'2020-02-05',5000,12,23,15,16,0004),
       (100061,'2020-01-15',5000,12,23,15,16,0001),
       (100071,'2020-01-01',5000,12,23,15,16,0001),
       (100081,'2019-12-15',5000,12,23,15,16,0001),
       (100091,'2019-12-01',5000,12,23,15,16,0001),
       (100103,'2019-11-10',5000,12,23,15,16,0001),
       (100084,'2018-12-15',5000,12,23,15,16,0001),
       (100093,'2018-12-01',5000,12,23,15,16,0001),
       (100105,'2018-11-10',5000,12,23,15,16,0001),
       (100022,'2018-03-15',6000,12,23,15,16,0002),
       (100039,'2018-03-05',5000,12,23,15,16,0001),
       (100040,'2018-02-20',5000,12,23,15,16,0001),
       (100050,'2018-02-05',5000,12,23,15,16,0001),
       (100060,'2018-01-15',5000,12,23,15,16,0001),
       (100070,'2018-01-01',5000,12,23,15,16,0001),
       (100080,'2015-12-15',5000,12,23,15,16,0001),
       (100090,'2015-12-01',5000,12,23,15,16,0001),
       (100107,'2015-11-10',5000,12,23,15,16,0001);

INSERT INTO Phone(PhoneNumber, ID)
VALUES ('(778) 789-5645', 0001),
       ('(604) 512-3695', 0002),
	   ('(778) 956-1234', 0003),
	   ('(778) 456-1293', 0004),
	   ('(778) 236-1290', 0005);

INSERT INTO Vacation(ID, TotalVacationEarned, PercentageofGrossPay, YearlyCarryOver, TotalVacationPaid)
VALUES(0001,2000,0.4,2000,0),
	  (0002,5200,0.6,2200,3000),
	  (0003,5060,0.6,2060,3000),
	  (0004,5100,0.6,2100,3000);

INSERT INTO Shift(ID, ShiftID, StartTime, EndTime, DateofShift)
VALUES(0001,100,'12:20:01','18:10:02','2021-03-10'),
      (0002,101,'11:20:01','15:10:02','2021-03-10'),
      (0003,102,'09:20:01','14:10:06','2021-03-10'),
      (0004,103,'12:00:00','16:00:00','2021-03-10'),
      (0005,104,'12:40:01','18:10:02','2021-03-10');

CREATE TRIGGER adding_to_exEmployess
   AFTER DELETE ON Employee
BEGIN
    INSERT INTO exEmployees 
    VALUES (old.EmployeeID, old.SIN, old.DateofBirth, old.DateofHire, old.Fname, old.Mname, old.Lname, old.Address,DATETIME('NOW'));
       
END;



/*EMPLOYEE REPORT - JOIN QUERY*/
/*SELECT employee.EmployeeID, employee.Fname, employee.Lname, DATEDIFF(SYSDATE(), employee.DateofHire)/365
AS DATEDIFF, Payroll.ID, Payroll.PayrollDate, Payroll.GrossPay, Payroll.CPP, Payroll.EI, Payroll.FederalTax, Payroll.ProvincialTax 
FROM employee
INNER JOIN Payroll ON EMPLOYEE.EmployeeID = Payroll.ID;


/*Alter vacation pay value */ /*How to do it automatically
UPDATE vacation SET PercentageofGrossPay=0.6 WHERE vacation.ID IN (
 		SELECT EmployeeID FROM employee WHERE (DATEDIFF(SYSDATE(), employee.DateofHire)/365)>4 AND employee.EmployeeID = Vacation.ID);

/*Aggregation query - average weekly pay
SELECT employee.Fname, employee.Lname, payroll.ID, AVG(payroll.GrossPay/48) FROM employee,payroll
WHERE payroll.ID = employee.EmployeeID; */

