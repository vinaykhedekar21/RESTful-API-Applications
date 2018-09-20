INSERT INTO user (user_id, username, password)
VALUES
('1', 'vinay', 'Vinay@21'),
('2', 'samarthamarth', 'Samarth@21'),
('3', 'rani','Rani@21');

INSERT INTO forum (forum_id, name, creator)
VALUES
('1', 'Redis','vinay'),
('2', 'MongoDB','samarth'),
('3', 'AWS','rani');

INSERT INTO thread (id, forum_id, title, text, creator, timestamp)
VALUES
('1', '1','Does anyone know how to start Redis?','I m trying to connect to Redis, but dont know how to start','vinay','Tue, 04 Sep 2018 13:18:43 GMT'),
('2', '2','Does anyone MongoDB?',' I know about MongoDB','samarth','Tue, 04 Sep 2018 14:18:43 GMT'),
('3', '3','Does anyone know AWS?','Yes, Its Amazon Web Services','Rani','Tue, 04 Sep 2018 15:18:43 GMT');

INSERT INTO post (id, forum_id, thread_id, author, text, timestamp)
VALUES 
('1', '1', '1', 'vinay', 'I guess sudo start Redis?', 'Tue, 05 Sep 2018 13:18:43 GMT'),
('2', '2', '2', 'samarth', 'I guess sudo start MongoDB?', 'Tue, 05 Sep 2018 14:18:43 GMT'),
('3', '3', '3', 'Rani', 'I guess sudo start AWS?', 'Tue, 05 Sep 2018 15:18:43 GMT');


