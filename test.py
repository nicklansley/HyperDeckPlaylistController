from prettytable import PrettyTable
from HyperDeck import HyperDeck
from time import sleep

# Displays a formatted clkip list
def display_clip_list(hyperdeck):
    clip_list = hyperdeck.get_clips_list()
    table = PrettyTable()
    table.field_names = ["Clip ID", "Name", "TimeCode", "Duration"]
    for clip in clip_list:
        table.add_rows([ [ clip['index'], clip['name'], clip['timecode'], clip['duration'] ] ])
    print(table)


# Example function that lists HyperDecks clip list and invited you to choose one to play.
# If you select 0 (bypass) then you are invited to set a from and to timecode from which the
# hyperdeck will then play and loop.
def main():
    hyperdeck = HyperDeck("192.168.0.145", 9993)
    response = hyperdeck.connect()
    print(response)
    if response['response_code'] == 500:
        display_clip_list(hyperdeck)
        chosen_clip_id = input('Choose a clip to play (0 to bypass)  >> ')
        if chosen_clip_id == "0":
            choice_yn = input("Would you like to set a play range using timecodes? > ")
            if choice_yn == "y":
                start_timecode = input ("Enter starting timecode in format 00:00:00:00 > ")
                end_timecode = input ("Enter ending timecode in format 00:00:00:00 > ")
                hyperdeck.stop()
                hyperdeck.set_playrange(start_timecode, end_timecode)
                hyperdeck.play(True)
            else:
                quit()
        else:
            hyperdeck.select_clip_with_index(int(chosen_clip_id) + 1)
    while True:
        print(hyperdeck.get_transport_info())
        sleep(1)


if __name__ == '__main__':
    main()