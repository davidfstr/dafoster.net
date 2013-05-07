---
layout: post
title: Avoid feeling like a port on the Mac
tags: [Software]
x_date_written: 2013-04-15

---

Mac users get rather annoyed when using programs that feel like they're just a port from another OS (usually Windows).

Here's are a few important points for making your Mac app feel like a native app:

* The user should never have to refresh local information that an application is viewing. Refresh should happen automatically when needed.

    * *Exception:* Web browsers. (The HTTP protocol provides no means to detect whether a web page requires refresh while it is being viewed.)
    
    * *Common violation:* Wait for an application to close, without auto-refreshing the application list. [*violated by Adobe Flash Updater*]
    
    * *Common violation:* Wait for disk to be inserted, without auto-refreshing the disk list. 
    
* When altering settings, change take effect *immediately*. If these settings are presented in a dialog, the changes can be reverted by pressing Cancel.

    * <p>*Common violation:* Settings dialogs that have an "Apply" button in addition to "OK" and "Cancel".</p>
    
* When dialogs are used to present information, the buttons in the dialog should have titles that are useful and easy to interpret. The default action should be presented as the right-most button.

    * *Example:* The Log Out action presents a dialog asking the user to confirm whether they want to log out, with buttons "Cancel" and "Log Out".
    
    * *Common violation:* Any dialog with "Yes", "No", and "Cancel" buttons.

* Don't ask the user any information that can be detected automatically with high confidence.

    * *Common violation:* Asking the user what language to use. [*Some installers*]
    
    * *Common violation:* Web pages for downloading software that prompt the user to select 32-bit vs. 64-bit architecture or an OS version.

* Aesthetics are important. If you make an ugly app, it probably won't be used.

* Drag & drop should be supported whenever it seems like it should make sense.


And now for some nitpicks related to command key shortcuts:

* Common command key shortcuts must be supported and not modified:

    * Command-Shift-Z = Redo [*violated by all Microsoft programs*]
    
    * Command-Left/Right = Move to beginning and end of line [*violated by all Microsoft programs*]
    
    * Command-F = Find [*violated by Microsoft Outlook*]
    
    * Command-P = Print [*violated by Sublime Text*]

* All command key shortcuts must include the command key. That is neither Control nor Option (Alt) can be the primary modifier for a shortcut sequence.

* Do not make shortcuts with the function keys (F1 - F15). They are hard to remember.

* All command key shortcuts must be tied to a menu item.

    * *Example:* Command-Option-Escape (Force Quit), which is analogous to Control-Alt-Delete on Windows, can actually be found in the Apple menu.
    
    * *Exception:* Command-Shift-3 and Command-Shift-4 are legacy shortcuts that take screenshots.

* There is no such thing as the Apple key. You probably meant the Command key.

* There is no such thing as the Backspace key. You probably meant the Delete key - which is not to be confused with the Forward Delete key, which most Windows users just call Delete.

* Not all users have a right mouse button. In that case, you must instruct the user to Control-click instead of right-click.

    * *Exemplar:* The game Black and White detects whether the primary mouse is a single-button or a multi-button mouse and provides different instructions (and mouse graphics) for each case.

For all other issues, including other philosphical concerns to consider, read and follow the OS X [Human Interface Guidelines]&nbsp;(HIG). This is one of the best descriptions of the "Zen of the Mac". Every Mac developer should reread this every few years.

[Human Interface Guidelines]: https://developer.apple.com/library/mac/#documentation/UserExperience/Conceptual/AppleHIGuidelines/Intro/Intro.html
