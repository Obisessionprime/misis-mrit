CREATE DATABASE mrit;

\connect mrit;

CREATE SCHEMA ansible_runner;

CREATE TABLE ansible_runner.task (
	task_id int NOT NULL,
	task_initiator_username varchar(256) NOT NULL,
	task_runstart timestamp NOT NULL,
	CONSTRAINT files_pk PRIMARY KEY (task_id)
);
