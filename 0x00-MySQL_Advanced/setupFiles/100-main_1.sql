-- 2 projects of weight 1
SELECT * FROM users;
SELECT * FROM projects;
SELECT * FROM corrections;

CALL ComputeAverageWeightedScoreForUser((SELECT id FROM users WHERE name = "User 1"));

SELECT "--";
SELECT * FROM users;
