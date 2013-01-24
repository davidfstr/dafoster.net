---
layout: project
title: HandBrake Subtitles
summary: >
    Extends the popular HandBrake ripping and transcoding tool
    to enable processing subtitles from files, including the SSA subtitles
    found commonly in anime.
x_started_on: Feb 6, 2010
x_ended_on: Oct 2, 2010
x_languages: [C]
x_location: Online at svn://svn.handbrake.fr/HandBrake/trunk

style: |
    h3 { margin-bottom: -.3em; }
    small { font-size: 14px; }
    .span9 > hr { border-top-color: #d3d3d3; /* subtle */ }

---
[HandBrake] is a popular program for ripping DVDs and for converting
converts movie files from one format to another.

I extended HandBrake to support subtitles from file inputs (in addition
to DVDs) and to support the <acronym title="SubStation Alpha">SSA</acronym>
and <acronym title="Advanced SubStation Alpha">ASS</acronym> subtitle formats,
which are popular for encoding Japanese anime and foreign films.

My main motivation for adding subtitle support was to watch movies on my iPhone
while riding public transit and flying long-distance.

This was the first open source project I participated in.

## Download

* [HandBrake 0.9.5 and later][hbdownload] has subtitle support
* I have personally tested:
    * HandBrake svn3563 (2010100201)
    * HandBrake svn3567 (2010100301)

## You may also like...

* **[hbencode]** - A command line tool for automatically encoding multiple
  video files in bulk with optimized settings for an iPhone (or iPod Touch).

* **[Burn Planner]** - Automatically burn lots of files to DVDs.

## SSA Problems?

If you experience any major rendering issues with SSA subtitles, please:

* Check whether it is a known issue on the [HandBrake bug tracker].
* Otherwise please send a message to the [Bugs board] on the HandBrake forum.
* Only if you are not satisfied with the response there, then you may try
  [contacting me directly].

These days (as of 2011) I am more or less inactive on HandBrake development.
Yet I am currently your best shot at getting SSA issues fixed. Therefore if you
really want to get a particular issue fixed, you are encouraged to find a
creative way to motivate me.[^motivate] :-)

## Updates

### Simultaneous subtitle support added
<small>2011-02-24</small>

Committed: <https://forum.handbrake.fr/viewtopic.php?f=4&t=18379&p=93265>

---
### HandBrake 0.9.5 released
<small>2011-01-03</small>

Now everyone can see my SSA subtitle improvements.

<http://handbrake.fr/?article=11>

---
### SSA burn-in support committed!
<small>2010-09-28</small>

At long last. The main body of work is now complete.

Committed: <https://forum.handbrake.fr/viewtopic.php?f=4&t=17609&start=75#p83649>

---
### SSA burn-in now compiles under all supported architectures.
<small>2010-09-19</small>

Announced: <https://forum.handbrake.fr/viewtopic.php?f=4&t=17609&start=50#p83250>

---
### Initial version of SSA burn-in patch completed.
<small>2010-08-14</small>

Announced: <https://forum.handbrake.fr/viewtopic.php?f=4&t=17609#p81389>

---
### Wrote HandBrake Architectural Guide.
<small>2010-07-02</small>

This should help new developers on the HandBrake project come up to speed more quickly.

Committed: <https://forum.handbrake.fr/viewtopic.php?f=4&t=16559#p77909>

---
### Now decodes SSA to UTF-8 subtitles.
<small>2010-06-01</small>

Subtitled anime is now playable on iPhone, albeit without styling info.

Committed: <https://forum.handbrake.fr/viewtopic.php?f=4&t=16538#p77832>

---
### Can now transcode all subtitle formats that it can output.
<small>2010-05-20</small>

HandBrake can now transcode all subtitle formats that it can output (VOB, UTF-8, TX3G).

Committed: <https://forum.handbrake.fr/viewtopic.php?f=4&t=16267#p77158>

---
### General support for subtitles from file-inputs.
<small>2010-05-04</small>

Committed: <https://forum.handbrake.fr/viewtopic.php?f=4&t=16099#p76255>

---
### Approach decided.
<small>2010-04-13</small>

Announced to the HandBrake community here:  
<https://forum.handbrake.fr/viewtopic.php?f=4&t=15967>


[HandBrake]: http://handbrake.fr/
[hbdownload]: http://handbrake.fr/downloads.php
[HandBrake bug tracker]: https://trac.handbrake.fr/report/11
[Bugs board]: https://forum.handbrake.fr/viewforum.php?f=12
[contacting me directly]: https://forum.handbrake.fr/ucp.php?i=pm&mode=compose&u=12649
[^motivate]: Perhaps by introducing me to a really awesome TV show or anime series that happens not to transcode its subtitles correctly. Particularly if I'm about to fly somewhere. Other ideas encouraged.
[hbencode]: https://github.com/davidfstr/hbencode#readme
[Burn Planner]: /projects/burn-planner/