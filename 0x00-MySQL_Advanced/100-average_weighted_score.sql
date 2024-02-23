-- An SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN userId INT)
BEGIN
	DECLARE userScores DECIMAL;
	SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
	INTO userScores
	FROM corrections
	JOIN projects ON corrections.project_id = projects.id
	WHERE corrections.user_id = userId;
	UPDATE users SET average_score = userScores WHERE id = userId;
END //
DELIMITER ;
