"""Defines all the functions related to the database"""
from xmlrpc.client import boolean
from app import db
from datetime import datetime

def fetch_todo() -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("SELECT * from Posts ORDER BY PostId DESC;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "PostId": result[0],    
            "PostContent": result[3],   
            "UserName": result[1],  
            "PostDate": result[2],
        }
        todo_list.append(item)

    return todo_list


def fetch_drink_searches() -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("SELECT * FROM searchDrink;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "CoffeeName": result[0],
            "Calories": result[1],
            "CategoryName": result[2],
            "UserCount": result[3]
        }
        todo_list.append(item)

    return todo_list

def fetch_beans() -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("SELECT * FROM Beans;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "BeanId": result[0],
            "FarmName": result[1],
            "Species": result[13],
            "Color": result[12]
        }
        todo_list.append(item)

    return todo_list

def fetch_bean_stats(bean_id: int) -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("SELECT * FROM Beans WHERE BeanId={};".format(bean_id)).fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "Aroma": result[2],
            "Flavor": result[3],
            "Aftertaste": result[4],
            "Acidity": result[5],
            "Body": result[6],
            "Balance": result[7],
            "Uniformity": result[8],
            "CleanCup": result[9],
            "Sweetness": result[10],
            "Moisture": result[11]
        }
        todo_list.append(item)

    return todo_list

def fetch_bean_farm(bean_id: int) -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query = ''' 
        SELECT FarmName, Owner, CountryofOrigin, Company, Altitude, Region
        FROM Farm 
        WHERE FarmName IN (
            SELECT FarmName
            FROM Beans
            WHERE BeanId={});
    '''.format(bean_id)
    query_results = conn.execute(query).fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "FarmName": result[0],
            "Owner": result[1],
            "CountryofOrigin": result[2],
            "Company": result[3],
            "Altitude": result[4],
            "Region": result[5]
        }
        todo_list.append(item)

    return todo_list

def search_drink(name: str) -> dict:
    conn = db.connect()
    query1 = "DROP TABLE IF EXISTS searchDrink;"
    query2 = ''' 
        CREATE TABLE searchDrink AS 
        SELECT CoffeeName, Calories, CategoryName, COUNT(UserName) AS UserCount
        FROM FavoriteCoffee NATURAL JOIN (
            SELECT *
            FROM CoffeeDrink
        ) AS C
        GROUP BY CoffeeName
        HAVING LOWER(CoffeeName) LIKE '%%{}%%'
        ORDER BY UserCount DESC
        LIMIT 15;
    '''.format(name.lower())

    conn.execute(query1)
    conn.execute(query2)
    conn.close()

    return 

def search_category(category: str) -> dict:
    conn = db.connect()
    query = ''' 
        SELECT Recipe, CupSize
        FROM CoffeeCategory 
        WHERE categoryName='{}'
    '''.format(category)

    query_result = conn.execute(query).fetchall()
    conn.close()

    todo_list = []
    for result in query_result:
        item = {
            "Ratio": result[0],
            "CupSize": result[1],
        }
        todo_list.append(item)

    return todo_list

def search_category_drink(category: str) -> dict:
    conn = db.connect()
    query = ''' 
        SELECT CoffeeName
        FROM CoffeeDrink
        WHERE CategoryName='{}'
    '''.format(category)

    query_result = conn.execute(query).fetchall()
    conn.close()

    todo_list = []
    for result in query_result:
        item = {
            "CoffeeName": result[0],
        }
        todo_list.append(item)

    return todo_list

def recommandDrink(category: str) -> dict:
    conn = db.connect()
    query = ''' 
        CALL suggestDrink('{}')
    ''' .format(category)

    query_result = conn.execute(query).fetchall()
    conn.close()

    todo_list = []
    for result in query_result:
        item = {
            "CoffeeName": result[0],
            "Tag": result[1],
            "UserCount": result[2]
        }
        todo_list.append(item)

    return todo_list

def update_task_entry(PostId: int, text: str) -> None:
    """Updates task description based on given 'task_id'

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """

    conn = db.connect()
    query = query = 'UPDATE Posts SET PostContent = "{}" WHERE PostId = {};'.format(text, PostId)
    conn.execute(query)
    conn.close()

def update_post_entry(PostId: int, text: str, username) -> None:
    """Updates post content based on given 'postid' and 'username'
    Returns:
        None
    """
    conn = db.connect()
    query = 'UPDATE Posts SET PostContent = "{}", UserName = "{}" WHERE PostId = {};'.format(text, username, PostId)
    result = conn.execute(query)
    affectedrow = result.rowcount
    conn.close()
    if affectedrow == 0:
        return False
    else:
        return True

def remove_drink(username: str, CoffeeName: str) -> None:
    """Deletes drink based on 'CoffeeName' for admin only

    Args: 
        username (str): must be 'admin'
        CoffeeName (str): Targeted CoffeeName

    Returns:
        None
    """
    if username == 'admin':
        conn = db.connect()
        query = """
            DELETE FROM CoffeeDrink
            WHERE CoffeeName = "{}";
        """.format(CoffeeName)
        result = conn.execute(query)
        conn.close()
        return True
    else:
        return False

def update_drink_entry(username: str, CoffeeName: str, Calories: int) -> None:
    """Updates drink fact based on 'CoffeeName' for admin only

    Args: 
        username (str): must be 'admin'
        CoffeeName (str): Targeted CoffeeName
        Calories ():

    Returns:
        None
    """
    if username == 'admin':
        conn = db.connect()
        query = """
            UPDATE CoffeeDrink
            SET Calories = {}
            WHERE CoffeeName = "{}";
        """.format(Calories, CoffeeName)
        result = conn.execute(query)
        conn.close()
        return True
    else:
        return False

def like_drink(username: str, CoffeeName: str) -> None:
    """Updates Table FavoriteCoffee based on 'UserName' and 'CoffeeName'

    Args:
        username (str): Current User
        CoffeeName (str): Targeted CoffeeName

    Returns:
        None
    """
    conn = db.connect()
    query = """
        INSERT INTO FavoriteCoffee (UserName, CoffeeName)
        VALUES ("{}", "{}")
    """.format(username, CoffeeName)
    result = conn.execute(query)
    conn.close()

def unlike_drink(username: str, CoffeeName: str) -> None:
    """Updates Table FavoriteCoffee based on 'UserName' and 'CoffeeName'

    Args:
        username (str): Current User
        CoffeeName (str): Targeted CoffeeName

    Returns:
        None
    """
    conn = db.connect()
    query = """
        DELETE FROM FavoriteCoffee
        WHERE UserName = "{}" AND CoffeeName = "{}"
    """.format(username, CoffeeName)
    result = conn.execute(query)
    conn.close()

def update_status_entry(task_id: int, text: str) -> None:
    """Updates task status based on given 'task_id'

    Args:
        task_id (int): Targeted task_id
        text (str): Updated status

    Returns:
        None
    """

    conn = db.connect()
    query = 'UPDATE tasks SET status = "{}" WHERE id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def insert_new_task(text: str, username: str) -> int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """
    conn = db.connect()
    now  = datetime.now()   
    date = now.strftime('%Y-%m-%d') 
    query = 'INSERT INTO Posts (PostDate, PostContent, UserName) VALUES ("{}","{}","{}");' .format(  
    date,text,username)
    conn.execute(query)
    query_results = conn.execute("SELECT LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_task_by_id(task_id: int, username: str) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    if username == 'admin':
        query = 'DELETE FROM Posts WHERE PostId = {};'.format(task_id)
    else:
        query = 'DELETE FROM Posts WHERE PostId = {} AND UserName="{}";'.format(task_id, username)
    result = conn.execute(query)
    affectedrow = result.rowcount
    conn.close()
    if affectedrow == 0:
        return False
    else:
        return True


def fetch_drinks(username: str, search={"top":15}) -> list:
    """Reads all drinks listed in the CoffeeDrink table

    Args:
        username (str): current UserName
        search (dict): search conditions

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    clause_keyword = ""
    clause_calories = ""
    clause_select_cat = ""
    if 'keyword' in search.keys():
        clause_keyword = """
            UPPER(C.CoffeeName) LIKE UPPER('%%{}%%')
        """.format(search["keyword"])
    if 'Calories' in search.keys():
        clause_calories = """
            Calories <= {}
        """.format(search["Calories"])
    if 'selected_cat' in search.keys():
        clause_select_cat = """
            CategoryName = "{}"
        """.format(search["selected_cat"])
    clauses = [clause_keyword, clause_calories, clause_select_cat]
    for i in range(len(clauses)):
        if clauses[i] != "":
            clauses[i] = "WHERE "+clauses[i]
            break
    for i in range(i+1, len(clauses)):
        if clauses[i] != "":
            clauses[i] = " AND "+clauses[i]
    clause_keyword, clause_calories, clause_select_cat = clauses

    query = """ 
        SELECT COUNT(UserName) AS UserCount, COUNT(CASE WHEN F.UserName="{}" THEN 1 END) AS Liked,
        C.CoffeeName, Calories, Fat, Carb, Fiber, Protein, Sodium, CategoryName
        FROM FavoriteCoffee F RIGHT JOIN CoffeeDrink C
        ON F.CoffeeName = C.CoffeeName
        {}
        {}
        {}
        GROUP BY C.CoffeeName
        ORDER BY UserCount DESC, C.CoffeeName
        LIMIT {};
    """.format(username, clause_keyword, clause_calories, clause_select_cat, search["top"])
    query_results = conn.execute(query).fetchall()
    conn.close()
    conn = db.connect()
    search["MaxCalories"], = conn.execute("""
        SELECT MAX(Calories)
        FROM CoffeeDrink
    """).fetchall()[0]
    conn.close()
    conn = db.connect()
    categories = conn.execute("""
        SELECT CategoryName
        FROM CoffeeCategory
        ORDER BY CategoryName
    """)
    search["categories"] = [res[0] for res in categories]
    conn.close()
    conn = db.connect()
    MaxUserCount = max([i[0] for i in conn.execute(
        """
            SELECT MAX(UserCount)
            FROM (
                SELECT CoffeeName, COUNT(UserName) AS UserCount
                FROM FavoriteCoffee
                GROUP BY CoffeeName
            ) AS R
        """).fetchall()]+[1])
    conn.close()
    drink_list = []
    for result in query_results:
        item = {
            "UserCount": result[0],
            "Liked": result[1],
            "CoffeeName": result[2],
            "Calories": result[3],
            "Fat": result[4],
            "Carb": result[5],
            "Fiber": result[6],
            "Protein": result[7],
            "Sodium": result[8],
            "CategoryName": result[9],
            "MaxUserCount": MaxUserCount
        }
        drink_list.append(item)

    return drink_list, search

def fetch_limits() -> dict:
    """Reads all drinks listed in the CoffeeDrink table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute(
    """ SELECT * FROM calory_limit;
    """
    ).fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "CoffeeName": result[0],
            "Calories": result[1],
            "CategoryName": result[2],
            "UserCount": result[3]
        }
        todo_list.append(item)

    return todo_list


def fetch_drinks_w_calory_limit(calory_limit) -> dict:
    """Reads all drinks listed in the CoffeeDrink table

    Returns:
        A list of dictionaries
    """
    conn = db.connect()
    conn.execute("DROP TABLE IF EXISTS calory_limit;")
    if calory_limit == '':
        conn.execute(
        '''CREATE TABLE calory_limit AS 
            SELECT CoffeeName, Calories, CategoryName, COUNT(UserName) AS UserCount
            FROM FavoriteCoffee NATURAL JOIN (
                SELECT CoffeeName, Calories, CategoryName
                FROM CoffeeDrink
            ) AS C
            GROUP BY CoffeeName
            ORDER BY UserCount DESC
            LIMIT 15;
        ''')
    else:
        conn.execute(
        """ CREATE TABLE calory_limit AS SELECT CoffeeName, Calories, CategoryName, COUNT(UserName) AS UserCount
            FROM FavoriteCoffee NATURAL JOIN (
                SELECT CoffeeName, Calories, CategoryName
                FROM CoffeeDrink
                WHERE Calories <= {}
            ) AS C
            GROUP BY CoffeeName
            ORDER BY UserCount DESC
            LIMIT 15;
        """.format(calory_limit)
        )
    conn.close()

    return 

def insert_new_drink(text: str) -> int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query = 'INSERT INTO tasks (task, status) VALUES ("{}", "{}");'.format(
        text, "Todo"
    )
    conn.execute(query)
    query_results = conn.execute("SELECT LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id

def userinfo(loginid: str) -> str:
    """get info from login page and check whether record match with database user table.
    Returns: true false
    """
    conn = db.connect()

    query_results = conn.execute(
    ''' 
        SELECT Password FROM Users 
        WHERE UserName = '%s';
    ''' % (loginid)
    ).fetchall()
    conn.close()
    for result in query_results:
        return result


def insert_user(userenter: str, passenter: str):
    """Insert new record into user table
    """

    conn = db.connect()
    query = 'INSERT INTO Users (UserName, Password) VALUES ("{}", "{}");'.format(
        userenter, passenter
    )
    conn.execute(query)
    query_results = conn.execute("SELECT LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    conn.close()
    return

def delete_user(username: str):
    conn = db.connect()
    query = 'DELETE FROM Users WHERE UserName="{}";'.format(username)
    result = conn.execute(query)
    affectedrow = result.rowcount
    conn.close()
    if affectedrow == 0:
        return False
    else:
        return True


def advance_query_post(category: str) -> dict:
    conn = db.connect()
    query = ''' 
        SELECT PostId, UserName, PostDate, PostContent, ViewCount, categoryName 
        FROM Posts 
        NATURAL JOIN categorize
        NATURAL JOIN (
            SELECT COUNT(UserName) as ViewCount, PostId 
            FROM ViewHistory 
            GROUP BY PostId
        ) as T 
        WHERE categoryName='{}' ORDER BY ViewCount DESC, PostDate DESC
        LIMIT 5;
    ''' .format(category)

    query_result = conn.execute(query).fetchall()
    conn.close()

    todo_list = []
    for result in query_result:
        item = {
            "PostId": result[0],
            "PostContent": result[3],
            "Author": result[1],
            "Views": result[4],
            "PostDate": result[2]
        }
        todo_list.append(item)

    return todo_list


def search_posts(data: str) -> dict:
	conn = db.connect()
	query1 = "DROP TABLE IF EXISTS search;"
	query = ''' 
	    SELECT PostId, UserName, PostDate, PostContent, ViewCount, categoryName 
		FROM Posts 
		NATURAL JOIN categorize
		NATURAL JOIN (
		    SELECT COUNT(UserName) as ViewCount, PostId 
		    FROM ViewHistory 
		    GROUP BY PostId
		) as T 
		WHERE LOWER(categoryName) LIKE '%%{}%%' ORDER BY ViewCount DESC, PostDate DESC
		LIMIT 5;
	'''.format(data.lower())
	conn.execute(query1)
	query_result = conn.execute(query).fetchall()
	conn.close()
	todo_list = []
	for result in query_result:
		item = {
			"PostId": result[0],
			"PostContent": result[3],
			"UserName": result[1],
			"PostDate": result[2],
		}
		todo_list.append(item)

	return todo_list
