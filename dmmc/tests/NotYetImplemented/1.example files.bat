


REM E:\Music\Recorded\Soundtracks\Mortal Kombat - Original Motion Picture Soundtrack\06 Orbital - Halcyon + On + On.flac
REM D:\Projects\DigitalMusicMC\bin\06 Orbital - Halcyon + On + On.flac.mp3

REM E:\Music\Video Game Music\Compilations\A Tribute To Nobuo Uematsu\nazarenonigretti_celes.mp3
REM D:\Projects\DigitalMusicMC\bin\A Tribute To Nobuo Uematsu\nazarenonigretti_celes.mp3


flac.exe -c -d "E:\Music\Recorded\Soundtracks\Mortal Kombat - Original Motion Picture Soundtrack\06 Orbital - Halcyon + On + On.flac" | lame.exe -h -m j --resample 44.1 -b 160 - "D:\Projects\DigitalMusicMC\bin\06 Orbital - Halcyon + On + On.flac.mp3" > errors-lastrun-manually-ranline-from-flac.txt

lame.exe -h -m j --resample 44.1 -b 160 "E:\Music\Video Game Music\Compilations\A Tribute To Nobuo Uematsu\nazarenonigretti_celes.mp3" "D:\Projects\DigitalMusicMC\bin\A Tribute To Nobuo Uematsu\nazarenonigretti_celes.mp3" > errors-lastrun-manually-ranline-from-mp3.txt