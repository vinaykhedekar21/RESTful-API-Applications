select (select p.timestamp from 
posts p, threads t WHERE
t.thread_id = p.thread_id
and t.forum_id = 1 order by p.id desc) as timestamp, 
(select u.username from 
posts p, threads t, users u WHERE
t.thread_id = p.thread_id
and t.forum_id = 1 
and p.user_id = u.user_id order by p.id asc) as creator, 
t.title from threads t