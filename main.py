import io, sys, json, os, numpy, warnings


# change these values to the streamer's name and ID
# find the ID for a streamer here: https://streamscharts.com/tools/convert-username
# or here: https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/

STREAMER_USERNAME = "demonadcL9"
STREAMER_ID = 480960481



if __name__ == "__main__":
    filename = sys.argv[1]
    
    extension = ".json"
    debug_count = 0
    content_id = "000000000"
    channel_id = str(STREAMER_ID)
    id = 1000000
    user_id = 770000
    jsonArray = []
    start = '{"streamer": { "name": "' + STREAMER_USERNAME + '", "id": ' + str(STREAMER_ID) + ' }, "comments":'
    end = ',"embeddedData": null }'

    USER_NOTICE_PARAM_SUB = {"msg-id": "resub"}

    MODERATORS = []
    VIPS = []
    COLORS = []
    COLORS_USERNAMES = []

    def convert_csv_into_array(filename):
        try:
            with io.open(filename, 'r', encoding='utf8') as reader:
                word_array = []
                for line in reader:
                    words = line.split(',')
                    word_array += words

            if not word_array:
                print(filename + " is empty, none of these badges will be added to any messages")

            # removes trailing and leading spaces and newlines, and removes elements if they are empty
            word_array = [x.strip() for x in word_array if x.strip()]
        except FileNotFoundError:
            print(filename + " is not found, none of these badges will be added to any messages")
            word_array = []
            pass
        return word_array
    
    def get_usernames_and_colors(filename):
        try:
            # disables numpy warnings from being displayed in console
            warnings.filterwarnings('ignore')

            usernames = list(numpy.loadtxt(filename, delimiter=",", dtype="str", comments="/", usecols=0, ndmin=1))
            colors = list(numpy.loadtxt(filename, delimiter=",", dtype="str", comments="/", usecols=1, ndmin=1))

            if not usernames:
                print(filename + " is empty, no colors will be set for any usernames")

            usernames = [x.strip() for x in usernames]
            colors = [x.strip() for x in colors]
        except FileNotFoundError:
            print(filename + " is not found, no colors will be set for any usernames")
            usernames = []
            colors = []
            pass

        # print(usernames)
        # print(colors)

        return usernames, colors
    
    COLORS_USERNAMES, COLORS = get_usernames_and_colors("config/colors.csv")

    MODERATORS = convert_csv_into_array("config/mods.csv")
    VIPS = convert_csv_into_array("config/vips.csv")
    
    firstIteration = True
    dayStartCheck = 0
    newday = False

    with io.open(filename, 'r', encoding='utf8') as reader:
        for line in reader:
            #checking if the line is a message
            if line[0] != '[':
                continue

            #debug_count = debug_count + 1
            #print(debug_count)

            splitLine = line.split(' ', 2)
            #print(splitLine)

            if len(splitLine) <= 2:
                continue

            user_notice = {}
            user_badges = {}
            
            timestamp = splitLine[0].strip('[]')
            timestampSplit = timestamp.split(':')
            #print(timestampSplit)
            offset_seconds = (int(timestampSplit[0]) * 3600) + (int(timestampSplit[1]) * 60) + int(timestampSplit[2])
            
            #checking next day (bad implementation prob (only 2 days))
            #>>>offset_seconds compare instead of just hours
            datestamp = ""

            if firstIteration:
                firstIteration = False
                dayStartCheck = timestampSplit[0]

            if timestampSplit[0] < dayStartCheck:
                datestamp = "2023-01-02T" + timestamp + "Z"
                offset_seconds = offset_seconds + (24 * 3600)
            else:
                datestamp = "2023-01-01T" + timestamp + "Z"
            
            name = ""
            message = ""
            
            if splitLine[1][len(splitLine[1]) - 1] == ':':
                name = splitLine[1].rstrip(':')
                message = splitLine[2].rstrip('\n')
                #print("." + name + ".")
                #print("." + message + ".")
            #i don't understand what this supposed to do
            elif splitLine[1].rstrip('\n') == "":
                try:
                    name = splitLine[2].rstrip(':')
                    #print("." + name + ".")
                    message = splitLine[3].rstrip('\n')
                    is_action = False
                except IndexError: continue # if there happens to be a timestamp and a blank line, ignore it and continue to the next line
            elif "subscribed" in splitLine[2]:
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

            jsonArray.append(the_json)
            
            id += 1
            user_id += 1
    
    try:
        os.remove(filename + extension)
    except FileNotFoundError: pass
    
    writer = io.open(filename + extension, 'w', encoding='utf8')

    writer.write(start)
    json.dump(jsonArray, writer)
    writer.write(end)
