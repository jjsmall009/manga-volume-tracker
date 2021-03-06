# Overall Idea

I've been mulling over this project for a few years now and I've finally decided to finally give it a go.

I have quite the collection of manga on my computer and it's pretty time consuming and cumbersome to keep track of when a new volume in a series comes out. My goal is to create a program that will maintain a database of the manga I have and query some API to determine which series have new volumes.

There's still a lot to decide and design but in general this is some of the ideas I have and some of the features I intend to implement.

- Nice UI. The main view will be a grid of images/titles for a series. Cover, name, etc.
- You can click on a series to bring up some basic info about it.
- There will be a button to scan through your series and check if any new volumes are out (it won't download anything, just let you know there's something new).
- Specify different "shelves" based on some sort of criteria. Completed series, favorites, etc.

## Current Progress

### Stage 4 - Better Software Design

- [ ] Type annotations
- [ ] Data classes maybe
- [ ] Logging
- [ ] Unit testing

### Stage 3 - Clean Up

- [ ] Refactor and clean up my code.
- [x] Add in loading bars or spinners.
- [x] Improve UI and polish up the look and feel.
- [x] Create a flow based layout for the series grid.
- [x] Application startup - load an initial library

### Stage 2 - GUI

- [x] Do some initial layout planning and GUI mockups.
- [x] Learn the basics of PyQt (PySide6 actually).
- [x] Get started with Qt Designer.
- [x] Organize files.
- [x] Integrate layout with the rest of my code.
- [ ] Work on proper logging.

### Stage 1 - Console Based Menu

- [x] Create a basic design doc of ideas and program features.
- [x] Take a look at which API has what I want.
- [x] Start iterating and do one small task at a time and build.
- [x] Fuzzy string matching.
- [x] Grab series data for each valid search result.
- [x] Compare volume results
- [x] Test some database functionality and design.
- [x] Implement console menu design.

## Volume regex types

There is no standard format for how a file is named in regards to what volume it is. That's why I'm going to write out some common patterns.

- Aho-Girl v01 - leading 0 - [v0#] to [v##]
- Ichigo 100% 01 - no v/vol/volume - [0#] to [##]
- Kyochuu Rettou Volume 5 - no v/vol/volume and no leading 0 - [1] to [12]
- Ana Satsujin Vol. 1 - vol and then a space - [v/Vol. #]
- Wrapped in () - [(v##)]

## Program Components

1. Library Scanning
    - This program treats a top level folder/directory as a "library". That is, the subfolders of the top level folder are manga series.
    - To add a library to the program, give it a path to the directory and it will scan for valid subfolders.
    - The important pieces of information is a series title and the number of volumes for that series.
2. Web Scrapping
    - Once a library has been scanned we need to get information from MangaUpdates about each series.
    - This includes official title, source status and volumes, english status and volumes, things like that.
    - Values that don't have any matching data will be null.
3. Database Management
    - The database stores library and manga information, as well as the relationship between them.
    - A library has many manga entries and a manga entry can be in many libraries (will work on that as well as custom library filters later...).
    - The junction table between the library and manga table is just the ID of both.

## Data I Want from MangaUpdates

The whole crux of this program is to get an accurate english volume count for each series. That way the program can scan a library, pull in new data for ongoing series, and let yo know which series have new volumes.

- Series ID
- Series title from page
- Status in Country of Origin
  - \# of volumes
  - Complete, Ongoing, Cancelled, Hiatus
- Licensed (in English)
  - Yes, No, Dropped
- English Publisher
  - \# of Volumes (greatest)
  - Complete, Ongoing, N/A
- Authors
- Years

## Phase 1 - Menu Based Interface

Eventually this will be full fledged GUI app but for now the first implementation will be a console app. The menu below gives an idea of the features and functionality for phase one.

```text
============================
Welcome to Manga Manager 1.0
============================
Options:
  * 1: Add a Library
  * 2: Scan a Library
  * 3: Update Library
  * 4: Find New Volumes
  * 5: Exit
```

**1. Add a Library** - Specify a path and the program will scan the directory, find valid series, pull data for each series, and add all of the data to the database.
**2. Scan a Library** - Display a list of libraries. Pick one. It will then scan the directory for said library and look for changes (new series, removed series, new volumes for a series).
**3. Update a Library** - Display a list of libraries. Pick one. For series marked as ongoing, grab new data and update the database.
**4. Find New Volumes** - Simply query the database for a library and print out series that have local_volumes < english_volumes.

Now, some of the options might get combined or use bits and pieces of each other.

### Some User Stories

- Getting a list of new volumes
  1. "Scan a Library" to check for changes to local files.
  2. "Update a Library" to get new data for ongoing series (or mark as complete).
  3. "Find New Volumes" to grab data from the database and print out a list.  
  
### Random notes

Updating a library

```text
1. Before getting here, this is tested for valid library name/path
2. For each folder in this library
    a. Are you in the database?
        1. Yes, update my_volume count and move on
        2. No, 
            a. create Manga object
            b. Query api for data
            c. Add manga entry to database
3. For each row in database for this library
    a. Are you stored locally?
        1. Yes, carry on
        2. No, delete from junction table
```
