CREATE TABLE submit_messages (
  id serial,
  username text NOT NULL,
  content_of_message text NOT NULL,
  submitted_time timestamp NOT NULL
);
