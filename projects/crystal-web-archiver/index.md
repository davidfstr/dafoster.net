---
layout: project
title: "Crystal: A Website Archiver"
subtitle: Free Website Downloader for Mac & Windows
subtitle_hidden_from_page_header: true
summary: >
    Crystal is a free website downloader and archiver for Mac, Windows, and Linux.
    Save entire websites for offline viewing and long-term digital preservation.
logo_png_filename: logo-128.png
started_on: 2011-09-30
ended_on: Ongoing
x_active_time_ranges:
    - [2011-09-30, 2012-01-25]
    - [2021-02-28, 2021-03-23]
x_languages: [Python]
x_lines_of_code: 4,106
x_location: Cathode at /Users/davidf/Projects
featured: true

style: |
    .download-links li { margin-bottom: 0.5em; }

---
**Crystal** is a free tool that downloads high-fidelity copies of websites
for long-term archival and offline viewing.

It works best on traditional websites made of distinct pages using 
limited JavaScript — such as **blogs**, **wikis**, and other **static websites** —
although it can also download more dynamic sites which have infinitely 
scrolling feeds of content, such as social media sites.

Crystal saves downloaded websites in an **archival-friendly format** where 
pages are stored in their original form (including all HTTP headers) and 
metadata is kept in a [SQLite database](https://sqlite.org/lts.html), 
making your archives durable and self-contained.

<img src="https://raw.githubusercontent.com/davidfstr/Crystal-Web-Archiver/main/README/crystal-ui.png"
     alt="Crystal's user interface"
     title="Crystal's user interface"
     style="max-width: 100%;" />


## Download

<ul class="download-links">
<li>📦 <a href="https://github.com/davidfstr/Crystal-Web-Archiver/releases/download/v2.3.0/crystal-mac-2.3.0.dmg"><strong>macOS 14 and later</strong></a></li>
<li>📦 <a href="https://github.com/davidfstr/Crystal-Web-Archiver/releases/download/v2.3.0/crystal-win-2.3.0.exe"><strong>Windows 11 and later</strong></a></li>
<li>📦 <strong>Linux:</strong> Install from source via <code>pipx install crystal-web</code> 
    (<a href="https://github.com/davidfstr/Crystal-Web-Archiver#download">details</a>)</li>
</ul>

[All releases &raquo;](https://github.com/davidfstr/Crystal-Web-Archiver/releases)


## Features

* **Download entire websites** with a single click, or precisely select
  which pages to download from complex sites.
* **Browse archived sites offline** in your regular web browser — 
  navigate downloaded pages just like you would online.
* **Archival-quality storage** — pages are saved in their original form 
  with all HTTP headers, suitable for long-term digital preservation.
* **Runs on Mac, Windows, and Linux.**
* **Free for noncommercial use.**


## Getting Started

Crystal makes it easy to download and archive websites. For a step-by-step 
walkthrough — including video tutorials — see the 
[Tutorial](https://github.com/davidfstr/Crystal-Web-Archiver#tutorial) 
on the project page.

There are many practice websites you can try downloading at 
<https://daarchive.net/>.


## Learn More

* [Full documentation & source code on GitHub](https://github.com/davidfstr/Crystal-Web-Archiver#readme)
* [Release notes](https://github.com/davidfstr/Crystal-Web-Archiver/blob/main/RELEASE_NOTES.md)
* [Complex website download examples](https://github.com/davidfstr/Crystal-Web-Archiver/wiki/Complex-Website-Download-Examples)
* [Report a bug or request a feature](https://github.com/davidfstr/Crystal-Web-Archiver/issues/new)
