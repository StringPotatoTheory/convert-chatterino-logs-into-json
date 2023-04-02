import io, sys, json, os, numpy


# change these values to the streamer's name and ID
# find the ID for a streamer here: https://streamscharts.com/tools/convert-username
# or here: https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/

STREAMER_USERNAME = "HasanAbi"
STREAMER_ID = 207813352



if __name__ == "__main__":
    filename = sys.argv[1]
    
    extension = ".json"
    debug_count = 0
    content_id = "000000000"
    channel_id = STREAMER_ID
    id = 1000000
    user_id = 770000
    jsonArray = []
    start = '{"streamer": { "name": "' + STREAMER_USERNAME + '", "id": ' + str(STREAMER_ID) + ' }, "comments":'
    end = '}'

    USER_NOTICE_PARAM_SUB = {"msg-id": "resub"}

    MODERATORS = []
    VIPS = []
    COLORS = []
    COLORS_USERNAMES = []

    def convert_csv_into_array(filename):
        with io.open(filename, 'r', encoding='utf8') as reader:
            word_array = []
            for line in reader:
                words = line.split(',')
                word_array += words
        # removes trailing and leading spaces and newlines, and removes elements if they are empty
        word_array = [x.strip() for x in word_array if x.strip()]
        return word_array
    
    def get_usernames_and_colors(filename):
        usernames = list(numpy.loadtxt(filename, delimiter=",", dtype="str", comments="/", usecols=0))
        colors = list(numpy.loadtxt(filename, delimiter=",", dtype="str", comments="/", usecols=1))

        usernames = [x.strip() for x in usernames]
        colors = [x.strip() for x in colors]

        print(usernames)
        print(colors)

        return usernames, colors
    
    COLORS_USERNAMES, COLORS = get_usernames_and_colors("config/colors.csv")

    MODERATORS = convert_csv_into_array("config/mods.csv")
    VIPS = convert_csv_into_array("config/vips.csv")

    with io.open(filename, 'r', encoding='utf8') as reader:
        for line in reader:
            #debug_count = debug_count + 1
            #print(debug_count)

            splitLine = line.split(' ', 3)
            #print(splitLine)

            user_notice = {}
            user_badges = {}
            
            timestamp = splitLine[0].strip('[]')
            timestampSplit = timestamp.split(':')
            #print(timestampSplit)
            offset_seconds = (int(timestampSplit[0]) * 3600) + (int(timestampSplit[1]) * 60) + int(timestampSplit[2])
            
            datestamp = "2023-01-01T" + timestamp + "Z"
            
            if splitLine[1].rstrip('\n') == "":
                try:
                    name = splitLine[2].rstrip(':')
                    #print("." + name + ".")
                    message = splitLine[3].rstrip('\n')
                    is_action = False
                except: continue # if there happens to be a timestamp and a blank line, ignore it and continue to the next line
            elif splitLine[2] == "subscribed":
                splitSub = line.split(' ', 2)
                name = splitSub[1]
                message = name + " " + splitSub[2].rstrip('\n')
                user_notice = USER_NOTICE_PARAM_SUB

                is_action = False

            the_json = {
                "_id": "c2345678-9012-3456-7890-" + str(id),
                "created_at": datestamp,
                "updated_at": datestamp,
                "channel_id": channel_id,
                "content_type": "video",
                "content_id": content_id,
                "content_offset_seconds": offset_seconds,
                "commenter": {
                    "display_name": name,
                    "_id": "" + str(user_id),
                    "name": name,
                    "type": "user",
                    "bio": "",
                    "created_at": datestamp,
                    "updated_at": datestamp,
                    "logo": ""
                },
                "source": "chat",
                "state": "published",
                "message": {
                    "body": message,
                    "fragments": [
                        {
                            "text": message
                        }
                    ],
                    "is_action": is_action,
                    "user_notice_params": user_notice
                }
            }

            # tries to find the name in the list, if it's not found just continue
            try:
                username_color_index = COLORS_USERNAMES.index(name)
                if username_color_index >= 0:
                    the_json["message"]["user_color"] = COLORS[username_color_index]
            except: continue

            if name.lower() in MODERATORS:
                the_json["message"]["user_badges"] = [{}]
                the_json["message"]["user_badges"][0]["_id"] = "moderator"
                the_json["message"]["user_badges"][0]["version"] = "1"
            elif name.lower() is STREAMER_USERNAME.lower():
                the_json["message"]["user_badges"] = [{}]
                the_json["message"]["user_badges"][0]["_id"] = "broadcaster"
                the_json["message"]["user_badges"][0]["version"] = "1"
            elif name.lower() in VIPS:
                the_json["message"]["user_badges"] = [{}]
                the_json["message"]["user_badges"][0]["_id"] = "vip"
                the_json["message"]["user_badges"][0]["version"] = "1"

            jsonArray.append(the_json)
            
            id += 1
            user_id += 1
    
    try:
        os.remove(filename + extension)
    except: pass
    
    writer = io.open(filename + extension, 'w', encoding='utf8')

    writer.write(start)
    json.dump(jsonArray, writer)
    writer.write(end)
