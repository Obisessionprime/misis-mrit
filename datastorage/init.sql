CREATE DATABASE mrit;

\connect mrit;

CREATE SCHEMA ansible_runner;

CREATE TABLE ansible_runner.ssh_keys (
    ssh_key_id SERIAL,
    private_key varchar,
    public_key varchar,
    username varchar,

    CONSTRAINT ssh_keys_pk PRIMARY KEY (ssh_key_id)
);

CREATE TABLE ansible_runner.task_state (
    state_id SERIAL,
    state_name VARCHAR(256),

    CONSTRAINT task_state_pk PRIMARY KEY (state_id)
);

CREATE TABLE ansible_runner.tasks (
	task_id SERIAL,
	task_initiator_username varchar(256) NOT NULL,
	task_runstart timestamp NOT NULL,
	state_id int,

	CONSTRAINT files_pk PRIMARY KEY (task_id),
	CONSTRAINT state_fk FOREIGN KEY(state_id) REFERENCES ansible_runner.task_state(state_id)
);
