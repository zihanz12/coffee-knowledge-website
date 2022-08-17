DELIMITER //

create trigger PostDeleteTrig
    after delete on Posts
    for each row
    begin
        insert into postlog(id,operation,operate_time,operate_id,operate_params) values (null,'delete',now(),old.PostId, concat('before delete(id:',old.PostId,',  username:',old.UserName,',  content:',old.PostContent,')'));
    end //

DELIMITER ;