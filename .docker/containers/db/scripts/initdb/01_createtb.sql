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

CREATE TABLE teacher_schedules(
  teacher_id varchar(6) NOT NULL,
  slot_datetime timestamp NOT NULL,
  opened_datetime timestamp NOT NULL,
  primary key(teacher_id, slot_datetime)
);
