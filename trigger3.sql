DELIMITER //

create trigger PostUpdateTrig
    after update on Posts
    for each row
    begin
        insert into postlog(id,operation,operate_time,operate_id,operate_params) values(null,'update',now(),new.PostId, concat('before update(content:',old.PostContent,')', 'after update(content:',new.PostContent,')'));
    end //

DELIMITER ;