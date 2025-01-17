create database vulcanTracker;

show databases;

use vulcanTracker;

create table signup(formno varchar(20), fname varchar(20), lname varchar(20), password varchar(20), age varchar(2));

create table login(username varchar(20), password varchar(20));

create table userProfile(username varchar(20), password varchar(20), age varchar(2), miles varchar(9), activites varchar(9));