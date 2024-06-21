# TimeStamp Generator
<p align='center'>
    <img src="readme_assets\head.png">
</p>

**TimeStamp Generator** -  free, *open-source* application tailored for those looking to add a touch of *vintage* to their videos or images. While not all cameras have the capability to embed timestamps, this application allows you to overlay timestamps onto their media, enhancing the *retro aesthetic*. It’s perfect for creators and enthusiasts who appreciate the classic look of dated footage, providing an *authentic* timestamp that can transform modern recordings into *nostalgic* masterpieces. You can select the *font, color, position, and other settings* to ensure the timestamp perfectly complements your media.

>Any assistance in the development of the project is accepted. In particular, code optimization, project assembly (as far as possible), tests and bug detection.
## Example of TimeStamp
<p align='center'>
    <img src="readme_assets\example.gif" width="786">
</p>

## Installation and running app (Windows)
```powershell
# poetry
poetry install
poetry run python main.py
```
```powershell
# pip
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
You can also unzip the zip archive of the current version of the application from the [releases](https://github.com/yrkdaysnf/timestampgenerator/releases) and run `.exe` file.
## Using
1. Select one or more media files. 
2. If necessary, using the buttons around to the media name, change the date and time, or delete the media from the queue.
3. Click the green button in the lower right corner of the application.
4. Done! 

To customize timestamp, go to settings by clicking on the button in the lower left corner of the application.

### Settings
<p align='center'>
    <img src="readme_assets\settings.png">
</p>

* **Output folder** - The folder for saving the generation results.
  * By default - `Videos\TimeStamps` folder in the user's home directory your OS.
  * You can choose another output folder.
  * You can enable the opening of this folder after generation. It is enabled by default.
* **Font** - The font for the timestamp text.
  * By default - *vcrosdmonorus_vhsicons.ttf* font.
  * You can add and use any font, to do this, copy it to the `assets\fonts` folder, which is located in the program directory.
* **Position on frame** - The position of the timestamp in the frame.
  * You can choose from 4 positions:
    * *Top Left*
    * *Bottom Left*
    * *Top Right*
    * *Bottom Right*
  * By default - *Bottom Right*
* **Text color** - Timestamp text color.
  * By default - Vintage yellow color <span style="background-color:BLACK;color:#FFD94F">(<b>#FFD94F</b>)</span>.
  * Use a color picker to select a different color.
  * The outline is not customized and is always black.
* **Text size** - Timestamp text size.
  * By default - *24*
  * It is selected individually for the media.
* **Offset** - The distance for the timestamp from the edges.
  * By default - *20*
* **Effects and view** - Timestamp display Options.
  * *Twitch* - Shaking the timestamp. Disabled by default.
  * *Month in letters* - Writing the month in letters. Enabled by default.
  * *Aberration* - Distorts the timestamp colors by shifting the color channels. Enabled by default.

### Speed test
* Input
  * Resolution - *720x576*
  * Duration - *12 seconds*
* Speed processing
  * Only timestamp - *4 seconds*
  * With aberration - *8 seconds*
  * With twitch - *12 seconds*
  * With aberration and twitch - *16 seconds*

## To-Do
- [ ] Test on Linux
- [ ] Custom format for timestamp
- [ ] Testing other videoformats
