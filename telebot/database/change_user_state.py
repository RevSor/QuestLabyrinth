import os
import psycopg2


def get_user_state(user_id:int)->(int,int,int):
    """User chose direction of move. This function get an old state for user."""
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        conn.set_isolation_level(0)
        conn.autocommit = True
        cur = conn.cursor()        
    except:
        print("Unable to connect to the database.")   
    if cur:    
        try:
            cur.execute("""
            SELECT coordinate_x, coordinate_y, current_direction, time_before_attack
            FROM user_state
            WHERE user_id = %s;
            """, (user_id, ))
            record = cur.fetchone()
            coordinate_x = record[0]
            coordinate_y = record[1]
            current_direction = record[2]          
            time_before_attack = record[3]            
        except:
            print("Can\'t to execute get_user_state query") 
        cur.close()
        conn.close()
    return coordinate_x, coordinate_y, current_direction, time_before_attack


def update_state(user_id:int, delta_x:int, delta_y:int, 
                 coordinate_x: int, coordinate_y:int, 
                 current_direction: str, time_before_attack: int,
                 direction: str) -> (int, int):
    """User chose direction of move. This function change user state coordinates and time_before_attack and return new coordinates for getting actions and screenplay."""
    
    time_before_attack -= 1
    
    if time_before_attack == 0:
        coordinate_x_new = -1000
        coordinate_y_new = -1000
    else:
        coordinate_x_new = coordinate_x + delta_x
        coordinate_y_new = coordinate_y + delta_y
    
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        conn.set_isolation_level(0)
        conn.autocommit = True
        cur = conn.cursor()        
    except:
        print("Unable to connect to the database.")   
        
    updated_sucessful = False
    if cur:    
        try:
            cur.execute("""
            UPDATE user_state 
            SET coordinate_x = %s, 
            coordinate_y = %s, 
            current_direction = %s, 
            time_before_attack = %s
            WHERE user_id = %s;
            """, (coordinate_x_new, 
                  coordinate_y_new, 
                  direction,
                  time_before_attack, 
                  user_id))
            updated_sucessful = bool(cur.rowcount)
        except:
            print("Can\'t to execute update_user_state query") 
        cur.close()
        conn.close()
        
    if updated_sucessful:
        return coordinate_x_new, coordinate_y_new
    else:
        return coordinate_x, coordinate_y
