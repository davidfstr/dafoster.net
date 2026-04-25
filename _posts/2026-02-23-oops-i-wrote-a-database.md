---
layout: post
title: Oops, I wrote a database
tags: [Software]

wide_image_filepath: /assets/2026/oops-i-wrote-a-database/windows-move-aside--article-image.png

---

> Never write your own database or filesystem. It's way harder than you expect.  
> — some wise programmer[^never-write-your-own-database]

Databases and filesystems are hard to write in part because they have very strong requirements around **never losing data** (durability) even when unusual events happen such as unexpected process termination, hardware failure, out of disk space, or out of memory. I realized recently that Crystal - a program of mine for downloading websites - should strive to provide the same high reliability guarantees when saving websites to disk in its project format. And so began my ~3-week quest to shore up the ACID (atomicity, consistency, isolation, and durability) properties of how Crystal writes to its projects. Here are a few things I learned along the way.

[^never-write-your-own-database]: I can't find a specific original person who said "Never write your own database or filesystem". The closest discussion I was able to locate comes from [Never Write Your Own Database](https://terrycrowley.medium.com/never-write-your-own-database-736f704c780). So perhaps this specific quote just comes from me now 🙂


## Background

A Crystal project is an ACID-compliant storage system for holding downloaded website data: multiple-reader, single-writer.

It contains a SQLite table of downloaded page **revisions**, each row of which corresponds to an on-disk file with the revision's content.

![A project's revisions table, with a line connecting each table row to a file](/assets/2026/oops-i-wrote-a-database/revision-table-to-files.svg)

Adding a revision requires creating both a database row and file at the same time.


## Strategy: Write file then rename to commit<small>, rather than (re)write in place</small>

It's not safe to write a file directly to its final location because sudden process termination or disk disconnection could abort the write in the middle, leaving an incompletely written file in its final "committed" location.

Instead it's safer to write a file first to a temporary location on the same filesystem as its committed location. After the write is complete, move it to its final place.

![An old revision file connected by line to multiple readers (👁 icons). A new revision file connected by line to one writer (✏️ icon). A wide "Replace" arrow leading from the new revision file to the old revision file.](/assets/2026/oops-i-wrote-a-database/file-write-and-replace.svg)

If sudden process termination stops the write, when Crystal reopens the project it will delete the temporary file. Additionally Crystal will check whether the highest numbered revision row in the database is missing its corresponding revision file, and delete the incomplete revision row if so.


## Strategy: Write file then replace to commit<small>, if the file may have concurrent readers</small>

Crystal projects using the Pack16 format have a more complex challenge: Each revision row now corresponds to an entry in a zip file that can be shared by up to 16 revisions. Thus writing one revision may require altering a zip file containing a different revision that is being concurrently read.

![A project's revisions table, with a line connecting each table row to an entry inside a zip file. There are many rows but only a few zip files, with each zip file connected to multiple rows.](/assets/2026/oops-i-wrote-a-database/revision-table-to-zip-entries.svg)

Similar to the write+rename strategy, we can use a write+replace strategy: Write a new revision to a new zip file and then replace the old zip file. Existing readers of the old zip file will not be disrupted; they will still be able to read from the copy of the zip file that they opened even though it is no longer visible in the filesystem.

![An old zip file connected by line to multiple readers (👁 icons). A new zip file connected by line to one writer (✏️ icon). A wide "Replace" arrow leading from the new zip file to the old zip file.](/assets/2026/oops-i-wrote-a-database/zip-file-write-and-replace.svg)


## Windows-only: Move-aside a file before replacing it

On macOS and Linux the above strategy just works; it is possible to replace a file that is open for reading with a different file without doing anything special. However on Windows files are opened in an exclusive mode by default that prevents reading or writing the file while it is still open. **You must *explicitly* open a file with `FILE_SHARE_READ`, `FILE_SHARE_WRITE`, or `FILE_SHARE_DELETE` modes on Windows if you want to allow concurrent readers, writers, or deleters.** Crystal defines its own [`open_nonexclusive`] function to get this same non-exclusive open behavior across all operating systems.

However Windows presents another challenge: It does not allow you to *replace* a file that is opened for reading even if it is opened with all of `FILE_SHARE_READ`, `FILE_SHARE_WRITE`, and `FILE_SHARE_DELETE`, despite allowing you to *delete* it or *rename* it.

So on Windows, Crystal renames an old zip file to a transitional (but crash-durable) "moved-aside" location before renaming the new zip file to the original location of the old zip file. So the total process looks like:

1. Write new zip file to temporary location
2. Move aside the old zip file to a moved-aside location
    - This is permitted even if the old zip file has readers, when opened with `FILE_SHARE_WRITE`
3. Rename the new zip file to its permanent location, where the old zip file was
4. Delete the old zip file in its moved-aside location
    - This is permitted even if the old zip file has readers, when opened with `FILE_SHARE_DELETE`

![An old zip file connected by line to multiple readers (👁 icons). A "moved-aside" zip file. A new zip file connected by line to one writer (✏️ icon). A wide "2. Move Aside" arrow leading from the old zip file to the moved-aside zip file. A wide "3. Rename" arrow leading from the new zip file to the old zip file. A "4. Delete" box beside the moved-aside zip file.](/assets/2026/oops-i-wrote-a-database/windows-move-aside.svg)

The above (non-atomic) process introduces several complexities:

* &ZeroWidthSpace;A. If **a new concurrent reader** appears between steps 2 and 3, when the old zip file has been moved-aside but not yet replaced with a new zip file, the reader must know to look for the old zip file at the moved-aside location in addition to its normal location.
* B1. If **sudden process termination** happens between steps 2 and 3, some kind of repair process after reopening the project must move the old zip file from its moved-aside location back to its normal location.
* B2. If **sudden process termination** happens between steps 3 and 4, the old zip file in the moved-aside location should be deleted.

In case B1, Crystal performs the repair at read time, when an entry from the zip file is first read after reopening the project.


## Read Repair<small>: A time to clean up incomplete operations</small>

When Crystal performs a read on a Pack16 project, looks for a zip file corresponding to a revision, and does not find it, it will then look for a moved-aside zip file that was left behind during scenario B1 above. If it finds such a moved-aside zip file it will *repair* it by moving it back to its normal location.

Note that this kind of repair is itself a kind of **write** which might happen during a high-level **read** operation. Since Crystal allows *concurrent reads*, the possibility of a repair happening during a read means that *concurrent writes* are now possible too... Yikes.

Concurrent writes to the same file are unsafe by default but can be made safe with **mutual exclusion**. Crystal maintains an in-memory mutex lock for each file it is in the middle of repairing to prevent concurrent writes from corrupting the project.


## Zooming Out: The Big Picture

I expected this work to take 1–1.5 weeks. It took about three. Most of the overrun came from a cascade of complications I didn't see coming:

* Windows opens files exclusively by default, so even allowing **concurrent readers** required `FILE_SHARE_READ`.
* Windows then refused to *replace* a file that was still open for reading — even with all three share modes set — so **writes** required the move-aside dance and `FILE_SHARE_WRITE` / `FILE_SHARE_DELETE` on the reader side.
* The move-aside dance introduced two new **crash-recovery** cases (B1 and B2), which became read-repair.
* Read-repair quietly turned reads into potential writes, which forced in-memory **per-revision locks** to keep the multiple-reader/single-writer contract honest.

Each layer was reasonable on its own; the surprise was how much each one cost in aggregate.

Of the four ACID properties, **atomicity** and **durability** drove essentially all of this work. **Consistency** was largely a freebie given the architecture: the database lives in one place, only one process ever opens a project, and that process has at most one writer. **Isolation** was similarly cheap given the single-writer rule and the absence of in-place rewrites — with the wrinkle that read-repair turned a "read" into a {read + limited write}, requiring introducing per-revision locks.

It was a fun exercise in polishing one aspect of Crystal to a high standard. But I must say the caution around hand-rolling your own storage code is well earned: you may very well double or triple the time you expect it to take. 🙂


[`open_nonexclusive`]: https://github.com/davidfstr/Crystal-Web-Archiver/blob/21bbf89d358d88336a8ba4e506a9681a2a62d83a/src/crystal/filesystem/local.py#L15-L92
