---
layout: project
title: MediaQueue
x_aka: OmniQueue
summary: >
    A system for tracking and searching for media items
    (movies, TV series, anime, books) in various different
    media sources.
started_on: 2015-01-02
ended_on: 2015-01-06
x_languages: [Google_Apps_Script]
x_lines_of_code: 819
x_location: "Google Docs > Media Queue Latest - David Foster"

full_width: true

style: |
    .img-right { float: right; margin-left: 0.5em; }
    
    /* Override Bootstrap rule that conflicts with carousel */
    #screenshots img { max-width: none; }

carousels: true
script: |
    // Display carousel
    $(window).load(function() {
        $('#screenshots').orbit({ bullets: true });
    });

---

MediaQueue allows you to write down media that you want to watch - movies, TV series, books, etc. - and helps you to quickly locate the media for streaming, download, pickup, or purchase.

MediaQueue is implemented as a Google Docs spreadsheet with custom macros that search for media items entered into the sheet.

<div style="margin-bottom: 3em;">
    <div id="screenshots">
        <img src="/assets/2015/media-queue/screen1.png" width="750" height="525" />
        <img src="/assets/2015/media-queue/screen2.png" width="750" height="525" />
        <img src="/assets/2015/media-queue/screen3.png" width="750" height="525" />
    </div>
</div>

### Supported Media Sources

* Netflix - Stream source for everything
* KissAnime - Stream source for Anime (`A`)
* The Pirate Bay - Download source for everything
* BakaBT - Download source for Anime (`A`)
* Seattle Public Library - Pickup source for everything
* Barnes & Noble - Pickup source for Books (`B`)
* Amazon - Buy source for everything

{% capture toc_content %}

* [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)

{% endcapture %}

<div class="toc">
  {{ toc_content | markdownify }}
</div>

<a id="installation"></a>
## Installation

1. Open the spreadsheet:
   
   <a class="btn btn-primary" target="_new" href="https://docs.google.com/spreadsheets/d/1heViK7cdeo3AdjvUP7oGoP5lVPzH9MLQw_CVS8GCnIo/edit#gid=0">Open in Google Docs</a>

2. If you're not already logged in to Google, click the **SIGN IN** link in
   the top-right corner.

3. From the **File** menu select **Make a copy**:
   
   ![Menu: File > Make a copy](steps/install-copy.png)

4. From the **MediaQueue** menu select **Settings...**:
   
   ![Menu: MediaQueue > Settings...](steps/install-settings.png)
   
5. Confirm the authorization prompt:
   
   ![Authorization prompt](steps/install-authorize.png)
   
   This will take you to the settings page, which you can leave blank for now.
   
4. Again, from the **MediaQueue** menu select **Settings...**:
   
   ![Menu: MediaQueue > Settings...](steps/install-settings.png)
   
   This will take you back to the Queue sheet.

5. From the **Tools** menu select **Script editor...**:
   
   ![Menu: Tools > Script editor...](steps/install-open-editor.png)
   
   The script editor will appear in a new tab.

6. From the **Resources** menu select **Current project's triggers**:
   
   ![Menu: Resources > Current project's triggers](steps/install-show-triggers.png)
   
   An empty trigger box will appear:
   
   ![Empty trigger box](steps/install-empty-triggers.png)

7. Configure a new edit trigger with the following settings:
   
   ![Edit trigger settings](steps/install-edit-trigger.png)
   
8. Click "Save" to dismiss the trigger box.

9. Close the current script editor tab. This will take you back to the Queue sheet:

   ![Back on the Queue sheet](steps/install-queue-sheet.png)

<a id="usage"></a>
## Usage

### 1. Add an item

<img title="Insert a row" src="steps/usage-add.png" class="img-right"/>

To insert a new media item in the queue, insert a new row and type the item name and the item type. Providing a correct item type helps MediaQueue search more relevant media sources in the next step.

Media types currently recognized by the **Type** column include:

* `A` = Anime
* `M` = Movie
* `B` = Book

Multiple types can be specified by separating with commas. For example `M,A` refers to an anime movie.

It's okay to use other ad-hoc media types not in this list. They will be ignored. If a media item contains no recognized media type, only a generic set of media sources that are widely applicable will be searched.

<br style="clear: both;"/>
### 2. Search for an item

To search for a media item in various media sources, locate the row containing the media item and the gray-colored column that corresponds to the type of media sources you want to search. For example if you wanted to find a stream to watch a media item, you would choose the **Stream** column.

1. Type a period (`.`) in the cell for the row and column you identified. This will summon a new sheet and initiate a search for the media item in various media sources. 

   <img title="Type period into appropriate cell" src="steps/usage-search.png"/>

2. Once the search is complete select a search result by typing the number of your choice into the yellow cell.

   <img title="Type choice into yellow cell" src="steps/usage-results.png"/>

3. The selected choice will be substituted back into the cell that you initially typed a period into.

   <img title="Choice substituted back on Queue sheet" src="steps/usage-done.png"/>

### Tips

By default the name of the media item is used as the search query when searching media sources. If you want to use an alternate search query then type a period followed by the desired search query when summoning the search sheet. For example you could type `.azumanga daioh` to specifically search for "azumanga daioh".

<a id="contributing"></a>
## Contributing

I'd love to hear from you if you make extensions to this program.
<a href="/contact/">Send me an email</a>.

<a class="btn btn-primary" target="_new" href="https://gist.github.com/davidfstr/0f212ddf160b2f776884">
    Browse Source Code
</a>

Adding support for new media sources would be especially welcome:

### Desired Media Sources

* Wikipedia - Info source for everything
* Google - Info source for everything
* THEM Anime - Info source for Anime (`A`)
* Anime Planet - Info source for Anime (`A`)
* Rotten Tomatoes - Info source for Movies (`M`)
* IMDB - Info source for Movies (`M`)
* NyaaTorrents - Download source for Anime (`A`)
* iTunes Store - Buy source for everything