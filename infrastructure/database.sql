CREATE SCHEMA IF NOT EXISTS task_flow;
USE task_flow;



CREATE TABLE CustomerStatus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enumerator VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Inserir valores de status
INSERT INTO CustomerStatus (enumerator) VALUES
    ('active'),
    ('inactive'),
    ('suspended');


CREATE TABLE Customer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_key VARCHAR(36) NOT NULL,
    name VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    status_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_customer_status_id FOREIGN KEY (status_id) REFERENCES CustomerStatus(id)
);

CREATE TABLE ProjectStatus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enumerator VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Inserir valores de status
INSERT INTO ProjectStatus (enumerator) VALUES
    ('open'),
    ('closed');


CREATE TABLE Project (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_key VARCHAR(36) NOT NULL,
    customer_id INT NOT NULL,
    status_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    due_date DATE,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_customer_id FOREIGN KEY (customer_id) REFERENCES Customer(id) ON DELETE CASCADE,
    CONSTRAINT fk_project_status_id FOREIGN KEY (status_id) REFERENCES ProjectStatus(id)
);


CREATE TABLE ActivityStatus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enumerator VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Inserir valores de status
INSERT INTO ActivityStatus (enumerator) VALUES
    ('not_started'),
    ('in_progress'),
    ('completed'),
    ('blocked');


CREATE TABLE Activity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    activity_key VARCHAR(36) NOT NULL,
    project_id INT NOT NULL,
    status_id INT NOT NULL,
    description TEXT NOT NULL,
    due_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_project_id FOREIGN KEY (project_id) REFERENCES Project(id) ON DELETE CASCADE,
    CONSTRAINT fk_activity_status_id FOREIGN KEY (status_id) REFERENCES ActivityStatus(id)
);
