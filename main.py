import io, sys, json, os, numpy, warnings


# change these values to the streamer's name and ID
# find the ID for a streamer here: https://streamscharts.com/tools/convert-username
# or here: https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/

STREAMER_USERNAME = ""
STREAMER_ID = 207813352

DEBUG_MODE = False


def convert_csv_into_array(file_name):
    try:
        with io.open(file_name, 'r', encoding='utf8') as reader:
            word_array = []
            for line in reader:
                words = line.split(',')
                word_array += words

        if not word_array:
            print(file_name + " is empty, none of these badges will be added to any messages")

        # removes trailing and leading spaces and newlines, and removes elements if they are empty
        word_array = [x.strip() for x in word_array if x.strip()]
    except FileNotFoundError:
        print(file_name + " is not found, none of these badges will be added to any messages")
        word_array = []
        pass
    return word_array
    
def get_usernames_and_colors(file_name):
    try:
        # disables numpy warnings from being displayed in console
        warnings.filterwarnings('ignore')

        usernames = list(numpy.loadtxt(file_name, delimiter=",", dtype="str", comments="/", usecols=0, ndmin=1))
        colors = list(numpy.loadtxt(file_name, delimiter=",", dtype="str", comments="/", usecols=1, ndmin=1))

        if not usernames:
            print(file_name + " is empty, no colors will be set for any usernames")

        usernames = [x.strip() for x in usernames]
        colors = [x.strip() for x in colors]
    except FileNotFoundError:
        print(file_name + " is not found, no colors will be set for any usernames")
        usernames = []
        colors = []
        pass

    # print(usernames)
    # print(colors)

    return usernames, colors


if __name__ == "__main__":
    file_name = sys.argv[1]
    
    extension = ".json"
    debug_count = 0
    content_id = "000000000"
    channel_id = str(STREAMER_ID)
    id = 1000000
    user_id = 770000
    json_array = []
    start = '{"streamer": { "name": "' + STREAMER_USERNAME + '", "id": ' + str(STREAMER_ID) + ' }, "comments":'
    end = ',"embeddedData": null }'

    USER_NOTICE_PARAM_SUB = {"msg-id": "resub"}

    MODERATORS = []
    VIPS = []
    COLORS = []
    COLORS_USERNAMES = []
    
    COLORS_USERNAMES, COLORS = get_usernames_and_colors("config/colors.csv")

    MODERATORS = convert_csv_into_array("config/mods.csv")
    VIPS = convert_csv_into_array("config/vips.csv")
    
    first_iteration = True
    day_start_check = 0

    with io.open(file_name, 'r', encoding='utf8') as reader:
        for line in reader:
            # checking if the line starts with a "["" which means a timestamp, the messages
            # we want will all start with one, so skip to the next line if it's not there
            if line[0] != '[':
                continue

            if DEBUG_MODE:
                debug_count = debug_count + 1
                print("lines in loop: " + str(debug_count))

            split_line = line.split(' ', 2)
            if DEBUG_MODE:
                print(split_line)

            if len(split_line) <= 2:
                continue

            user_notice = {}
            user_badges = {}
            
            timestamp = split_line[0].strip('[]') # from "[23::01:24]"" to "23:01:24" 
            timestamp_split = timestamp.split(':') # from "23:01:24" to an array of "23", "01", "24"
            offset_seconds = (int(timestamp_split[0]) * 3600) + (int(timestamp_split[1]) * 60) + int(timestamp_split[2])
            
            #checking next day (bad implementation prob (only 2 days))
            #>>>offset_seconds compare instead of just hours
            datestamp = ""

            if first_iteration:
                first_iteration = False
                day_start_check = timestamp_split[0]

            if timestamp_split[0] < day_start_check:
                datestamp = "2023-01-02T" + timestamp + "Z"
                offset_seconds = offset_seconds + (24 * 3600)
            else:
                datestamp = "2023-01-01T" + timestamp + "Z"
            
            name = ""
            message = ""
            
            if split_line[1][len(split_line[1]) - 1] == ':':
                name = split_line[1].rstrip(':')
                message = split_line[2].rstrip('\n')
                if DEBUG_MODE:
                    print("." + name + ".")
                    print("." + message + ".")
            #i don't understand what this supposed to do
            elif split_line[1].rstrip('\n') == "":
                try:
                    name = split_line[2].rstrip(':')
                    if DEBUG_MODE:
                        print("." + name + ".")
                    message = split_line[3].rstrip('\n')
                    is_action = False
                except IndexError: continue # if there happens to be a timestamp and a blank line, ignore it and continue to the next line
            elif "subscribed" in split_line[2]:
                splitSub = line.split(' ', 2)
                name = splitSub[1]
                message = name + " " + splitSub[2].rstrip('\n')
                user_notice = USER_NOTICE_PARAM_SUB

                is_action = False
            else:
                continue

            the_json = {
                "_id": "c2345678-9012-3456-7890-" + str(id),
                "created_at": datestamp,
                "channel_id": channel_id,
                "content_type": "video",
                "content_id": content_id,
                "content_offset_seconds": offset_seconds,
                "commenter": {
                    "display_name": name,
                    "_id": "" + str(user_id),
                    "name": name,
                    "bio": "",
                    "created_at": datestamp,
                    "updated_at": datestamp,
                    "logo": ""
                },
                "message": {
                    "body": message,
                    "bits_spent": 0,
                    "fragments": [
                        {
                            "text": message,
                            "emoticon": None
                        }
                    ],
                    "emoticons": []
                }
            }

            # tries to find the name in the list, if it's not found just pass this section
            try:
                username_color_index = COLORS_USERNAMES.index(name)
                if username_color_index >= 0:
                    the_json["message"]["user_color"] = COLORS[username_color_index]
            except ValueError: pass

            if name.lower() in MODERATORS:
                the_json["message"]["user_badges"] = [{}]
                the_json["message"]["user_badges"][0]["_id"] = "moderator"
                the_json["message"]["user_badges"][0]["version"] = "1"
            elif name.strip().lower() == STREAMER_USERNAME.strip().lower():
                the_json["message"]["user_badges"] = [{}]
                the_json["message"]["user_badges"][0]["_id"] = "broadcaster"
                the_json["message"]["user_badges"][0]["version"] = "1"
            elif name.lower() in VIPS:
                the_json["message"]["user_badges"] = [{}]
                the_json["message"]["user_badges"][0]["_id"] = "vip"
                the_json["message"]["user_badges"][0]["version"] = "1"

            json_array.append(the_json)
            
            id += 1
            user_id += 1
    
    try:
        os.remove(file_name + extension)
    except FileNotFoundError: pass
    
    writer = io.open(file_name + extension, 'w', encoding='utf8')

    writer.write(start)
    json.dump(json_array, writer, indent=2)
    writer.write(end)
