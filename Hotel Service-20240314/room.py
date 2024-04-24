from nameko.rpc import rpc

import dependencies

class RoomService:

    name = 'room_service'

    database = dependencies.Database()

    @rpc
    def get_all_room_type(self):
        room_types = self.database.get_all_room_type()
        return room_types

    @rpc
    def get_all_room(self):
        rooms = self.database.get_all_room()
        return rooms

    # ambil data room berdasarkan nomor
    @rpc
    def get_room_by_num(self, num):
        room = self.database.get_room_by_num(num)
        return room

    # ambil data detail room berdasarkan nomor
    @rpc
    def get_room_details_by_num(self, num):
        status_code, room_details = self.database.get_room_details_by_num(num)
        return status_code, room_details
    
    # tambah room
    @rpc
    def add_room(self, room_num, room_type):
        status_code, new_room = self.database.add_new_room(room_num,room_type)
        return status_code, new_room
    
    # update status room berdasarkan nomor tertentu
    @rpc
    def up_stat(self, room_num):
        status_code, new_stat = self.database.update_status(room_num)
        return status_code, new_stat

    @rpc
    def up_stat_1(self, room_num, room_stat):
        status_code, new_stat = self.database.update_status_room(room_num,room_stat)
        return status_code, new_stat
    
    # delete room berdasarkan nomor tertentu
    @rpc
    def del_room(self, room_num):
        status_code, del_room = self.database.delete_room(room_num)
        return status_code, del_room
# Method to add a room
# add_room(self, room_num, room_type)

# Method to change a room's status (0 to 1, or vice versa)
# change_room_status(self, room_num)

# Method to delete a room
# delete_room(self, room_num)

# Notes: you may replace room_num with id
