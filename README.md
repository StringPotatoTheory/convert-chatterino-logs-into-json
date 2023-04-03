# Convert Chatterino Logs to JSON

Want to render chat as a video but you only have the chatterino logs and weren't able to download chat in time? This program might help!

Run your Chatterino logs through this program then use [Twitch Downloader](https://github.com/lay295/TwitchDownloader) to render chat into a video.

If the code crashes or doesn't work as expected, please create an issue and include either your chatterino log file you are trying to convert or include the line that caused problems.

**NOTE** If you get the following error while using Twitch Downloader v1.52.2: `ERROR: Value cannot be null. (Parameter 'source')` wait until the next version is released, or use [this build](https://github.com/lay295/TwitchDownloader/actions/runs/4580082135).

## How to Use

### Prerequisites

You need python 3 and the `NumPy` python library installed.

### Set Up

1. **Rename the .csv config files**. If you will be using the files in `config/`, remove `example-` from the file names.

2. **Set up the mods and vips file (optional)**. If you would like the vips / mods to have their vip / mod badges, add their usernames separated by commas to `config/vips.csv` and `config/mods.csv` respectively. You can use the `/mods` and `/vips` commands in twitch chat and copy paste the results into the .csv files.

3. **Set up chat colors (optional)**. If you have some chatters where you'd like to set their color (by default Twitch Downloader sets colors randomly), add their usernames and colors like this:

```csv
username, #ff00ff
username_2, #00cc00
```

4. **Set the streamer's username and ID (the ID is optional, but I recommend setting the username)**. In [main.py](main.py) near the top, set the variables `STREAMER_USERNAME` and `STREAMER_ID`. You can find their ID either from [here](https://streamscharts.com/tools/convert-username) or [here](https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/).

### Run it

Run it using:

```cmd
python main.py <chatterino log file>
```
