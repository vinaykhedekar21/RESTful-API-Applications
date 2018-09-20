drop table if exists user;
create table user (
  user_id integer primary key autoincrement,
  username text not null,
  password text not null
);

drop table if exists forum;
create table forum (
  forum_id integer primary key autoincrement,
  name text not null,
  creator text not null
);

drop table if exists thread;
create table thread (
  id integer primary key autoincrement,
  forum_id integer not null,
  title text not null,
  text text not null,
  creator text not null,
  timestamp text not null,
  FOREIGN KEY(forum_id) REFERENCES forum(forum_id)	
);

drop table if exists post;
create table post (
  id integer primary key autoincrement,
  forum_id integer not null,
  thread_id integer not null,
  author text not null,
  text text not null,
  timestamp text not null, --add db timestamp
  FOREIGN KEY(thread_id) REFERENCES thread(thread_id)	
);
