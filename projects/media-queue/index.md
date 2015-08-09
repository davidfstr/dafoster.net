---
layout: project
title: MediaQueue
x_aka: OmniQueue
summary: >
    A system for tracking and searching for media items
    (movies, TV series, anime, books) in various different
    media sources.
started_on: 2015-01-02
ended_on: 2015-01-06
x_languages: [Google_Apps_Script]
x_lines_of_code: 819
x_location: "Google Docs > Media Queue Latest - David Foster"

full_width: true

style: |
    .img-right { float: right; margin-left: 0.5em; }
    
    /* Override Bootstrap rule that conflicts with carousel */
    #screenshots img { max-width: none; }

carousels: true
script: |
    // Display carousel
    $(window).load(function() {
        $('#screenshots').orbit({ bullets: true });
    });

---

MediaQueue allows you to write down media that you want to watch - movies, TV series, books, etc. - and helps you to quickly locate the media for streaming, download, pickup, or purchase.

MediaQueue is implemented as a Google Docs spreadsheet with custom macros that search for media items entered into the sheet.

<div style="margin-bottom: 3em;">
    <div id="screenshots">
        <img src="/assets/2015/media-queue/screen1.png" width="750" height="525" />
        <img src="/assets/2015/media-queue/screen2.png" width="750" height="525" />
        <img src="/assets/2015/media-queue/screen3.png" width="750" height="525" />
    </div>
</div>

## Download

In the past I have provided installation instructions for MediaQueue 1.0.

Since then I have implemented further extensions, fixing old media sources and adding new ones. These subsequent changes were not integrated to the public 1.0 version due to the time required to revise instructions and migrate data from prior versions.

For now I have decided to take down the installation instructions unless I [hear sufficient interest](/contact/) from site visitors that convinces me that the maintenance effort is worth it.

Nevertheless if you're still curious about how the code works, I've decided to leave the 1.0 code online:

<a class="btn btn-primary" target="_new" href="https://gist.github.com/davidfstr/0f212ddf160b2f776884">
    Browse Source Code for 1.0
</a>
