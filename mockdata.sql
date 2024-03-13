

INSERT INTO polls_users (username, password) VALUES ('batman', 'scrypt:32768:8:1$IadegoiteNBIbqxo$49a7287d1ea396bf8d30743c2ade481ce86be5dc5144912fd4ee7698f9915fd67501d3ba7127ba5c90240d17b5c16627f4b78c4ea1ed467e8a348760cf8bc16c') ON CONFLICT DO NOTHING;
INSERT INTO polls_users (username, password) VALUES ('spiderman', 'scrypt:32768:8:1$IadegoiteNBIbqxo$49a7287d1ea396bf8d30743c2ade481ce86be5dc5144912fd4ee7698f9915fd67501d3ba7127ba5c90240d17b5c16627f4b78c4ea1ed467e8a348760cf8bc16c') ON CONFLICT DO NOTHING;
INSERT INTO polls_users (username, password) VALUES ('ironman', 'scrypt:32768:8:1$IadegoiteNBIbqxo$49a7287d1ea396bf8d30743c2ade481ce86be5dc5144912fd4ee7698f9915fd67501d3ba7127ba5c90240d17b5c16627f4b78c4ea1ed467e8a348760cf8bc16c') ON CONFLICT DO NOTHING;
INSERT INTO polls_users (username, password) VALUES ('superman', 'scrypt:32768:8:1$IadegoiteNBIbqxo$49a7287d1ea396bf8d30743c2ade481ce86be5dc5144912fd4ee7698f9915fd67501d3ba7127ba5c90240d17b5c16627f4b78c4ea1ed467e8a348760cf8bc16c') ON CONFLICT DO NOTHING;
INSERT INTO polls_users (username, password) VALUES ('woman', 'scrypt:32768:8:1$IadegoiteNBIbqxo$49a7287d1ea396bf8d30743c2ade481ce86be5dc5144912fd4ee7698f9915fd67501d3ba7127ba5c90240d17b5c16627f4b78c4ea1ed467e8a348760cf8bc16c') ON CONFLICT DO NOTHING;

INSERT INTO polls_groups(name, creator) VALUES ('Justice League', 1) ON CONFLICT DO NOTHING;
INSERT INTO polls_groups(name, creator) VALUES ('Avengers', 3) ON CONFLICT DO NOTHING;
INSERT INTO polls_groups(name, creator) VALUES ('Nice Guys', 5) ON CONFLICT DO NOTHING;

INSERT INTO polls_group_members(group_id, user_id) 
VALUES 
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (2, 3),
    (2, 4),
    (2, 5),
    (3, 3),
    (3, 4),
    (3, 5)
ON CONFLICT DO NOTHING;

INSERT INTO polls_polls(name, group_id, created_by, created_at, closes_at, description)
VALUES
    ('Who is the best superhero?', 1, 1, NOW() - INTERVAL '1 day', NOW() + INTERVAL '1 day', 'This is a poll to determine who is the best superhero.'),
    ('Who is the worst supervillan?', 1, 2, NOW() - INTERVAL '5 hours', NOW() + INTERVAL '1 day', 'This is a poll to determine who is the best superhero.'),
    ('Night or day?', 2, 3, NOW() - INTERVAL '1 hour', NOW() + INTERVAL '1 hour', 'Do you prefer night or day?'),
    ('What is the best food?', 3, 5, NOW() - INTERVAL '1 minute', NOW() + INTERVAL '1 day', 'This is a poll to determine what is the best food.'),
    ('What should we eat?', 3, 5, NOW(), NOW() + INTERVAL '1 day', 'What should we eat at the hideout today?')
ON CONFLICT DO NOTHING;

INSERT INTO polls_choices(name, poll_id, added_by, added_at,votes)
VALUES
    ('Batman', 1, 1, (NOW() - INTERVAL '5 seconds'),1),
    ('Spiderman', 1, 2, (NOW() - INTERVAL '4 seconds'),1),
    ('Ironman', 1, 3, (NOW() - INTERVAL '3 seconds'),1),
    ('Superman', 1, 4, (NOW() - INTERVAL '2 seconds'),1),
    ('The nazis',2,1, (NOW() - INTERVAL '5 seconds'),0),
    ('The joker',2,1, (NOW() - INTERVAL '4 seconds'),0),
    ('The monster under my bed',2,4, (NOW() - INTERVAL '3 seconds'),0),
    ('The communists',2,3, (NOW() - INTERVAL '2 seconds'),0),
    ('The patriarchy',2,5, NOW(),0),
    ('Night',3,3,(NOW() - INTERVAL '5 seconds'),0),
    ('Day',3,3, NOW(),0),
    ('Pizza',4,5, (NOW() - INTERVAL '5 seconds'),0),
    ('Burgers',4,5, (NOW() - INTERVAL '2 seconds'),0),
    ('Tacos',4,5, NOW(),0),
    ('Pizza',5,5, (NOW() - INTERVAL '5 seconds'),0),
    ('Burgers',5,5, (NOW() - INTERVAL '2 seconds'),0),
    ('Tacos',5,5,NOW(),0)
ON CONFLICT DO NOTHING;

INSERT INTO polls_user_votes(choice_id, user_id)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4)
ON CONFLICT DO NOTHING;