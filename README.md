# JobShala Recruiting Application

Welcome to JobShala, a powerful recruiting application designed to help you manage job listings, user registrations, and contact form submissions.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Database Tables](#database-tables)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

JobShala is a web-based application that simplifies job listing management, user registration, and contact form submissions. It provides an easy-to-use interface for employers to post job listings and for job seekers to browse available job opportunities.

## Features

- User registration and login system
- Job listing categories and details
- Dynamic job categorization
- Contact form for user inquiries

## Database Tables

### Jobs Table

```sql
CREATE TABLE jobs (
  idjobs INT NOT NULL AUTO_INCREMENT,
  Category VARCHAR(100) NOT NULL,
  Company VARCHAR(100) NOT NULL,
  Title VARCHAR(60) NOT NULL,
  Description VARCHAR(1000) NOT NULL,
  Location VARCHAR(100) DEFAULT NULL,
  Salary VARCHAR(100) DEFAULT NULL,
  DateOfPost DATETIME DEFAULT NULL,
  PRIMARY KEY (idjobs),
  UNIQUE KEY Category_UNIQUE (Category)
);

CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(100) NOT NULL,
  password VARCHAR(100) NOT NULL,
  email VARCHAR(150) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY email_UNIQUE (email)
);

CREATE TABLE contactform (
  idcontactForm INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(100) NOT NULL,
  Email VARCHAR(150) NOT NULL,
  Message VARCHAR(1000) NOT NULL,
  Time DATETIME NOT NULL,
  PRIMARY KEY (idcontactForm)
);


## Installation

To set up and run the JobShala application on your local machine, follow these steps:

1. Clone this repository: git clone https://github.com/yourusername/jobshala.git
2. Navigate to the project directory: cd jobshala
3. Install required dependencies: pip install -r requirements.txt
4. Configure the MySQL database settings in app.py
5. Run the application: python app.py

## Usage
* Access the application at http://localhost:5000
* Register as a user or log in if you already have an account
* Browse job listings, apply for jobs, and explore the features
* Users can submit inquiries using the contact form