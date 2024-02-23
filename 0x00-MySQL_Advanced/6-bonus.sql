-- An SQL script that creates a stored procedure AddBonus that adds a new correction for a student.
DELIMITER //
CREATE PROCEDURE AddBonus(IN userId INT, IN projectName VARCHAR(255), IN scoreProject INT)
BEGIN
	DECLARE projectId INT;
	SET projectId = (SELECT id from projects WHERE name = projectName);
	IF projectId IS NULL THEN
		INSERT INTO projects (name) VALUES (projectName);
		SET projectId = LAST_INSERT_ID();
	END IF;
	INSERT INTO corrections (user_id, project_id, score) VALUES (userId, projectId, scoreProject);
END //
DELIMITER ;
