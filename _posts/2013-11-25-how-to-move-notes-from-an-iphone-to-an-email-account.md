---
layout: post
title: How to move notes from an iPhone to an email account
tags: [Productivity]

---

If you have notes in the "On My Phone" or "On My Mac" accounts but want to move them to an email account instead, this article provides instructions for moving the notes. It's surprisingly tricky.

![](/assets/2013/notes-accounts-on-iphone.png)

## Easy Way <small>(Straightforward but tedious)</small>

Mail every note to yourself and copy the contents into the Notes program (if using OS X 10.8 - 10.9) or into Mail (if using OS X 10.7 or earlier).

<span style="color: red">**Caution:** This method loses the dates of the original notes which will mess up their ordering.</span>

## Hard Way <small>(Perfect migration but lots of steps)</small>

First you will need **OS X 10.7 (Lion)**, either already running on a computer you own or installed on a virtual machine, such as created by [Parallels](http://www.parallels.com/products/desktop/) or [VMware](http://www.vmware.com/products/fusion/). OS X 10.8 (Mountain Lion) and OS X 10.9 (Mavericks) [removed the notes syncing feature](https://support.apple.com/kb/HT4191) that these instructions depend on.

1. Sync the iPhone with iTunes. Be sure that in the **Info** tab of iTunes that the **Sync notes** option is checked. If the option isn't there then you might be running OS X 10.8+ where this option was removed.

   ![](/assets/2013/notes-sync-in-itunes.png)

2. Open Mail and configure it with the email account that you want the notes to be synced with. Make sure that in the Mail preferences that the **Show notes in Inbox** option is checked.

   ![](/assets/2013/notes-show-in-mail.png)

3. You should see a **Notes** folder in the left sidebar of the main mail window. It should also have a triangle that expands to show "On My Mac" and your email account. If there is no triangle then you may need to quit and relaunch Mail for it to pick up the synced notes from iTunes.

   ![](/assets/2013/notes-in-mail-sidebar.png)

4. Move all the notes inside the "On My Mac" to your email account.

5. Verify that your iPhone sees the notes added to your email account.

6. Tell iTunes to sync with the phone again so that the notes moved from "On My Mac" no longer appear on the iPhone under the "On My Mac" account.
  
   ![](/assets/2013/notes-sync-in-itunes.png)

   This last step didn't work as expected for me, as no notes disappeared from the "On My Mac" account on my iPhone. I tried using iTunes's special option to forcefully replace all notes on the iPhone with the Mac's notes on the next sync. That didn't work either.
  
   ![](/assets/2013/notes-force-sync.png)

   In the end to remove the old notes from the "On My Mac" account on the iPhone, I manually deleted each note on the iPhone itself. Not ideal but it didn't take too long.