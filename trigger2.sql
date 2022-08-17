DELIMITER //

CREATE TRIGGER PostInsertTrig
    AFTER insert ON Posts
    FOR EACH ROW
    BEGIN
        insert into postlog(id,operation,operate_time,operate_id,operate_params) values (null,'insert',now(),new.PostId,concat('after insert(id:',new.PostId,',  username:',new.UserName,')'));
    END //

DELIMITER ;
