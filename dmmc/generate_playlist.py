#!/usr/bin/env python3
import os
import codecs
import sys
import random
# Purpose: generate a playlist based on rating
# (the situation below only plays songs rated 1 to 3)
# TODO: store gain in mp3

# generator_string = "111211121113"
generator_string = "11211121113"
music_path = "/mnt/seandata/wav"
folder_path = music_path
p_name = generator_string+".m3u8"
p_file = None
p_path = os.path.join(music_path, p_name)


class GPSong:
    title = None
    artist = None
    form = None
    album = None
    genre = None
    vocal = None
    path = None
    rating = None
    used_count = None
    filename = None

    def __init__(self):
        self.vocal = False
        self.used_count = 0

songs_used_count = 0
songs = list()
error_song_names = list()
looper_indices = dict()
looper_plays_counts = dict()
looper_playable_counts = dict()
looper_unique_songs_played_count = 0
loopable_unique_songs_count = 0

if os.path.isdir(folder_path):
    p_file = open(p_path, 'wb')
    #p_file.write("#EXTM3U"+"\n")
    p_file.write(codecs.BOM_UTF16_LE)
    p_file.write(("#EXTM3U"+"\n").encode('utf-16-le'))
    #UTF8Writer = codecs.getwriter("utf8")
    #sys.stdout = UTF8Writer(sys.stdout)
    print("#EXTM3U")
    for sub_name in os.listdir(folder_path):
        sub_path = os.path.join(folder_path, sub_name)
        if sub_name[:1]!="." and os.path.isfile(sub_path):
            basename=os.path.splitext(sub_name)[0]
            parts=basename.split("-")
            index = 0
            last_number = None
            song = GPSong()
            artist_index = None
            for part in parts:
                if part.lower() == "muzak":
                    artist_index = index
                    song.artist = "Muzak"
                    break
                index += 1
            index = 0
            #if part[0].lower() == "muzak":
            #    song.artist = part[0]

            for part in parts:
                #naming scheme (hyphen in between, whitespace ok but not required)
                #title
                #artist
                #7,10,12 after album is inch size of vinyl, otherwise cd (could also be cd then album name, such as cd 40 for cd named 40 hits)
                # -- could also just contain word such as "tape" in Wwmd tape 29a6 for a station named WWMD and tape named 29a6
                # -- could also be radio, or yt for youtube
                #genre
                #(sometimes a hyphen is missing here)
                # tags could be after album name, such as if I loved you - vocal - party
                #    V for very relaxing
                #song type (vocal, or I or i for instrumental)
                #if says h4 (such as after vocal): named based on "h4 headlights"
                # some more edge cases:
                # And I Love Her-Manny Kellem-LP-love is blue-I-2.ogg
                # Andrea - Bano & Power -tape-sempre-vocal-3.ogg
                # Born to Be Wild - Enoch Light -LP-whoever-vocal-party-3.ogg
                #    where "love is blue" or "sempre" or "whoever" is the name of the collection
                # 4-68-3-Muzak-LP-4-68-I-1
                #    where 4 is stream name, 68 is year (4 68 is album name)
                # Muzak tape 2,1 -I-1
                #    where album is "Muzak tape 2" track is 1, I for Instrumental, rating 1
                # Blue Bayou - Muzak - LP-moe82-I-3
                #    song name - artist - medium - album (muzak of the 80's published 1982) - type (instrumental) - rating
                #              -        -        - could also be nd something (for New Dimensions Volume 2, or first one with no volume #)
                # A Taste of Honey-Muzak-LP-4-68-I-1
                # "have" means stuff was extracted from it, and the rest is elsewhere

                # new naming scheme to suggest: title - medium - album - artist - genre - type - rating - use
                # where type is vocal or I, and last hypen is optional, followed by something like party, or V for very relaxing
                part=part.strip()
                #print(part)
                index += 1



            if len(parts)>0:
                rating_string = parts[len(parts)-1].strip()
                song.path = sub_path
                song.filename = sub_name
                if rating_string=="0":
                    song.rating = 0
                elif rating_string=="1":
                    song.rating = 1
                elif rating_string=="2":
                    song.rating = 2
                elif rating_string=="3":
                    song.rating = 3
                elif rating_string=="4":
                    song.rating = 4
                else:
                    error_song_names.append(sub_name)
                if song.rating is not None:
                    looper_indices[rating_string] = 0
                    looper_plays_counts[rating_string] = 0
                    looper_playable_counts[rating_string] = 0
                    songs.append(song)
            else:
                error_song_names.append(sub_name)

    random.shuffle(songs)
    for song in songs:
        generator_string_index = 0
        if song.rating is not None:
            while generator_string_index<len(generator_string):
                rating_string = generator_string[generator_string_index:generator_string_index+1]
                if str(song.rating)==rating_string:
                    loopable_unique_songs_count+=1
                    #commented since impossible due to loop above
                    #if rating_string not in looper_playable_counts.keys
                    #    looper_playable_counts[rating_string]=0
                    looper_playable_counts[rating_string] += 1
                    break
                generator_string_index+=1
    generator_string_index = 0
    #while (looper_unique_songs_played_count<len(songs)):
    while (looper_unique_songs_played_count<loopable_unique_songs_count):
        rating_string = generator_string[generator_string_index:generator_string_index+1]
        if (looper_playable_counts[rating_string]>0):
            while (str(songs[looper_indices[rating_string]].rating) != rating_string):
                looper_indices[rating_string]+=1
                if looper_indices[rating_string]>=len(songs):
                    looper_indices[rating_string]=0
            #deterministically, looper_indices[rating_string] is now a song with the required rating
            if songs[looper_indices[rating_string]].used_count == 0:
                looper_unique_songs_played_count+=1
            #try:
            p_file.write(("./"+songs[looper_indices[rating_string]].filename+"\n").encode('utf-16-le'))
            looper_plays_counts[rating_string]+=1
            if songs[looper_indices[rating_string]].used_count is None:
                print("used_count is None for rating "+rating_string+" song "+str(looper_indices[rating_string])+" of "+str(len(songs)))
                #print(songs[looper_indices[rating_string]].
                #input("press enter to continue anyway...")
            songs[looper_indices[rating_string]].used_count += 1
            #do the same thing as while loop, since no other way apparently:
            looper_indices[rating_string]+=1
            if looper_indices[rating_string]>=len(songs):
                looper_indices[rating_string]=0
            #print(rating_string)
            #except:
            #    print("Could not finish parsing filename for song "+str(looper_indices[rating_string]))
        generator_string_index+=1
        if (generator_string_index>=len(generator_string)):
            generator_string_index=0
        #else there are no songs with this rating
    p_file.close()

#s_file = open('','w')
if len(error_song_names)>0:
    print("The following song filenames did not end with a rating 0-4:")
    for this_name in error_song_names:
        print("    "+this_name)
    print("")

print("loopable_unique_songs_count: "+str(loopable_unique_songs_count))
print("looper_unique_songs_played_count: "+str(looper_unique_songs_played_count))
print("Song plays by rating:")
for key in looper_plays_counts.keys():
    print(key+": "+str(looper_plays_counts[key]))
print("Songs by rating:")
for key in looper_playable_counts.keys():
    print(key+": "+str(looper_playable_counts[key]))

#input("press enter to exit...")
#s_file.close()
