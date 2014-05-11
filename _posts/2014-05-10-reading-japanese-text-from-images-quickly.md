---
layout: post
title: Reading Japanese text from images
tags: [Offtopic]

style: |
    
    .bad { background-color: pink; }
    .good { background-color: MediumSeaGreen; }
    
    /* Make kanji big so that they are legible */
    .kanji { font-size: 28px; }
    
    /* Extra spacing between bulleted list items to separate large kanji characters */
    .post ul li { line-height: 36px; }

---

I've been intensively studying Japanese recently[^post-delay], and something I have to do quite a lot is look up Japanese words that I see in images. Particularly words that involve a lot of kanji characters.

Last evening I hacked together a program that allows me to select arbitrary Japanese from an image on my screen, performs optical character recognition (OCR) on it, and outputs it as regular Unicode text. This regular text can then be looked up in an online Japanese-English dictionary, such as the excellent [jisho.org](http://jisho.org/).

Let's take the following sentence:

![Japanese sentence with lots of kanji](/assets/2014/kanji.png)

The first word in that sentence already has 4 kanji characters, which would normally take a long time to look up individually.[^kanji-lookup]

With my program, I can take a screenshot of this sentence as it appears on my screen and the program will immediately output the following text:

* <p class="kanji">痴話喧嘩は<span class="bad">維</span>続中か</p>

Then I can lookup the words as usual from jisho.org's [Words](http://jisho.org/words/) search:

* <span class="kanji">痴話喧嘩</span> = lover's quarrel
* <span class="kanji"><span class="bad">維</span>続</span> = ?
* <span class="kanji">中</span> = inside; in (a space or building)

Character recognition still isn't perfect, as demonstrated by the character marked in <span class="bad">pink</span> above, which wasn't decoded correctly.

Nevertheless even having a partially correct character is useful, as I can still use jisho.org's [Kanji](http://jisho.org/kanji/) search to break it down into its component radicals:

* <span class="kanji"><span class="bad">維</span> = <span class="good">小</span> + <span class="good">幺</span> + <span class="good">糸</span> + <span class="bad">隹</span></span>

And then use a few of the *correct* radicals in the [Kanji by Radicals](http://jisho.org/kanji/radicals/) search to quickly find the correct character:

* <span class="kanji"><span class="good">継</span> = <span class="good">小</span> + <span class="good">幺</span> + <span class="good">糸</span> + ｜ + 米</span>

And so the original word can now be looked up correctly:

* <span class="kanji"><span class="good">継</span>続</span> = continuation

[^post-delay]: All this studying is one reason I haven't posted in a while.

[^kanji-lookup]: Individual kanji can be looked up by their component radicals at jisho.org's [Kanji by Radicals](http://jisho.org/kanji/radicals/) search. Unfortunately it can take a few minutes to lookup each character.

## How it Works
 
The program operates by waiting for you to take a screenshot using Command-Shift-4 (on the Mac), observing the new screenshot appearing on the desktop, and feeding it to the [nhocr] tool, which reads the Japanese text inside the screenshot and prints it.

## Source Code


```
#!/usr/bin/env python
# 
# nhocr_desktop.py
#
# Waits for screenshots to appear on the desktop,
# scans them for Japanese text using OCR,
# and prints out the text that was decoded from the image.
# 
# This script is useful for rapidly converting on-screen Japanese
# text to actual text that can be looked up.
#
# Prerequisites:
#   * nhocr
#   * ImageMagick
#   * Python 2.7 - maybe 2.6 okay too
#   * watchdog
# 
# @author David Foster
# 

import os.path
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ScreenshotFileCreationEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            if 'Screen Shot' in os.path.basename(event.src_path):
                # Convert screenshot to PPM format with ImageMagick
                subprocess.check_call([
                    'convert', event.src_path, '/tmp/line.ppm'])
                
                line = subprocess.check_output([
                    'nhocr', '-line', '/tmp/line.ppm', '-o', '-'])
                print line.decode('utf-8'),

event_handler = ScreenshotFileCreationEventHandler()

observer = Observer()
observer.schedule(event_handler, '/Users/me/Desktop', recursive=False)
observer.start()

print 'Waiting for screenshots on the desktop to analyze...'
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
```

[nhocr]: https://code.google.com/p/nhocr/
