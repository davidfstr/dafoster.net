---
layout: post
title: Retrospect vs. Time Machine
tags: [Digital_Preservation]
date_published: 2012-12-21
date_updated: 2012-12-21

---

## The old Retrospect 6.0

In the past I have used Retrospect 6.0 to backup my Macs, since it was one of
the few programs that reliably backed up everything correctly, with all the 
metadata intact. But it is looking much less attractive these days...

* It no longer finds my laptop on the network reliably, due to some bug.
  Especially when switching between wireless and wired networks.
  Thus I often miss backups.
  
* It is slow.

* It does not groom backups.

* It stores everything inside a single monolithic file,
  which is at risk of corruption.

## The new Retrospect 8.0

The latest version of Retropect (8.0) is somewhat better but has some problems:

* It does not seem to backup all attributes correctly.
  For example, volume icons do not seem to be restored correctly.
  Inaccurate backups are useless.

* It is more complicated to use.

* Automatic grooming, although supported, is so slow to be practically unusable.
  It takes maybe 2x as long to do one grooming operation as an incremental backup.

## Time Machine

Now there is Time Machine. Since my primary systems are 10.5+, I can use it.

* It *should* support reliable backup of all filesystem attributes,
  since it was made by Apple, who is in a position to know about them.
  Also, Apple typically makes solid products.

* It has quick, automatic, incremental backups.

* It also grooms automatically while it is backing up. Grooming behavior is
  intelligent, keeping snapshots at sensible intervals.

* The single-file restore interface is precise, intuitive, and fast.

Only wrinkle is that Time Machine is not really designed to backup to network
drives, however there are [instructions for circumventing this].
(Of course there is Time Machine + Time Capsule for network backups, but a
Capsule is egregiously expensive.)

### 2012 Update

Time Machine misses a few filesystem attributes that Retrospect 6.0 nailed back
in the day, like volume icons.

I think it may also strip HFS+ extended attributes, since applications appear
to be quarantined after they are restored from a Time Machine backup.

One last nitpick is that TM has very poor handling for bad media and bad blocks.
In particular if your primary hard drive develops bad blocks, which is an early
sign of imminent failure, Time Machine will choke and refuse to backup the
entire volume. And this is exactly at the time you need it your files backed up
the most, when your hard drive is likely to fail.


[instructions for circumventing this]: http://safalra.com/other/time-machine-network-drive/