---
layout: post
title: Custom file icons, folder icons, and app icons on different operating systems
tags: [Software]

---

I recently extended my [website downloader, Crystal], so that the projects it creates have a proper icon on macOS, Windows, and Linux. It was a lot more challenging than I expected!

Crystal organizes a group of downloaded web pages into a **project**, which is a special folder containing a particular arrangement of files:

```
$ tree xkcd.crystalproj
xkcd.crystalproj      ← project
├── database.sqlite   ← web page metadata
└── revisions
    ├── 1   ← web page #1 content
    ├── 2   ← web page #2 content
    ├── 3   ← web page #3 content
    ├── 4   ← web page #4 content
    └── 5   ← web page #5 content
```

My goal was to make each of these projects appear as a *file*, rather than as a folder, and to open in Crystal automatically when it is double-clicked on:

![A project](/assets/2023/custom-file-icons-and-folder-icons/crystalproj.png)<br/>
*Looks and behaves like a file, but is secretly a folder!*


## Icons in macOS

On macOS it's easy to get projects to behave the way I wanted. It's actually common on macOS for certain types of folders - called [bundles] - to behave like files. For example apps on macOS are themselves stored as bundles with the `.app` extension.

To tell macOS that folders ending with `.crystalproj` are bundles I added the following to Crystal's `Info.plist` file, which is included in all macOS applications:

```xml
<key>CFBundleDocumentTypes</key>
<array>
    <dict>
        <key>CFBundleTypeExtensions</key>
        <array>
            <string>crystalproj</string>
        </array>
        <key>CFBundleTypeIconFile</key>
        <string>DocIconMac.icns</string>
        <key>CFBundleTypeName</key>
        <string>Crystal Project</string>
        <key>CFBundleTypeRole</key>
        <string>Editor</string>
        <key>LSTypeIsPackage</key>
        <true/>
    </dict>
</array>
```

The important parts of this `Info.plist` are:

* CFBundleTypeExtensions = ['crystalproj']
    * Defines the extension used to recognize a project
* LSTypeIsPackage = true
    * Says that a project is a bundle and therefore should be treated as a file even though it is a folder
* CFBundleTypeIconFile = "DocIconMac.icns"
    * Defines the name of the `.icns` icon file to use for a project

Setting the app icon requires similar changes to the `Info.plist`:

```
<key>CFBundleIconFile</key>
<string>AppIconMac.icns</string>
```

Simple.

## Icons in Windows

On Windows there is no concept of a "bundle". However it is possible to give a folder a custom icon by putting [a specially crafted `desktop.ini` file](https://learn.microsoft.com/en-us/windows/win32/shell/how-to-customize-folders-with-desktop-ini) inside of it:

```console
$ cat xkcd.crystalproj/desktop.ini
[.ShellClassInfo]
DirectoryClass=crystalproj
ConfirmFileOp=0
IconFile=icons\docicon.ico
IconIndex=0
InfoTip=Crystal Project
```

<img alt="Diagram showing how to customize a folder's icon on Windows with desktop.ini" src="/assets/2023/custom-file-icons-and-folder-icons/windows-customize-folder-icon.png" style="max-width: 100%" />

It's even possible to [tell Windows to open Crystal when the folder is double-clicked on](https://learn.microsoft.com/en-us/windows/win32/shell/context-menu-handlers#implementing-custom-verbs-for-folders-through-desktopini) by setting some registry keys:

<img alt="Diagram showing how to customize a folder's open action on Windows with registry keys and desktop.ini" src="/assets/2023/custom-file-icons-and-folder-icons/windows-customize-folder-open.png" style="max-width: 100%" />

<img alt="Reference explaining how to customize a folder's open action on Windows with registry keys and desktop.ini" src="/assets/2023/custom-file-icons-and-folder-icons/windows-customize-folder-open-reference.png" style="max-width: 100%; border: .5px solid black;" />

However it's still possible to navigate inside of a such a folder, notably from Open and Save dialogs, so we need another way to open projects in those contexts. My solution was to add a special "opener" file inside of a project folder which could be used to open the enclosing project:

<img alt=".crystalproj folder containing a .crystalopen opener file" src="/assets/2023/custom-file-icons-and-folder-icons/crystalproj-contents.png" style="max-width: 488px" />

Of course that `.crystalopen` file itself needs an icon. Again you can set some registry keys to tell Windows about this new file extension and its associated icon:

<img alt="Diagram showing how to customize a file's icon on Windows with registry keys" src="/assets/2023/custom-file-icons-and-folder-icons/windows-customize-file-icon.png" style="max-width: 100%" />

And if a `.crystalopen` file is double-clicked we want it to open Crystal, which can be configured with more registry keys:

<img alt="Diagram showing how to customize a file's open action on Windows with registry keys" src="/assets/2023/custom-file-icons-and-folder-icons/windows-customize-file-open.png" style="max-width: 100%" />

All of these registry keys should be [set by the installer for the app](https://github.com/davidfstr/Crystal-Web-Archiver/blob/147adc7bea1fa8d278258e75be3e51fd26892bfa/setup/win-installer.iss#L13-L54). 

## Icons in Linux

Oh Linux... Icons for files, folders, and apps are displayed by the **desktop environment**, and multiple such desktop environments exist for Linux. The most common ones (in 2023) seem to be **GNOME 3** and **KDE**, but there's also xfce, MATE (GNOME 2), and Budgie, among others. Most of these desktop environments strive to implement the [Freedesktop Specifications](https://specifications.freedesktop.org/) for defining file types & icons, but with varying degrees of compatibility.

According to the [Icon Theme Specification], which is one of the Freedesktop Specifications, an application developer *should* be able to install icons for file types to <!-- known locations in --> a special "hicolor" theme which all other themes must eventually inherit from. But there are some problems:

* [GNOME doesn't seem to implement theme inheritance correctly](https://askubuntu.com/questions/52138/how-do-i-change-the-icon-for-a-particular-file-type/752316#752316), so icons installed in the "hicolor" theme aren't picked up by other themes. So instead of installing there I wrote a script that [installed icons to every theme on the user's system](https://github.com/davidfstr/Crystal-Web-Archiver/blob/147adc7bea1fa8d278258e75be3e51fd26892bfa/src/crystal/install.py#L107-L230). [Nobody on StackOverflow](https://askubuntu.com/questions/1486524/how-to-set-the-icon-for-a-file-extension-in-a-portable-way-without-sudo) has been able to find a better solution so far.
* GNOME stores custom icon references for folders in [the GIO database](https://askubuntu.com/a/1235178/1724736) but KDE (and the Freedesktop Specification) use [.directory files](https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html).
* GNOME has not one but *two* GIO attributes for storing custom icon references, and not all programs recognize both of them:
    * The `metadata::custom-icon-name` key references the name of an icon installed to a theme.
        * However the Desktop Icons GNOME Shell Extension, which is responsible for displaying icons on the desktop, does not understand this key!
    * The `metadata::custom-icon` key references a single icon file.
        * All programs in GNOME seem to understand this kind of key so long as you use an absolute `file://` URL rather than an absolute or relative file path.
* Some programs only recognize PNG icons and other programs only recognize SVG icons, so [you must install both PNG and SVG versions of each icon](https://github.com/davidfstr/Crystal-Web-Archiver/blob/147adc7bea1fa8d278258e75be3e51fd26892bfa/src/crystal/install.py#L144-L151).
    * In particular some programs in KDE only seem to recognize SVG icons even though the [Icon Theme Specification] implies that support for PNG icons is mandatory.
    * GNOME by contrast seems to prefer PNG icons.
    * If you started with only a raster version of an icon, as I did, you'll have to vectorize the icon to make it an SVG. I had some success using the [Adobe Express PNG to SVG converter tool](https://github.com/davidfstr/Crystal-Web-Archiver/blob/147adc7bea1fa8d278258e75be3e51fd26892bfa/src/crystal/resources/application-vnd.crystal.opener.svg-README.txt#L4-L11) to make an initial conversion and [Inkscape](https://inkscape.org/) for touching it up.
* Some programs don't notice new icons immediately after installing them.
    * KDE's desktop, [Plasma, must be restarted](https://github.com/davidfstr/Crystal-Web-Archiver/blob/147adc7bea1fa8d278258e75be3e51fd26892bfa/src/crystal/install.py#L232-L261) before it notices new icons.
    * KDE's file manager Dolphin doesn't seem to notice new icons until it is restarted. Unfortunately I haven't found a safe way to restart Dolphin without losing information about the windows and tabs it has open.
* Some programs - notably Open and Save dialogs - aren't able to scale icons to the size they expect, so [you must provide prescaled versions of each icon](https://github.com/davidfstr/Crystal-Web-Archiver/blob/147adc7bea1fa8d278258e75be3e51fd26892bfa/src/crystal/install.py#L264-L288).
    * Scaling SVG icons isn't particularly straightforward, but I managed to do so with the [rconvert-svg tool](https://github.com/davidfstr/Crystal-Web-Archiver/blob/147adc7bea1fa8d278258e75be3e51fd26892bfa/src/crystal/resources/application-vnd.crystal.opener.svg-README.txt#L17).
* Icons for apps on the desktop don't show up correctly in GNOME unless you [set the `metadata::trusted` GIO attribute on it](https://github.com/davidfstr/Crystal-Web-Archiver/blob/147adc7bea1fa8d278258e75be3e51fd26892bfa/src/crystal/install.py#L84-L97).
* There are probably even more issues in desktop environments other than GNOME 3 and KDE, but I did not test any additional desktop environments.

In short, my experience in getting icons to work in Linux has been a big poorly-documented mess. But after 2 weeks I did succeed!

## Conclusions

When creating a desktop application for end users it's important to get icons for your app and its documents configured correctly to provide a good user experience, but it getting those configurations correct can be challenging.

I'd like to file bugs on several Linux desktop environments so that future Linux application developers don't have such a hard time getting icons setup, but right now I just don't have the energy. Hopefully at least this blog post will help other Linux developers configure icons more quickly.

[website downloader, Crystal]: /projects/crystal-web-archiver/
[bundles]: https://en.wikipedia.org/wiki/Bundle_(macOS)
[Icon Theme Specification]: https://specifications.freedesktop.org/icon-theme-spec/icon-theme-spec-latest.html