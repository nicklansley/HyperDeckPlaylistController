import json


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
                json_data = json_file.readlines()
                self.db_data = json.loads(json_data[0])
        except FileNotFoundError:
            print("New playlist backup file will be created")
            self.db_data["playList"].append({"playListId": 1, "playListName": "My Playlist"})
            self._save_db()

    def _save_db(self):
        try:
            with open("hdpc.json", "w", encoding="utf-8") as json_file:
                json_data = json.dumps(self.db_data)
                json_file.write(json_data)
                print("DB saved")
        except Exception as e:
            raise self.DataClipException("Error saving JSON DB: " + e)

    def get_clips_list(self, play_list_id):
        try:
            clip_list = self.db_data["clipList"]
            filtered_clip_list = []
            for clip in clip_list:
                if clip["playListId"] == play_list_id:
                    filtered_clip_list.append(clip)

            return filtered_clip_list

        except Exception as e:
            raise self.DataClipException("Database exception: " + e)

    def get_play_lists(self):
        try:
            return self.db_data["playList"]
        except Exception as e:
            raise self.DataClipException("Database exception: " + e)

    def insert_clip(self, play_list_id, clip):
        try:
            max_running_order = 0
            for clip in self.db_data['clipList']:
                if clip['runningOrder'] > max_running_order:
                    max_running_order = clip['runningOrder']

            clip["runningOrder"] = max_running_order + 1
            clip['playListId'] = play_list_id
            clip['clipId'] = len(self.db_data['clipList']) + 1

            self.db_data['clipList'].append(clip)

            # Save this change:
            self._save_db()

            return True
        except Exception as e:
            raise self.DataClipException("Database exception: " + e)

    def delete_clip(self, clip_id):
        try:
            new_clip_list = []
            for clip in self.db_data['clipList']:
                if clip['clipId'] != clip_id:
                    new_clip_list.append(clip)
            self.db_data['clipList'] = new_clip_list

            # Save this change:
            self._save_db()

        except Exception as e:
            raise self.DataClipException("Database exception: " + e)

    def insert_playlist(self, play_list_name):
        try:
            if len(self.db_data['playList']) == 0:
                play_list_id = 1
            else:
                max_play_list_id = 0
                for play_list in self.db_data['playList']:
                    if play_list['playListId'] > max_play_list_id:
                        max_play_list_id = play_list['playListId']
                play_list_id = max_play_list_id + 1

            self.db_data['playList'].append({"playListId": play_list_id, "playListName": play_list_name})

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

            ## Discover current_running_order_position of clip we want to move:
            for clip in self.db_data['clipList']:
                if clip_id == clip['clipId']:
                    current_running_order_position = clip['runningOrder']
                    break

            # Calculate the new_running_order_position of our clip.
            if move_up_flag:
                new_running_order_position = current_running_order_position - 1
            else:
                new_running_order_position = current_running_order_position + 1

            # Which clip is in the new_running_order_position currently?:
            for cliplist_index in range(len(self.db_data['clipList'])):
                if new_running_order_position == self.db_data['clipList'][cliplist_index]['runningOrder']:
                    # Let's give this clip the current_running_order_position
                    self.db_data['clipList'][cliplist_index]['runningOrder'] = current_running_order_position
                    break

            # Now let's give our own clip the new_running_order_position
            for cliplist_index in range(len(self.db_data['clipList'])):
                if clip_id == clip['clipId']:
                    self.db_data['clipList'][cliplist_index]['runningOrder'] = new_running_order_position
                    break

            # Save all this change:
            self._save_db()

            return True

        except Exception as e:
            raise self.DataClipException("Database exception: " + e)

