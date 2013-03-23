---
layout: post
title: Migrating from BBEdit to Sublime Text
tags: [Software]

---

I've been using [BBEdit] as my primary text editor on the Mac for over 10 years. It is an extremely capable and mature editor with just about all the bells and whistles you can imagine. However the use of Sublime Text has been spreading throughout my workplace at Splunk[^splunk] so I decided I'd give it a try.

My initial impression was "BBEdit can do everything that Sublime can, what's the deal?" But after using Sublime full-time for about a week, I'm starting to come around to it.

Although it is true that both have comparable feature sets, Sublime's implementation feels more polished - not just eyecandy, but actually better usability.

* Incremental find
    * As you start typing the substring you want to find, it automatically starts searching within the current document. Frequently you don't have to finish typing the substring in order to get the result you want.
    * This saves a surprising amount of time compared to BBEdit where you have to finish providing a full substring (that you think is long enough) before kicking off the search.
    * **Edit:** *This is actually available in BBEdit under the "Live Search" command, but this is not part of the default Find experience and not advertised.*
* View a file without "opening" it (as a persistent tab)
    * Sublime keeps files of current interest available as tabs in the main window. If you just click on a file, it is shown in the editor but no tab is created by default. If you decide this is an important file, you can double-click on the file name to create an actual tab for it, which makes the file easy to return to.
        * Most "Goto X" actions in Sublime both show a file and create an actual tab for it, which usually is what you want.
    * If you click on any file at all in BBEdit, it is "opened" and added to the "Currently Open Documents" section, which is analogous to Sublime's set of open tabs. This can result in the "Currently Open Documents" section getting rather cluttered when rummaging around for a particular document, making it less useful.
* Minidocument view on the right side of an open file.
    * This makes it easier to get a bird's eye view of where you are in a long function or file.

Additionally, Sublime's marketing has some a much better job of exposing advanced features that turn out to be useful in daily use.

* "Goto Anything"
    * BBEdit has similar "Open File by Name", but it's slower, doesn't have as expressive syntax, and isn't incremental.
* "Open Folder"
    * This is equivalent to a BBEdit project.
* Plugins!
    * This is barely advertised on the BBEdit side but hugely promoted on the Sublime side. Thus lots of people are writing (publicly available) plugins for Sublime but not so many for BBEdit.

Some features in Sublime are named more obviously:

* Convert Indentation to Spaces. Convert Indentation to Tabs.
    * BBEdit calls these operations "Detab" and "Entab" respectively.

Some features in Sublime are easier to access:

* Change the displayed tab width.
    * To change this for a single file in BBEdit, you have to go to "Show Fonts", which I find completely nonintuitive.
    * BBEdit also allows you to change the default tab spacing *per source language* in its preferences, which makes sense given that different languages have different conventions.
    * However BBEdit does not permit you to change the tab width on a per project/folder basis, which is usually what you want when working on someone else's open source project.
* Access the function list. ("Goto Symbol...")
    * This can be done in Sublime entirely through the keyboard.

Sublime also has a few features lacking in BBEdit:

* Cross-platform support
    * This is huge when working in a mixed OS environment. You can use the same editor everywhere.

BBEdit still is better in a few areas:

* Can edit preferences in a GUI without mucking about in text files.
* Can quickly split a single file vertically to edit distant sections simultaneously.
* "Zap Gremlins..."
    * Deletes or replaces ASCII control characters and other nasties. Very useful for text pasted from web browsers, Word, or other less-than-pure sources of text.
* "Process Duplicate Lines..."
    * Eliminate duplicate lines in a file. This is often useful after performing a series of text transformations.
* "Process Lines Containing..."
    * Delete (or preserve) all lines containing a subexpression. Exactly like the `grep` command-line tool.
* Can edit files on an FTP/SFTP server directly.
* Customer support I've heard is top-notch.

I think I'm going to continue using Sublime Text. Featurewise it's about the same as BBEdit, but the cross-platform support[^cross-plat], active plugin community, and general polish <!-- & attention to usability --> are winning me over.

[BBEdit]: http://www.barebones.com/products/bbedit/index.html

[^splunk]: Splunk makes tools for analyzing large time-series datasets, such as log files. For details see the 3 minute [Splunk Product Overview](http://www.splunk.com/view/SP-CAAAHG6). I work on the Developer Platform, making it easy for other developers to build neat things on top of the Splunk core.

[^cross-plat]: It is extremely useful to be able to use the same full-featured text editor on any platform I use. I currently maintain a few open source projects that require testing, debugging, and development on multiple platforms (notably the [RDiscount](/projects/rdiscount/) Markdown processor) and it's nice being able to use the same editor everywhere.