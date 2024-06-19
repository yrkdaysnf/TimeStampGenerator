from datetime import datetime
from subprocess import Popen, call
from os import path, name, listdir, remove


def open_folder(out):
    if path.exists(out):
        if name == 'nt':Popen(f'explorer "{out}"')# Windows
        elif name == 'posix':  # macOS or Linux
            if call(['which', 'xdg-open']) == 0:Popen(['xdg-open', out])
            elif call(['which', 'open']) == 0:Popen(['open', out])

def get_creation_date(file_path):
    time = path.getmtime(file_path)
    date = datetime.fromtimestamp(time)
    return date.strftime('%d.%m.%Y'), date.strftime('%H:%M:%S')

def get_fonts():
    fonts = []
    for filename in listdir(path.join('assets', 'fonts')):
        if filename.endswith(('.ttf','.otf')):
            fonts.append(filename)
    return fonts

def cleantmp():
    all_files = listdir()
    for f in all_files:
        file_without_extension = path.splitext(f)[0]
        if "TEMP_MPY_wvf_snd" in file_without_extension:
            remove(f)