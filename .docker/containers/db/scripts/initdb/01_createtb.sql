CREATE TABLE submit_messages (
  id serial,
  username text NOT NULL,
  content_of_message text NOT NULL,
  submitted_time timestamp NOT NULL
);

CREATE TABLE teachers(
  id varchar(6) NOT NULL primary key,
  name varchar(30) NOT NULL,
  country varchar(40) NOT NULL
);

CREATE TABLE teacher_events(
  teacher_id varchar(6) NOT NULL,
  slot_id integer NOT NULL,
  event_id integer NOT NULL,
  happend_on date NOT NULL
);

CREATE TABLE events(
  id serial,
  name text NOT NULL
);

CREATE TABLE slots(
  id serial,
  time text NOT NULL
);
