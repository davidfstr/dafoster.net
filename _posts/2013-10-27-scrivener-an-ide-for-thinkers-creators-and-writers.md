---
layout: post
title: "Scrivener: An IDE for thinkers, creators, and writers"
tags: [Productivity]

---

Today I invested a few hours into learning [Scrivener], a tool created for the purpose of writing long-form texts such as books, screenplays, etc. However it wasn't the word processing capabilities of Scrivener that caught my eye but rather its system for **organizing** the fragments, research materials, and other documents that support the act of creating something new.

I have been looking for a way to organize the disparate source material I've been collecting on a few large project areas. For example I've been investigating ways for make more interactive software development tools since being inspired by [Bret Victor]'s work.

I've already been using [Evernote] as a way to **capture** sources of inspiration such as webpages, tech talk summaries, and research paper PDFs. However Evernote has a pretty terrible organizational model:

* You have exactly one level of hierarchical nesting available in the form of "notebooks".
* Within a notebook you have no ability to rearrange individual "notes" in a custom order.
* Notebooks themselves cannot be rearranged.
* The little tiles that preview individual notes cannot be customized in any way.

Scrivener on the other hand is extremely flexible with how it allows you to organize the documents that comprise a project:

* Documents can be rich-text, images, audio, or video. Rich-text documents can be edited natively.
* Documents can be given arbitrary names and reordered at will.
* Documents can be arbitrarily nested inside folders. And indeed inside other documents as well.[^docs-and-folders]
* Folders can be viewed in **corkboard mode** where items inside the folder are represented as index cards summarizing each item laid out on a virtual corkboard. This is great for getting an overview of a folder's contents.
    * The text on an item's index card can be customized.
    * The corkboard can be put into a freeform mode where items can be rearranged at will in space. This is great for spatial organization.
    * If a corkboard item itself contains multiple items, it appears as a *stack* of index cards instead of just an individual index card. This is great for determining at a glance how "big" something actually is.
* Items can be given a **label** (with a color and name) and a **status**, both of which are displayed visually on its summarizing index card. Custom metadata can be given as well. All of this metadata can be used for targeted searches.
* There are several ways to **view and edit multiple documents at once**:
    * Selecting a folder displays all of its contained items as a single continuous editable document.
    * Selecting multiple individual documents will also present a single continuous document.
    * The main editor view can be split horizontally or vertically to allow working on two documents side-by-side, or the same document at two locations.
    * Documents can be opened in separate QuickReference windows to arrange them off to the side.
* Documents can be located using a targeted search.
* Folder (and file) icons can be customized. This great for indicating at a glance how "big" a folder is or what kind of thing it represents. A good set of built-in icons are provided, and you can add your own.
* Custom **collections** of documents can be created that allow you to quickly browse between a subset of the documents in the project. These collections can be created manually, or automatically by a populating search.

Other nice features include:

* All changes to documents are saved automatically.
* Version control is built in, allowing you to take snapshots of a document at different times.
    * Previous versions can be restored if you made an undesirable change to the current version.
    * Multiple versions can be compared using diffs that are aware of not just lines but also paragraphs, clauses, and individual words.

Right now my plan is to continue capturing source materal using Evernote, since it excels at capture. But then I'll move the captured items over to Scrivener in order to actually organize them into something coherent I can chew on.


[Scrivener]: http://www.literatureandlatte.com/
[Bret Victor]: http://worrydream.com/
[Evernote]: https://evernote.com/

[^docs-and-folders]: There isn't a strong distinction between folders and documents. Folders can themselves have textual content, although this isn't common. Marking an item as a "folder" is mainly a hint to Scrivener that the item's primary function is to group items together.