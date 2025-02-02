create database vulcanTracker;

show databases;

use vulcanTracker;

create table signup(fname varchar(20), lname varchar(20), username varchar(20), password varchar(20), age varchar(2));

create table login(username varchar(20), password varchar(20));

create table userProfile(username varchar(20), password varchar(20), age varchar(2), miles varchar(9), activites varchar(9));


INSERT into signup (fname, lname, password, age)
VALUES("John", "Gerega", "Ninjago2!", 20);

INSERT into userProfile (username, password, age, miles, activites)
VALUES("jjgerega30", "Ninjago2!", 20, 584, 400);


SELECT * FROM signup;
SELECT * FROM userProfile;
