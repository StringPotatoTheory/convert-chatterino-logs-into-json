# Convert Chatterino Logs to JSON

Want to render chat as a video but you only have the Chatterino logs and weren't able to download chat in time? This program might help!

Run your Chatterino logs through this program then use [Twitch Downloader](https://github.com/lay295/TwitchDownloader) to render chat into a video.

If the code crashes or doesn't work as expected, please [create an issue](https://github.com/StringPotatoTheory/convert-chatterino-logs-into-json/issues) and include either your Chatterino log file you are trying to convert, or include the line that caused problems and the error message.

## How to Use

### Prerequisites

You will need [python 3](https://www.python.org/downloads/) and the [NumPy package](https://pypi.org/project/numpy/) installed.

### Set Up

1. **Set the streamer's username**: In [main.py](main.py) near the top of the file, set the variable `STREAMER_USERNAME` to the username of the streamer.

### Optional Set Up

1. **Rename the .csv config files**. If you will be using the files in `config/`, remove `example-` from the file names.

2. **Set up the mods and vips files**. If you would like the vips / mods to have their vip / mod badges, add their usernames separated by commas to `config/vips.csv` and `config/mods.csv` respectively. You can use the `/mods` and `/vips` commands in twitch chat and copy paste the results into the .csv files.

3. **Set up chatter colors**. If you have some chatters where you'd like to set their color (by default Twitch Downloader sets colors randomly), add their usernames and colors like this:

```csv
username, #ff00ff
username_2, #00cc00
```

4. **Set the streamer's ID**. In [main.py](main.py) near the top, set the variable `STREAMER_ID`. You can find their ID either from [here](https://streamscharts.com/tools/convert-username) or [here](https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/).

### Versions

If you are wanting to convert Chatterino logs that are from before late 2023 that have the below format, [download v1.0.0 here](https://github.com/StringPotatoTheory/convert-chatterino-logs-into-json/releases/tag/v1.0.0).

- `[12:44:00]  username: message` (with two spaces after the timestamp)
- `[18:51:25] username gifted a Tier 1 sub to username2!` (only one space after the timestamp)

If your logs are from a newer Chatterino version, [download a newer release](https://github.com/StringPotatoTheory/convert-chatterino-logs-into-json/releases) or clone this repo as you would normally.

### Run it

Run it using:

```bash
python main.py <chatterino-log-file>
```

Example:

```bash
python main.py streamer-2024-01-01.log
```

## Contributing

Contributions and suggestions welcome! Either view the [contributing guide](CONTRIBUTING.md) for making a pull request, or feel free to add any suggestions or bugs in the [issue tracker](https://github.com/StringPotatoTheory/convert-chatterino-logs-into-json/issues).

## License

This project is under the [GPLv3 License](LICENSE).
