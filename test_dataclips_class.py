from DataClip import DataClip
dataclip = DataClip()


#dataclip.insert_playlist("My Second PlayList")
playlists = dataclip.get_play_lists()
for playlist in playlists:
    print(playlist)

play_list_id = 2

#new_clip1 = {'hyperDeckClipIndex': 17, 'clipName': 'Sunny days', 'timecode': '11:17:17:17', 'duration': "11:17:10:00" }
#dataclip.insert_clip(play_list_id, new_clip1)
#new_clip2 = {'hyperDeckClipIndex': 23, 'clipName': 'Spring Awakening', 'timecode': '11:23:23:23', 'duration': "11:04:23:00" }
#dataclip.insert_clip(play_list_id, new_clip2)
#new_clip3 = {'hyperDeckClipIndex': 4, 'clipName': 'Autum Hold', 'timecode': '11:04:04:04', 'duration': "11:23:10:44" }
#dataclip.insert_clip(play_list_id, new_clip3)

clips = dataclip.get_clips_list(play_list_id)
for clip in clips:
    print(clip)

dataclip.move_clip_up_or_down_running_order(play_list_id, 2, True)

clips = dataclip.get_clips_list(play_list_id)
for clip in clips:
    print(clip)