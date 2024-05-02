# DigitalMusicMC
Manage your local music and never listen to another commercial.

The main focus on the project right now is to generate playlists intelligently.


## Project Status
### 2021-06-24
This project is a Python remake of a C# program I made that was never released (but was usable for certain tasks).
- So far this Python remake can:
  - (WIP) (`dmmc/unmangle.py`) unmangle filenames by removing characters not compatible with some operating systems or file systems such as FAT32 for portable devices or drives used by car music players
    - The resulting name should be used as the destination in any copy or move operation when exporting.
  - (`dmmc/generate_playlist.py`) generate playlists (Shuffle using numbers in the filename as per the *Sean's Naming Scheme*--See below--This should improve eventually).
- The PlaylistM3U (in the dmmc module) can load playlists.
- This project has been in the pre-alpha stage since at least 2010 as a C# GUI program that can:
  - Export songs to portable music players.
  - Re-encode music files (if not compatible with chosen format, or if above chosen max bitrate).
  - Fix unicode characters in filenames.
  - Export WinAmp playlists in bulk, making the filenames readable and the paths relative.
  - (and nothing else--no playback etc.)


## Credits
- tsf.svg, tsf-*.* CC0 posted 2014 by [spadassin](https://openclipart.org/user-detail/spadassin) on openclipart.org.
  - See also `tsf license.txt`.
- vintage_radio_drawing_5890254.png CC0 from https://pixy.org/5890254/


## Related Projects
- (Ruby) [OverClocked-ReMix-Downloader](https://github.com/rmondello/OverClocked-ReMix-Downloader)
- (various languages) [github.com/search?q=ocremix](https://github.com/search?q=ocremix)


## Known Issues
- In mencoder mode, cannot convert from mp4 or ogg and possibly some other common types (only supports mencoder native types AND lame)


## Conventions

### Required Data
The data directory contains required data.
- The files in the "handled-by-code" directory are not required.
  - In the "sequences" subdirectory, each file contains a sequence for modified characters such as accented character.
    - The second part is placed after an alphabetical letter in storage but above the letter when displayed.
    - The second part can't be stored alone in a file: As read by Python 3, the sequence counts as 2 characters together but the sequence counts as zero characters if you remove the preceding byte (the alphabetical character).

### Tagging and Naming
(preliminary)
- If a song is an internet single, the Album tag value should be set to "Song Name [internet single]" where "Song Name" is the song name (" [internet single]" is literal).

#### Sean's Naming Scheme
The Sean's Naming Scheme (SNS) is a scheme for adding various metrics to Sean's massive collection by changing the filename. This is the situation because Sean is an archivalist using obscure formats with elusive tagging support, and he doesn't have advanced software or the skills to use it. Whether or not using the filename will be the ongoing method, the plan for supporting the SNS is as follows:
- Derive the meaning of all characters in every filename in [tests/SNS-songs.txt](tests/SNS-songs.txt)

The main advantage is that it is a multi-dimensional (or multi-metric) naming scheme, So you can have:
1. Album, Artist, etc. (common metadata)
2. Category
3. Tag
4. Rating

Combining the data allows shuffling (or generating shuffled playlists) intelligently for huge collections.
- Playing all top-rated songs would be obtrusive, but using a generator string (see generate_playlist.py) such as `11211121113` you can space out the high-rated songs (on a scale of `0-3`).
  - This makes the playlist good for long playback since it is both unobtrusive and breaks up the boredom.
- Adding in other metrics such as tags (such as "party") or category (such as "instrumental") adds multiple metrics, not merely multiple tags. Having both tags and categories as separate metrics enables better results.
  - You don't need cloud AI to have a good selection. You can make your own decisions and this software can help you.


## Planned Features
See [contributing.md](contributing.md).

## Developer Notes
See [contributing.md](contributing.md).
