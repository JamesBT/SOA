from nameko.extensions import DependencyProvider

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def get_all_room_type(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM room_type"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'name': row['name'],
                'price': row['price'],
                'capacity': row['capacity'],
                'status': row['status']
            })
        cursor.close()
        return result

    def get_all_room(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        sql = "SELECT * FROM room"
        cursor.execute(sql)
        for row in cursor.fetchall():
            result.append({
                'num': row['num'],
                'id_type': row['id_type'],
                'status': row['status']
            })
        cursor.close()
        return result

    def get_room_by_num(self, num):
        cursor = self.connection.cursor(dictionary=True)
        sql = "SELECT * FROM room WHERE num = {}".format((num))
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result
    
    # ambil data detail dari room
    def get_room_details_by_num(self, num):
        cursor = self.connection.cursor(dictionary=True)
        try:
            sql = """
                SELECT *
                FROM room
                INNER JOIN room_type ON room.id_type = room_type.id
                WHERE room.num = {}
            """.format((num))
            cursor.execute(sql)
            result = cursor.fetchone()
            cursor.close()
            if result:
                return 200, result
            else:
                return 404, {
                    "status":"Failed",
                    "detail":f"No room with room number {num}",
                    "code":404
                    }
        except Exception as e:
            return 500, {
                "status":"Failed",
                "detail":f"Failed to get detail of room number {num}",
                "code":500
                }

    # tambah room baru
    def add_new_room(self, room_num, room_type):
        cursor = self.connection.cursor(dictionary=True)
        try:
            # cek apakah sudah ada atau belum
            cursor.execute("SELECT * FROM room WHERE num = %s", (room_num,))
            semua_room = cursor.fetchone()
            if semua_room is not None:
                return 409, {
                    "status":"Failed",
                    "detail":f"Room with number {room_num} already exist",
                    "code":409
                }

            # cek status room type
            cursor.execute("SELECT * FROM room_type WHERE id = %s", (room_type,))
            room_type_info = cursor.fetchone()
            if room_type_info is None:
                return 404, {
                    "status": "Failed",
                    "detail": f"Room type with ID {room_type} not found",
                    "code": 404
                }
            elif room_type_info['status'] == 0:
                return 409, {
                    "status": "Failed",
                    "detail": "Room type is not available",
                    "code": 409
                }
            
            # sql untuk tambah room
            sql = """
                    INSERT INTO room (`num`, `id_type`, `status`) 
                    VALUES (%s, %s, '1')
                """
            cursor.execute(sql, (room_num, room_type))
            self.connection.commit()
            result = cursor.lastrowid 
            result = 200, {
                "status": "Success",
                "detail":"Room added successfully",
                "room number": room_num,
                "room type": room_type
            }
            cursor.close()
            return result
        except Exception as e:
            cursor.close()
            return 500, {
                "status":"Failed",
                "detail": "Failed to add room",
                "code":500
                }

    # update status room
    def update_status(self, room_num):
        cursor = self.connection.cursor(dictionary=True)
        # cek apakah room ada atau tidak
        sql = """
            SELECT *
            FROM room
            WHERE room.num = {}
        """.format((room_num))
        cursor.execute(sql)
        result = cursor.fetchone()
        
        if result is not None:
            # jika ada baru ambil status dan set status baru
            if result.get('status') == 0:
                new_status = 1
            else:
                new_status = 0
            
            cursor.execute("UPDATE `room` SET `status` = %s WHERE `num` = %s", (new_status, room_num))
            self.connection.commit()
            result = 200, {
                "status":"Success",
                "detail":"Room status updated succesfully",
                "room number":room_num,
                "room status":new_status
            }
        else:
            result = 404, {
                "status":"Failed",
                "detail":f"No room with room number {room_num}",
                "code":404
            }

        cursor.close()
        return result
    
    def update_status_room(self, room_num, room_stat):
        if room_stat not in (0,1):
            return 409, {
                "status":"Failed",
                "detail":"Invalid room status",
                "code":409
            }
        cursor = self.connection.cursor(dictionary=True)
        # cek apakah room ada atau tidak
        sql = """
            SELECT *
            FROM room
            WHERE room.num = {}
        """.format((room_num))
        cursor.execute(sql)
        result = cursor.fetchone()
        
        if result is not None:
            # jika ada baru ambil status dan set status baru
            cursor.execute("UPDATE `room` SET `status` = %s WHERE `num` = %s", (room_stat, room_num))
            self.connection.commit()
            result = 200, {
                "status":"Success",
                "detail":"Room status updated succesfully",
                "room number":room_num,
                "room status":room_stat
            }
        else:
            result = 404, {
                "status":"Failed",
                "detail":f"No room with room number {room_num}",
                "code":404
            }

        cursor.close()
        return result
    
    # hapus room
    def delete_room(self, room_num):
        cursor = self.connection.cursor(dictionary=True)
        sql = "DELETE FROM room WHERE num = {}".format((room_num))
        cursor.execute(sql)
        if cursor.rowcount > 0:
            self.connection.commit()
            cursor.close()
            return 200, {
                "status":"Success",
                "detail":f"Succesfully deleted room with number {room_num}"
            }
        else:
            cursor.close()
            return 404, {"status":"Failed",
                    "detail":f"Can't find room number: {room_num}",
                    "code":404
                    }
        
    def __del__(self):
        self.connection.close()


class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=10,
                pool_reset_session=True,
                host='localhost',
                database='hotel',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)

    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
