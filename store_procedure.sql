DELIMITER //
CREATE PROCEDURE suggestDrink(IN category VARCHAR(255))
    BEGIN
        DECLARE currName VARCHAR(255);
        DECLARE currCategory VARCHAR(255);
        DECLARE currCalories REAL;
        DECLARE currAvg REAL;
        DECLARE currTag VARCHAR(255);

        DECLARE done BOOLEAN default False;
        DECLARE cur CURSOR FOR (SELECT CoffeeName, Calories, CategoryName, avgCalories
                                FROM CoffeeDrink NATURAL JOIN (
                                    SELECT CategoryName, ROUND(AVG(Calories), 2) AS avgCalories
                                    FROM CoffeeDrink
                                    GROUP BY CategoryName
                                ) AS avgfact);

        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = True;

        DROP TABLE IF EXISTS healthyDrink;

        CREATE TABLE healthyDrink(
            CoffeeName VARCHAR(255),
            CategoryName VARCHAR(255),
            Calories REAL,
            avgCalories REAL,
            Tag VARCHAR(255)
        );

        OPEN cur;

        REPEAT
            FETCH cur INTO currName, currCalories, currCategory, currAvg;
            IF currCalories < currAvg THEN
                SET currTag = 'low calories';
            ELSE
                set currTag = 'high calories';
            END IF;
            INSERT INTO healthyDrink VALUES (currName, currCategory, currCalories, currAvg, currTag);
        UNTIL done
        END REPEAT;

        CLOSE cur;

        SELECT CoffeeName, Tag, UserCount, Calories, avgCalories
        FROM healthyDrink NATURAL JOIN (
            SELECT CoffeeName, COUNT(UserName) AS UserCount
            FROM FavoriteCoffee NATURAL JOIN CoffeeDrink
            WHERE CategoryName = category
            GROUP BY CoffeeName
        ) AS fav
        ORDER BY UserCount DESC;

    END //

DELIMITER ;

