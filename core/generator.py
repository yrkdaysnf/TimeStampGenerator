from datetime import datetime, timedelta
from os import path
from random import randint as rint
from json import load
from tempfile import gettempdir

from proglog import ProgressBarLogger
from moviepy.editor import VideoFileClip
from PIL import Image, ImageDraw, ImageFont
from numpy import array as ar

class progress_logger(ProgressBarLogger):
    def __init__(self, stop_event, update_progress):
        super().__init__()
        self.stop_event = stop_event
        self.update_progress = update_progress

    def bars_callback(self, bar, attr, value, old_value=None):
        if self.stop_event.is_set():
            raise Exception("Processing stoped by user")
        percentage = value / self.bars[bar]['total']
        if bar == 't':
            self.update_progress(percentage)

def video(getframe, t):
    global start_time, twitch

    frame = getframe(t)
    pil_frame = Image.fromarray(frame)

    current_time = start_time + timedelta(seconds=int(t))
    
    return ar(add_text_to_frame(pil_frame, current_time))

def add_text_to_frame(frame, current_time):
    global month_names, text_color, font_name
    width, height = frame.size
    
    month = month_names[current_time.month - 1]
    if use_month_names:
        date = current_time.strftime(f'%d {month}. %Y')
    else:
        date = current_time.strftime(f'%d/%m/%Y')

    time = current_time.strftime('%H:%M:%S')

    text_image1 = Image.new('RGBA', (width, height), (0,0,0,0))
    text_image2 = Image.new('RGBA', (width, height), (0,0,0,0))
    draw1 = ImageDraw.Draw(text_image1)
    draw2 = ImageDraw.Draw(text_image2)

    font = ImageFont.truetype(path.join('assets', 'fonts', font_name), text_size)
    stroke = int(text_size/15)

    _, _, text_w1, text_h1 = draw1.textbbox((0,0), time, font)
    _, _, text_w2, text_h2 = draw2.textbbox((0,0), date, font)

    pos, align = position.split()
    text_pos1 = [0,0]
    text_pos2 = [0,0]

    text_pos1[0] = offset if align == 'Left' else width - text_w1 - offset
    text_pos2[0] = offset if align == 'Left' else width - text_w2 - offset

    text_pos1[1] = height - 2.5*text_h1 - offset if pos == 'Bottom' else 1.5*text_h1 + offset
    text_pos2[1] = height - text_h2 - offset if pos == 'Bottom' else offset

    draw1.text(tuple(text_pos1), time, font=font, fill=text_color, align=align, spacing=1, 
              stroke_width = stroke, stroke_fill=(0,0,0))
    
    draw2.text(tuple(text_pos2), date, font=font, fill=text_color, align=align, spacing=1, 
              stroke_width = stroke, stroke_fill=(0,0,0))

    r1, r2 = rint(-2,2)/10, rint(-2,2)/10

    if twitch:
        text_image1 = text_image1.transform(text_image1.size, Image.AFFINE,
                                            (1, 0, r1, 0, 1, r2), Image.BILINEAR)
        text_image2 = text_image2.transform(text_image2.size, Image.AFFINE, 
                                            (1, 0, r2, 0, 1, r1), Image.BILINEAR)
    
    text_image = Image.alpha_composite(text_image1, text_image2)

    if aberration:
        r, g, b, a = text_image.split()
        r = r.transform(r.size, Image.AFFINE, 
                        (1, 0, 0.2*stroke, 0, 1, 0.2*stroke), Image.BILINEAR)
        g = g.transform(g.size, Image.AFFINE,
                        (1, 0, -0.2*stroke, 0, 1, 0.2*stroke), Image.BILINEAR)

        text_image = Image.merge("RGBA", (r, g, b, a))

    frame.paste(text_image, (0,0), text_image)

    return frame

def timestamp(filename, details, output, update_progress, stop_event, jsonpath):
    global twitch, offset, aberration, use_month_names, position, text_color, font_name, text_size
    global start_time, month_names

    with open(jsonpath, 'r') as file:
            settings = load(file)

    month_names = ['JAN', 'FEB',
                   'MAR', 'APR', 'MAY',
                   'JUN', 'JUL', 'AUG',
                   'SEP', 'OCT', 'NOV',
                   'DEC']

    text_color = settings['timestamp']['user']['text_color']
    twitch = settings['timestamp']['user']['twitch']
    font_name = settings['timestamp']['user']['font']
    use_month_names = settings['timestamp']['user']['use_month_names']
    position = settings['timestamp']['user']['position']
    aberration = settings['timestamp']['user']['aberration']
    offset = settings['timestamp']['user']['offset']
    text_size = settings['timestamp']['user']['text_size']
    output_path = path.join(output, f'{filename.split(".")[0]}-timestamped')
    
    date = details[1]
    time = details[2]

    if int(time.split(':')[-1]) == 0:
        parts = time.split(':')
        parts[2] = f'{rint(0,59):02}'
        time = ':'.join(parts)

    start_time = datetime.strptime(date+' '+time, '%d.%m.%Y %H:%M:%S')

    if filename.split(".")[-1] in ['jpg', 'png', 'jpeg']:
        img = Image.open(details[0])
        output_img = add_text_to_frame(img, start_time)
        output_img.save(f'{output_path}.png')
        update_progress(1)

    else:
        clip = VideoFileClip(details[0])
        output_clip = clip.fl(video)
        output_clip.write_videofile(
                                    f'{output_path}.mp4', 
                                    codec = 'libx264',
                                    audio_codec = 'aac',
                                    logger=progress_logger(stop_event, update_progress),
                                    threads = 4
                                    )