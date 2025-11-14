CREATE DATABASE carinsurancedb;
USE carinsurancedb;

-----------------------------------------------------------
-- 1. Table: agent
-----------------------------------------------------------
CREATE TABLE agent (
    agentID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    branch VARCHAR(100)
);

-----------------------------------------------------------
-- 2. Table: agent_archive
-----------------------------------------------------------
CREATE TABLE agent_archive (
    archiveID INT AUTO_INCREMENT PRIMARY KEY,
    agentID INT NOT NULL,
    name VARCHAR(100),
    deleted_at DATETIME,
    FOREIGN KEY (agentID) REFERENCES agent(agentID)
        ON DELETE CASCADE
);

-----------------------------------------------------------
-- 3. Table: customer
-----------------------------------------------------------
CREATE TABLE customer (
    customerID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    DOB DATE,
    address VARCHAR(255),
    phone VARCHAR(20),
    email VARCHAR(100)
);

-----------------------------------------------------------
-- 4. Table: car
-----------------------------------------------------------
CREATE TABLE car (
    carID INT AUTO_INCREMENT PRIMARY KEY,
    registrationNumber VARCHAR(50) UNIQUE,
    model VARCHAR(100),
    manufacturer VARCHAR(100),
    year INT,
    customerID INT,
    FOREIGN KEY (customerID) REFERENCES customer(customerID)
        ON DELETE CASCADE
);

-----------------------------------------------------------
-- 5. Table: policy
-----------------------------------------------------------
CREATE TABLE policy (
    policyID INT AUTO_INCREMENT PRIMARY KEY,
    policyNumber VARCHAR(50) UNIQUE NOT NULL,
    startDate DATE,
    endDate DATE,
    premiumAmount DECIMAL(10,2),
    coverageDetails TEXT,
    customerID INT,
    carID INT,
    FOREIGN KEY (customerID) REFERENCES customer(customerID)
        ON DELETE CASCADE,
    FOREIGN KEY (carID) REFERENCES car(carID)
        ON DELETE CASCADE
);

-----------------------------------------------------------
-- 6. Table: claim
-----------------------------------------------------------
CREATE TABLE claim (
    claimID INT AUTO_INCREMENT PRIMARY KEY,
    claimDate DATE,
    claimAmount DECIMAL(10,2),
    status VARCHAR(50),
    policyID INT,
    FOREIGN KEY (policyID) REFERENCES policy(policyID)
        ON DELETE CASCADE
);

-----------------------------------------------------------
-- 7. Table: payment
-----------------------------------------------------------
CREATE TABLE payment (
    paymentID INT AUTO_INCREMENT PRIMARY KEY,
    paymentDate DATE,
    modeOfPayment VARCHAR(50),
    amount DECIMAL(10,2),
    policyID INT,
    FOREIGN KEY (policyID) REFERENCES policy(policyID)
        ON DELETE CASCADE
);

-----------------------------------------------------------
-- 8. Table: assignedto
-- (agent assigned to customer)
-----------------------------------------------------------
CREATE TABLE assignedto (
    agentID INT,
    customerID INT,
    PRIMARY KEY (agentID, customerID),
    FOREIGN KEY (agentID) REFERENCES agent(agentID)
        ON DELETE CASCADE,
    FOREIGN KEY (customerID) REFERENCES customer(customerID)
        ON DELETE CASCADE
);
1. agent
INSERT INTO agent (name, phone, email, branch) VALUES
('Rohit Sharma', '9876543210', 'rohit.agent@example.com', 'Bangalore'),
('Aditi Verma', '9123456780', 'aditi.verma@example.com', 'Mumbai'),
('Karan Mehta', '9811122233', 'karan.mehta@example.com', 'Delhi');

2. agent_archive
INSERT INTO agent_archive (agentID, name, deleted_at) VALUES
(1, 'Rohit Sharma', '2024-10-15 14:30:00');

3. customer
INSERT INTO customer (name, DOB, address, phone, email) VALUES
('Dhruv Thakur', '2004-07-15', 'Indiranagar, Bangalore', '9902651000', 'dhruv@example.com'),
('Sneha Kapoor', '1999-03-11', 'Andheri West, Mumbai', '9876001122', 'sneha.k@example.com'),
('Arjun Rao', '1988-12-05', 'Koramangala, Bangalore', '9988776655', 'arjunrao@example.com');

4. car
INSERT INTO car (registrationNumber, model, manufacturer, year, customerID) VALUES
('KA03AB1234', 'i20', 'Hyundai', 2020, 1),
('MH12XY9876', 'Swift', 'Maruti Suzuki', 2018, 2),
('KA05MN4567', 'City', 'Honda', 2019, 3);

5. policy
INSERT INTO policy (policyNumber, startDate, endDate, premiumAmount, coverageDetails, customerID, carID) VALUES
('POL2024001', '2024-01-01', '2025-01-01', 15000.00, 'Comprehensive Coverage', 1, 1),
('POL2024002', '2024-02-15', '2025-02-15', 13000.00, 'Third-Party Coverage', 2, 2),
('POL2024003', '2024-03-10', '2025-03-10', 18000.00, 'Zero Depreciation', 3, 3);

6. claim
INSERT INTO claim (claimDate, claimAmount, status, policyID) VALUES
('2024-06-20', 12000.00, 'Pending', 1),
('2024-07-05', 8000.00, 'Approved', 2),
('2024-08-15', 5000.00, 'Rejected', 3);

7. payment
INSERT INTO payment (paymentDate, modeOfPayment, amount, policyID) VALUES
('2024-01-01', 'Credit Card', 15000.00, 1),
('2024-02-15', 'UPI', 13000.00, 2),
('2024-03-10', 'Net Banking', 18000.00, 3);

8. assignedto (Agent–Customer Mapping)
INSERT INTO assignedto (agentID, customerID) VALUES
(1, 1),
(1, 2),
(2, 3);

-- ===========================
-- STEP 1: DROPS & REQUIRED TABLES
-- Use default delimiter ';'
-- ===========================
USE carinsurancedb; -- ensure you're in the correct database

-- Safety drops (routines, triggers, functions)
DROP TRIGGER IF EXISTS claim_date_check;
DROP TRIGGER IF EXISTS set_payment_date;
DROP TRIGGER IF EXISTS prevent_premium_decrease;
DROP TRIGGER IF EXISTS archive_agent_on_delete;
DROP TRIGGER IF EXISTS update_user_role_check;

DROP PROCEDURE IF EXISTS AddNewCustomerAndCar;
DROP PROCEDURE IF EXISTS GetPolicyDetails;
DROP PROCEDURE IF EXISTS UpdateClaimStatus;
DROP PROCEDURE IF EXISTS RegisterNewPolicy;

DROP FUNCTION IF EXISTS CalculateCustomerAge;
DROP FUNCTION IF EXISTS GetTotalPaymentsForPolicy;
DROP FUNCTION IF EXISTS GetAgentCustomerCount;
DROP FUNCTION IF EXISTS GetTotalApprovedClaims;

-- Ensure the dependency table exists for the archive trigger
CREATE TABLE IF NOT EXISTS agent_archive (
    archiveID INT AUTO_INCREMENT PRIMARY KEY,
    agentID INT,
    name VARCHAR(100),
    deleted_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- NOTE:
-- The following script assumes you already have these tables defined:
-- customer, car, policy, claim, payment, agent, users, assignedto
-- If any do not exist, create them before proceeding to STEP 2.
-- ===========================
-- STEP 2: CREATE TRIGGERS/ROUTINES
-- Requires custom delimiter
-- ===========================
DELIMITER //

-- 1. TRIGGERS
-- 1.1 claim_date_check (BEFORE INSERT on claim)
CREATE TRIGGER claim_date_check
BEFORE INSERT ON claim
FOR EACH ROW
BEGIN
    DECLARE policy_start DATE;
    DECLARE policy_end DATE;

    -- Get the start and end dates for the policy associated with the new claim
    SELECT startDate, endDate
    INTO policy_start, policy_end
    FROM policy
    WHERE policyID = NEW.policyID
    LIMIT 1;

    -- If policy not found, signal an error
    IF policy_start IS NULL OR policy_end IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Policy not found for this claim (invalid policyID).';
    END IF;

    -- Check if the claimDate is outside the policy period
    IF NEW.claimDate < policy_start OR NEW.claimDate > policy_end THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Claim date must be within the policy period (startDate to endDate).';
    END IF;
END //

-- 1.2 set_payment_date (BEFORE INSERT on payment)
CREATE TRIGGER set_payment_date
BEFORE INSERT ON payment
FOR EACH ROW
BEGIN
    IF NEW.paymentDate IS NULL THEN
        SET NEW.paymentDate = CURDATE();
    END IF;
END //

-- 1.3 prevent_premium_decrease (BEFORE UPDATE on policy)
CREATE TRIGGER prevent_premium_decrease
BEFORE UPDATE ON policy
FOR EACH ROW
BEGIN
    IF NEW.premiumAmount < OLD.premiumAmount THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Policy premium amount cannot be reduced upon update.';
    END IF;
END //

-- 1.4 archive_agent_on_delete (BEFORE DELETE on agent)
CREATE TRIGGER archive_agent_on_delete
BEFORE DELETE ON agentpaymentpaymentIDpaymentDatepaymentDatepaymentIDpolicyIDpolicyIDpolicyID
FOR EACH ROW
BEGIN
    INSERT INTO agent_archive (agentID, name)
    VALUES (OLD.agentID, OLD.name);
END //

-- 1.5 update_user_role_check (BEFORE UPDATE on users)
CREATE TRIGGER update_user_role_check
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.role NOT IN ('admin', 'agent') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid user role specified. Role must be "admin" or "agent".';
    END IF;
END //

-- 2. STORED PROCEDURES
-- 2.1 AddNewCustomerAndCar
CREATE PROCEDURE AddNewCustomerAndCar (
    IN cName VARCHAR(100),
    IN cDOB DATE,
    IN cAddress VARCHAR(255),
    IN cPhone VARCHAR(20),
    IN cEmail VARCHAR(100),
    IN carRegNumber VARCHAR(50),
    IN carModel VARCHAR(100),
    IN carManufacturer VARCHAR(100),
    IN carYear INT
)
BEGIN
    DECLARE newCustomerID INT;
    DECLARE exit handler for sqlexception
    BEGIN
        -- rollback on error and re-signal a generic error message
        ROLLBACK;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error in AddNewCustomerAndCar; transaction rolled back.';
    END;

    START TRANSACTION;

    -- Insert the new customer
    INSERT INTO customer (name, DOB, address, phone, email)
    VALUES (cName, cDOB, cAddress, cPhone, cEmail);

    SET newCustomerID = LAST_INSERT_ID();

    -- Insert the car, linking it to the new customer
    INSERT INTO car (registrationNumber, model, manufacturer, year, customerID)
    VALUES (carRegNumber, carModel, carManufacturer, carYear, newCustomerID);

    COMMIT;

    -- Return the new IDs
    SELECT newCustomerID AS CustomerID, LAST_INSERT_ID() AS CarID;
END //

-- 2.2 GetPolicyDetails
CREATE PROCEDURE GetPolicyDetails (
    IN pID INT
)
BEGIN
    SELECT
        p.policyID,
        p.policyNumber,
        p.startDate,
        p.endDate,
        p.premiumAmount,
        c.customerID,
        c.name AS CustomerName,
        c.phone AS CustomerPhone,
        cr.carID,
        cr.registrationNumber AS CarReg,
        cr.manufacturer AS CarManufacturer,
        cr.model AS CarModel
    FROM policy p
    JOIN customer c ON p.customerID = c.customerID
    JOIN car cr ON p.carID = cr.carID
    WHERE p.policyID = pID;
END //

-- 2.3 UpdateClaimStatus
CREATE PROCEDURE UpdateClaimStatus (
    IN claimID_in INT,
    IN newStatus VARCHAR(50)
)
BEGIN
    IF newStatus IN ('Pending', 'Approved', 'Rejected', 'Closed') THEN
        UPDATE claim
        SET status = newStatus
        WHERE claimID = claimID_in;

        IF ROW_COUNT() = 0 THEN
            SELECT 'Error: Claim ID not found.' AS Result;
        ELSE
            SELECT CONCAT('Claim ', claimID_in, ' status updated to ', newStatus) AS Result;
        END IF;
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid status. Must be Pending, Approved, Rejected, or Closed.';
    END IF;
END //

-- 3. FUNCTIONS
-- 3.1 CalculateCustomerAge
CREATE FUNCTION CalculateCustomerAge (
    DOB DATE
)
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN TIMESTAMPDIFF(YEAR, DOB, CURDATE());
END //

-- 3.2 GetTotalPaymentsForPolicy
CREATE FUNCTION GetTotalPaymentsForPolicy (
    pID INT
)
RETURNS DECIMAL(10,2)
READS SQL DATA
BEGIN
    DECLARE totalAmount DECIMAL(10,2);
    SELECT COALESCE(SUM(amount), 0.00) INTO totalAmount
    FROM payment
    WHERE policyID = pID;
    RETURN totalAmount;
END //

-- 3.3 GetAgentCustomerCount
CREATE FUNCTION GetAgentCustomerCount (
    aID INT
)
RETURNS INT
READS SQL DATA
BEGIN
    DECLARE customerCount INT;
    SELECT COUNT(*) INTO customerCount
    FROM assignedto
    WHERE agentID = aID;
    RETURN customerCount;
END //

-- Optional: Example function to count approved claims (if you intended GetTotalApprovedClaims)
CREATE FUNCTION GetTotalApprovedClaims ()
RETURNS INT
READS SQL DATA
BEGIN
    DECLARE cnt INT;
    SELECT COUNT(*) INTO cnt FROM claim WHERE status = 'Approved';
    RETURN IFNULL(cnt, 0);
END //

DELIMITER ;
