import os
import eyed3

def writeMusicToFile(musiclist, musicfilepath):
    with open(musicfilepath, "wb") as file:
        output = ""
        for track in musiclist:
            output += musicFormatter(track)
        file.write(output.encode('utf-8'))
def musicFormatter(track):
    string = "".join(["begin track","\n    file=",track[0],"\n    artist=",track[1],"\n    name=",track[2],"\nend track\n\n"])
    return string

def copyFile(filepath, destinationFolder):
    with open(filepath, "rb") as sourcefile:
        with open(os.path.join(destinationFolder, os.path.split(filepath)[1]), "wb") as destinationfile:
            destinationfile.write(sourcefile.read())

def inputMusicFile():
    musicFile = input("Objects in space folder pls: ") #default "C:/GOG Games/Objects in Space/assets/music.txt"
    if musicFile == "":
        musicFile = "C:/GOG Games/Objects in Space/"
    elif not musicFile[-1] == "/":
        musicFile += "/"
    musicFile += "assets/music.txt"
    if not os.path.isfile(musicFile):
        print("You must specify an existing music.txt file")
        return inputMusicFile()
    return musicFile

def parseMusicFile(musicfilepath): #parses into a list with other lists (tracks) containing [filename, authorname, trackname]
    with open(musicfilepath, "rb") as file:
        contents = file.read().decode("utf-8")
    tracks = contents.strip("\n").split("begin track\n    ")[1:]
    for track in tracks:
        new = track.strip("\n").strip("\nend track")
        new = new.split("\n    ")
        new[0] = new[0][5:]
        new[1] = new[1][7:]
        new[2] = new[2][5:]
        tracks[tracks.index(track)] = new
    return tracks
    
def inputNumberinRange(query, limitmin, limitmax):
    ipt = input(query)
    try:
        ipt = int(ipt)
    except ValueError:
        print("Please type a number")
        ipt = inputNumberinRange(query, limitmin, limitmax)
    if ipt < limitmin:
        print("Value too low")
        ipt = inputNumberinRange(query, limitmin, limitmax)
    if ipt > limitmax:
        print("Value too high")
        ipt = inputNumberinRange(query, limitmin, limitmax)
    return ipt

def importFolder(folderpath, musicFiles):
    files = []
    for file in [f for f in os.listdir(folderpath) if os.path.isfile(os.path.join(folderpath, f))]:
        if os.path.splitext(file)[1] == ".mp3":
            files.append([file, "", ""])
    #for file in musicFiles:
    #    if [file[0], "", ""] in files:
    #        files[files.index[[file[0], "", ""]]][1] = file[1]
    #        files[files.index[[file[0], "", ""]]][2] = file[2]
    return files

def inputFolder():
    ipt = input("Input folder name: ").strip('"')
    if len(ipt) == 0:
        print("You must specify an existing folder")
        return inputFolder()
    if ipt[-1] != "/":
        ipt += "/"
    if not os.path.isdir(ipt):
        print("You must specify an existing folder")
        return inputFolder()
    return ipt



musicFilePath = inputMusicFile()
musicFiles = parseMusicFile(musicFilePath)
folderfiles = []
deletionlock = True
#loop:
while True:
    print(
"""
Main screen
q  - quit program
f  - change music source
t  - add names and authors
vm - view music file music
vf - view music folder music
ca - copy over all added music from folder to file
cs - copy over specific music from folder to file
w  - write to music file
DELETING:
d  - enable/disable deleting
da - delete ALL music file
ds - delete specific music from file
""")
    ipt = input("Command: ")
    if ipt == "q":
        break
    elif ipt == "f":
        playlistFolderPath = inputFolder()
        folderfiles = importFolder(playlistFolderPath, musicFiles)
    elif ipt == "t":
        for i in range(len(folderfiles)):
            filename = os.path.split(folderfiles[i][0])[1]
            print(filename)
            try:
                absfilename=os.path.join(playlistFolderPath, folderfiles[i][0])
                audiofile = eyed3.load(absfilename)
                folderfiles[i][2] = audiofile.tag.title
                folderfiles[i][1] = audiofile.tag.artist
            except eyed3.Error as e:
                print("Small error processing metadata {}".format(e))
            if folderfiles[i][2] == "":
                #[filename, authorname, trackname]
                folderfiles[i][2] = input("What is '" + filename + "' name?: ")
            if folderfiles[i][1] == "":
                folderfiles[i][1] = input("What is '" + filename + "' author?: ")
    elif ipt == "vm":
        print("MusicFile tracks:")
        for i in range(len(musicFiles)):
            print("Track #" + str(i+1))
            print("Name    : " + musicFiles[i][2])
            print("Author  : " + musicFiles[i][1])
            print("FileName: " + musicFiles[i][0])
            print("Included: " + str(musicFiles[i] in folderfiles))
    elif ipt == "vf":
        print("MusicFolder tracks:")
        for i in range(len(folderfiles)):
            print("Track #" + str(i+1))
            print("Name    : " + folderfiles[i][2])
            print("Author  : " + folderfiles[i][1])
            print("FileName: " + os.path.split(folderfiles[i][0])[1])
            print("Included: " + str(folderfiles[i] in musicFiles))
    elif ipt == "ca":
        for track in folderfiles:
            print(track[2], track[1])
            if  track[2] != "" and  track[1] != "":
                if track in musicFiles:
                    print(track[2] + " already included, skipping")
                else:
                    copyFile((playlistFolderPath + track[0]), (os.path.split(musicFilePath)[0]))
                    musicFiles.append([os.path.split(track[0])[1], track[1], track[2]])
            else:
                print("Track #" + str(folderfiles.index(track)+1) + " translations not completed, skipping")
    elif ipt == "cs":
        trackNumber = inputNumberinRange("Track Number?: ", 1, len(folderfiles)) - 1
        track = folderfiles[trackNumber]
        if track[2] != "" and  track[1] != "":
            if track in musicFiles:
                print(track[2] + " already included")
            else:
                print("Copying {} to {}".format((playlistFolderPath + track[0]), os.path.split(musicFilePath)[0]))
                copyFile((playlistFolderPath + track[0]), (os.path.split(musicFilePath)[0]))
                musicFiles.append([os.path.split(track[0])[1], track[1], track[2]])
        else:
            print("Track #" + str(folderfiles.index(track)+1) + " translations not completed")
    elif ipt == "w":
        writeMusicToFile(musicFiles, musicFilePath)
    elif ipt == "d":
        deletionlock = not deletionlock
        print("Deletion lock is now", deletionlock)
    elif ipt == "da":
        if not deletionlock:
            musicFiles = []
        else:
            print("Deletion is locked")
    elif ipt == "ds":
        if not deletionlock:
            ipt = inputNumberinRange("Track Number?: ", 1, len(musicFiles)) - 1
            del musicFiles[ipt]
        else:
            print("Deletion is locked")
    elif ipt == "debug":
        print(folderfiles)
        print(musicFiles)
