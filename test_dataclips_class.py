from DataClip import DataClip
dataclip = DataClip()
playlists = dataclip.get_play_lists()
print(playlists)
play_list_id = playlists[0]["playListId"]
play_list_name = playlists[0]["playListName"]
print(play_list_id, play_list_name)

clips = dataclip.get_clips_list(play_list_id)
print(clips)

#new_clip = {'clipIndex': 27, 'clipName': 'Nick is hilarious', 'timecode': '00:17:17:17', 'duration': "00:00:10:00" }
#new_clip = {'clipIndex': 23, 'clipName': 'Nick is funny', 'timecode': '00:23:23:23', 'duration': "00:23:10:00" }
new_clip = {'clipIndex': 4, 'clipName': 'Nick is funny', 'timecode': '00:04:04:04', 'duration': "00:23:10:44" }
dataclip.insert_clip(play_list_id, new_clip)

clips = dataclip.get_clips_list(play_list_id)
for clip in clips:
    print(clip)
