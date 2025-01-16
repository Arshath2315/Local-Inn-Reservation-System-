
CREATE DATABASE Inn_reservation;
USE Inn_reservation;


CREATE TABLE inn_room (
    id INT PRIMARY KEY AUTO_INCREMENT,
    room_type VARCHAR(1),
    room_price DECIMAL(5,2),
    availability SMALLINT 
);

CREATE TABLE inn_customer (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(30),
    phone_number BIGINT UNIQUE
);


CREATE TABLE inn_reservation (
    id INT PRIMARY KEY AUTO_INCREMENT,
    room_type INT,
    customer_id INT,
    accommodation_days SMALLINT,
    cost DECIMAL(5,2),
    checkout TINYINT DEFAULT 0,
    FOREIGN KEY (room_type) REFERENCES inn_room(id),
    FOREIGN KEY (customer_id) REFERENCES inn_customer(id)
);


INSERT INTO inn_room (room_type, room_price, availability) VALUES
('S', 116.00, 10),
('P', 100.00, 8),
('E', 175.00, 4),
('O', 120.00, 3),
('E', 110.00, 2),
('P', 740.00, 1),
('S', 120.00, 2),
('S', 200.00, 5),
('O', 400.00, 2);

-- Switch to the Inn_reservation database
USE Inn_reservation;

INSERT INTO inn_customer (first_name, last_name, email, phone_number) VALUES 
('Michael', 'Johnson', 'michaeljohnson@email.com', 9876543210),
('Emily', 'Taylor', 'emilytaylor@email.com', 9876543211),
('Daniel', 'Williams', 'danielwilliams@email.com', 9876543212),
('Olivia', 'Davis', 'oliviadavis@email.com', 9876543214),
('Liam', 'Brown', 'liambrown@email.com', 9876543215),
('Ava', 'Miller', 'avamiller@email.com', 9876543216),
('Sophie', 'Smith', 'sophiesmith@email.com', 9876543217),
('Benjamin', 'Moore', 'benjaminmoore@email.com', 9876543218),
('Grace', 'Wilson', 'gracewilson@email.com', 9876543213);

INSERT INTO inn_reservation (room_type, customer_id, accommodation_days, cost, checkout) VALUES 
(1, 1, 3, 350.00, 1),
(2, 2, 4, 400.00, 1),
(3, 3, 2, 350.00, 0),
(4, 4, 1, 120.00, 0),
(5, 5, 4, 440.00, 0),
(6, 6, 1, 740.00, 0),
(7, 7, 1, 120.00, 1),
(8, 8, 1, 200.00, 1),
(9, 9, 1, 400.00, 1);

SELECT r.id, c.first_name, c.last_name, r.accommodation_days, r.cost
        FROM inn_reservation r
        JOIN inn_customer c ON r.customer_id = c.id
        WHERE c.phone_number = '9876543210' AND r.checkout = 0


