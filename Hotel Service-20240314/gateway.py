import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http


class GatewayService:
    name = 'gateway'

    hotel_rpc = RpcProxy('room_service')

    @http('GET', '/room')
    def get_rooms(self, request):
        rooms = self.hotel_rpc.get_all_room()
        return json.dumps(rooms)

    # ambil data detail room berdasarkan nomor
    @http('GET', '/room/<int:room_num>')
    def get_room_details(self, request, room_num):
        status_code, room_details = self.hotel_rpc.get_room_details_by_num(room_num)
        return status_code, json.dumps(room_details)
    # get info details of a particular room (identified by room_num)

    # tambah room 
    @http('POST', '/room')
    def add_new_room(self, request):
        data = request.get_data(as_text=True)
        json_data = json.loads(data)
        room_num = json_data.get('room_num')
        room_type = json_data.get('room_type')
        status_code, new_room = self.hotel_rpc.add_room(room_num, room_type)
        return status_code, json.dumps(new_room)
    # create a new room
    # contoh input:
    # {
    #     "room_num": 12345,
    #     "room_type": 1
    # }

    # update status room berdasarkan nomor tertentu
    @http('PUT', '/room/<int:room_num>')
    def update_room(self, request, room_num):
        status_code, new_room = self.hotel_rpc.up_stat(room_num)
        return status_code, json.dumps(new_room)
    
    @http('PUT', '/room/<int:room_num>/<int:room_stat>')
    def update_room_1(self, request, room_num,room_stat):
        status_code, new_room = self.hotel_rpc.up_stat_1(room_num,room_stat)
        return status_code, json.dumps(new_room)
    # toggle the status (0 to 1, or vice versa) of a particular room (identified by room_num)

    # delete room berdasarkan nomor tertentu
    @http('DELETE', '/room/<int:room_num>')
    def del_room(self, request, room_num):
        status_code, del_room = self.hotel_rpc.del_room(room_num)
        return status_code, json.dumps(del_room)
    # delete a particular room (identified by room_num)

