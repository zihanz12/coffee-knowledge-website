DELIMITER //

CREATE TRIGGER PostTrig
    BEFORE UPDATE ON Posts
    FOR EACH ROW
    BEGIN
        IF new.UserName = 'admin' THEN
            SET new.UserName = old.UserName;
        ELSEIF new.UserName = old.UserName THEN
            SET new.PostContent = new.PostContent;
            SET new.UserName = new.UserName;
        ELSE
            SET new.PostContent = old.PostContent;
            SET new.UserName = old.UserName;
        END IF;
    END //

DELIMITER ;
