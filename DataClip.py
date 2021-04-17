import json
from operator import itemgetter


class DataClip:
    def __init__(self):
        self.db_data = {"playList": [], "clipList": []}
        self._initialise_db()

    class DataClipException(Exception):
        def __init__(self, message):
            self.message = message

    def _initialise_db(self):
        try:
            with open("hdpc.json", "r", encoding="utf-8") as json_file:
                json_data_array = json_file.readlines()
                json_data = ""
                for json_data_line in json_data_array:
                    json_data += json_data_line
                self.db_data = json.loads(json_data)

        except FileNotFoundError:
            print("New playlist backup file will be created")
            self.db_data["playList"].append({"playListId": 1, "playListName": "My Playlist"})
            self._save_db()

    def _save_db(self):
        try:
            with open("hdpc.json", "w", encoding="utf-8") as json_file:
                json_data = json.dumps(self.db_data, indent=4, sort_keys=True)
                json_file.write(json_data)
                print("DB saved")
        except Exception as e:
            raise self.DataClipException("Error saving JSON DB: " + e)

    def get_clips_list(self, play_list_id):
        try:
            clip_list = self.db_data["clipList"]
            filtered_clip_list = []

            # We must get just the clips with the requested play_list_is
            for clip in clip_list:
                if clip["playListId"] == play_list_id:
                    filtered_clip_list.append(clip)

            # Now sort by runningOrder and return
            return sorted(filtered_clip_list, key=itemgetter('runningOrder'))

        except Exception as e:
            raise self.DataClipException("Database exception: " + e)

    def get_play_lists(self):
        try:
            return sorted(self.db_data["playList"], key=itemgetter('playListName'))
        except Exception as e:
            raise self.DataClipException("Database exception: " + e)

    def insert_clip(self, play_list_id, new_clip):
        try:
            # Find the highest running_order value and add 1 to its value
            # to assign to the new clip (which is going to the 'bottom' of the play list.
            max_running_order = 0
            for play_list_clip in self.db_data['clipList']:
                if play_list_clip['playListId'] == play_list_id and play_list_clip['runningOrder'] > max_running_order:
                    max_running_order = play_list_clip['runningOrder']

            # Assign the new running order and the playlist to which this clip is to belong:
            new_clip["runningOrder"] = max_running_order + 1
            new_clip['playListId'] = play_list_id
            new_clip['clipId'] = len(self.db_data['clipList']) + 1

            # Add the new clip to the list:
            self.db_data['clipList'].append(new_clip)

            # Save this change:
            self._save_db()

            return True
        except Exception as e:
            raise self.DataClipException("Database exception: " + e)

    def delete_clip(self, play_list_id, clip_id):
        try:
            new_clip_list = []
            for clip in self.db_data['clipList']:
                if clip['playListId'] != play_list_id and clip['clipId'] != clip_id:
                    new_clip_list.append(clip)
            self.db_data['clipList'] = new_clip_list

            # Save this change:
            self._save_db()

        except Exception as e:
            raise self.DataClipException("Database exception: " + e)

    def insert_playlist(self, new_play_list_name):
        try:
            if len(self.db_data['playList']) == 0:
                play_list_id = 1
            else:
                # Find the highest existing play_list_id:
                max_play_list_id = 0
                for play_list in self.db_data['playList']:
                    if play_list['playListId'] > max_play_list_id:
                        max_play_list_id = play_list['playListId']

                # Add 1 to create the new play_list_id value:
                play_list_id = max_play_list_id + 1

            # Add the playlist to the list:
            self.db_data['playList'].append({"playListId": play_list_id, "playListName": new_play_list_name})

            # Save this change:
            self._save_db()

            return True

        except Exception as e:
            raise self.DataClipException("Database exception: " + e)

    def delete_playlist(self, play_list_id):
        try:
            new_play_list = []
            for play_list in self.db_data['playList']:
                if play_list['playListId'] != play_list_id:
                    new_play_list.append(play_list)
            self.db_data['playList'] = new_play_list

            # Save this change:
            self._save_db()

            return True

        except Exception as e:
            raise self.DataClipException("Database exception: " + e)

    # move_clip_up_running_order finds where the requested clip is currently in the
    # playlist's running order, and moves it up/down one position depending on moveUpFlag
    def move_clip_up_or_down_running_order(self, play_list_id, clip_id, move_up_flag):
        try:

            current_running_order_position = 1
            clip_id_in_wanted_position = 0

            # Discover current_running_order_position of clip we want to move:
            for clip in self.db_data['clipList']:
                if play_list_id == clip['playListId'] and clip_id == clip['clipId']:
                    current_running_order_position = clip['runningOrder']
                    break

            # Calculate the new_running_order_position of our clip.
            if move_up_flag:
                new_running_order_position = current_running_order_position - 1
            else:
                new_running_order_position = current_running_order_position + 1

            # Which clip is in the new_running_order_position currently?:
            for cliplist_index in range(len(self.db_data['clipList'])):
                if play_list_id == clip['playListId'] and new_running_order_position == self.db_data['clipList'][cliplist_index]['runningOrder']:
                    # Let's give this clip the current_running_order_position
                    self.db_data['clipList'][cliplist_index]['runningOrder'] = current_running_order_position
                    break

            # Now let's give our own clip the new_running_order_position
            for cliplist_index in range(len(self.db_data['clipList'])):
                if play_list_id == self.db_data['clipList'][cliplist_index]['playListId'] and clip_id == self.db_data['clipList'][cliplist_index]['clipId']:
                    self.db_data['clipList'][cliplist_index]['runningOrder'] = new_running_order_position
                    break

            # Save all this change:
            self._save_db()

            return True

        except Exception as e:
            raise self.DataClipException("Database exception: " + e)

