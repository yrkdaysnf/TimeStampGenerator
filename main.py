from os import path, makedirs
from json import load, dump
import threading
from time import sleep

import flet as ft
from flet_contrib.color_picker import ColorPicker

from core.generator import timestamp
from core.util import get_creation_date, open_folder, get_fonts, cleantmp

jsonpath = path.join('assets','settings.json')
with open(jsonpath, 'r') as file:
        settings = load(file)

output = settings.get('output_folder') or path.join(path.expanduser('~'),'Videos','TimeStamps')

bg_color = settings['interface']['bg_color']
text_color = settings['interface']['text_color']
main_color = settings['interface']['main_color']

selected_files = {}

def main(page: ft.Page):
    page.title = 'TimeStampGenerator'
    page.theme = ft.theme.Theme(color_scheme_seed = main_color)
    page.window_width = 800
    page.window_height = 600
    page.window_min_width = 800
    page.window_min_height = 600
    page.bgcolor = bg_color

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            for f in e.files:
                if f.name not in selected_files:
                    dt = get_creation_date(f.path)
                    selected_files[f.name] = [f.path, dt[0], dt[1]]
            update_list_view()

    def delete_file(filename):
        del selected_files[filename]
        update_list_view()

    def pick_date(filename):
        def save_date(e):
            selected_files[filename][1] = date_picker.value.strftime("%d.%m.%Y")
            update_list_view()  
        date_picker.pick_date()
        date_picker.on_change = save_date
    
    def pick_time(filename):
        def save_time(e):
            selected_files[filename][2] = time_picker.value.strftime("%H:%M:%S")
            update_list_view()  
        time_picker.pick_time()
        time_picker.on_change = save_time


    def update_list_view():
        listofvideos.content = list_view
        list_view.controls.clear()
        for filename, details in selected_files.items():
            filename_short = filename[:30] + '...' if len(filename) > 33 else filename
            list_view.controls.append(
                ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    bgcolor=ft.colors.SURFACE,
                                    icon_color=ft.colors.SURFACE_TINT,
                                    on_click=lambda e, f=filename: delete_file(f)
                                ),
                                ft.Text(
                                    value=filename_short,
                                    color=ft.colors.ON_SECONDARY,
                                    weight=ft.FontWeight.BOLD
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text=details[1],
                                    icon=ft.icons.CALENDAR_MONTH,
                                    width= 150,
                                    on_click=lambda e, f=filename: pick_date(f)
                                ),
                                ft.ElevatedButton(
                                    text = details[2],
                                    icon = ft.icons.TIMER,
                                    width = 150,
                                    on_click = lambda e, f = filename: pick_time(f)
                                )
                            ]
                        )
                    ],
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                )
            )
        if len(list_view.controls) != 0:
            generatetime.disabled = False
            generatetime.bgcolor = '#93ff91'
            generatetime.tooltip = "Start generating TimeStamp's"
        else: 
            generatetime.disabled = True
            generatetime.bgcolor = ft.colors.GREY_50
            generatetime.tooltip = 'Select files before generation'
            listofvideos.content = tip
        page.update()

    def open_settings(e):
        global folder_s, settings, output
        
        def back(e):
            page.overlay.pop()
            page.update()

        def save(e):
            global output
            page.snack_bar = ft.SnackBar(ft.Text("Saved!"), duration = 500)

            if folder_s.value == path.join(path.expanduser('~'),'Videos','TimeStamps'):
                output = path.join(path.expanduser('~'),'Videos','TimeStamps')
                settings["output_folder"] = None
            else:
                output = folder_s.value
                settings["output_folder"] = folder_s.value

            settings["open_folder"] = open_s.value
            settings["timestamp"]["user"]["font"] = font_s.value
            settings["timestamp"]["user"]["text_color"] = color_s.value
            settings["timestamp"]["user"]["use_month_names"] = word_month_s.value
            settings["timestamp"]["user"]["twitch"] = twitch_s.value
            settings["timestamp"]["user"]["text_size"] = int(size_s.value)
            settings["timestamp"]["user"]["offset"] = int(offset_s.value)
            settings["timestamp"]["user"]["aberration"] = aberration_s.value
            settings["timestamp"]["user"]["position"] = position_s.value

            output_info.value = f'Output folder: {output}'

            with open(jsonpath, 'w') as file:
                dump(settings, file, indent = 4)

            page.snack_bar.open = True
            page.update()

        def default(e):
            folder_s.value = path.join(path.expanduser('~'),'Videos','TimeStamps')
            open_s.value = True
            font_s.value = settings["timestamp"]["default"]["font"]
            color_s.value = settings["timestamp"]["default"]["text_color"]
            color_s.color = settings["timestamp"]["default"]["text_color"]
            word_month_s.value = settings["timestamp"]["default"]["use_month_names"]
            twitch_s.value = settings["timestamp"]["default"]["twitch"]
            size_s.value = settings["timestamp"]["default"]["text_size"]
            offset_s.value = settings["timestamp"]["default"]["offset"]
            aberration_s.value = settings["timestamp"]["default"]["aberration"]
            position_s.value = settings["timestamp"]["default"]["position"]
            page.update()

        def open_color_picker(e):
            e.control.page.dialog = d
            d.open = True
            e.control.page.update()

        def open_fonts_folder(e):open_folder(path.join('assets', 'fonts'))

        color_icon = ft.IconButton(icon = ft.icons.BRUSH, on_click = open_color_picker)
        back_button = ft.IconButton(icon = ft.icons.ARROW_BACK, on_click = back)
        save_button = ft.IconButton(icon = ft.icons.SAVE, on_click = save)
        to_default_button = ft.TextButton('Return to the default settings', on_click = default)
        folderpick = ft.IconButton(
            icon = ft.icons.FOLDER, 
            on_click = lambda _: get_directory_dialog.get_directory_path(),
            tooltip = 'Select the output directory'
        )
        folderlook = ft.IconButton(
            icon = ft.icons.FOLDER, 
            on_click = open_fonts_folder,
            tooltip = 'Open the font directory'
        )

        folder_s = ft.TextField(label = 'Output Folder',
                                value = output, read_only = True)
        open_s = ft.Checkbox(label = "Open after processing", value = settings["open_folder"])

        font_s = ft.Dropdown(label = "Font", 
                            value = settings["timestamp"]["user"]["font"])
        for font in get_fonts():font_s.options.append(ft.dropdown.Option(font))

        color_s = ft.TextField(label = "Text color",
                                         color = settings["timestamp"]["user"]["text_color"],
                                         value = settings["timestamp"]["user"]["text_color"],
                                         autofocus = False,
                                         read_only = True)
        
        size_s = ft.TextField(label = "Text size", width = 90, 
                               input_filter = ft.NumbersOnlyInputFilter(),
                               text_align = ft.TextAlign.CENTER,
                               value = settings["timestamp"]["user"]["text_size"])
        
        offset_s = ft.TextField(label = "Offset", width = 90,
                                input_filter = ft.NumbersOnlyInputFilter(),
                                text_align = ft.TextAlign.CENTER,
                                value = settings["timestamp"]["user"]["offset"])
        
        word_month_s = ft.Checkbox(label = "Month in letters",
                                     value = settings["timestamp"]["user"]["use_month_names"])
        twitch_s = ft.Checkbox(label="Twitch",
                             value = settings["timestamp"]["user"]["twitch"])
        aberration_s = ft.Checkbox(label = "Aberration",
                                 value = settings["timestamp"]["user"]["aberration"])
        position_s = ft.Dropdown(label = "Position on frame",
                                 width = 190,
                                 value = settings["timestamp"]["user"]["position"],
                                 options =
                                 [
                                    ft.dropdown.Option('Top Left'),
                                    ft.dropdown.Option('Bottom Left'),
                                    ft.dropdown.Option('Top Right'),
                                    ft.dropdown.Option('Bottom Right')
                                 ])
    

        color_picker = ColorPicker(color=color_s.value, width=300)

        def change_color(e):
            color_s.value = color_picker.color
            color_s.color = color_picker.color
            d.open = False
            e.control.page.update()

        def close_dialog(e):
            d.open = False
            d.update()

        d = ft.AlertDialog(
            content = color_picker,
            actions = [
                ft.TextButton("OK", on_click = change_color),
                ft.TextButton("Cancel", on_click = close_dialog),
            ],
            actions_alignment = ft.MainAxisAlignment.END,
            on_dismiss = close_dialog,
        )

        overlay = ft.Container(
            ft.Container(
                ft.Column(
                    controls=
                    [
                        ft.Row(
                            [
                                back_button, to_default_button, save_button
                            ],
                            alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Container(
                            ft.ListView(
                                controls = 
                                [
                                    ft.Divider(),
                                    ft.Row([folderpick, folder_s, open_s]),
                                    ft.Row([folderlook, font_s, position_s]),
                                    ft.Row([color_icon, color_s, size_s, offset_s]),
                                    ft.Row([twitch_s, word_month_s, aberration_s],
                                           alignment = ft.MainAxisAlignment.SPACE_AROUND)
                                ],
                                spacing = 10,
                            )
                        )
                    ],
                    expand = True,
                    scroll = ft.ScrollMode.HIDDEN
                ),
                width = 600,
                border_radius = 15,
                margin = 20,
                padding = 20,
                bgcolor = ft.colors.ON_SECONDARY
            ),
            alignment = ft.alignment.center,
            expand = True,
            blur = 5
        )
        page.overlay.append(overlay)
        page.update()
    
    def get_directory_result(e: ft.FilePickerResultEvent):
        global folder_s
        if e.path:
            folder_s.value = e.path
            page.update()

    def generate(e):
        def stop_processing(e):
            stop_event.set()
            progress_percent.content = ft.Icon(name=ft.icons.CANCEL)
            cancel_button.disabled = True
            page.update()
            sleep(2)
            page.overlay.pop()
            page.update()
            stop_event.clear()
            cleantmp()
            return None

        def update_progress(progress):
            progress_ring.value = step*(i+progress)
            progress_percent_text.value = f'{int(step*(i+progress)*100)}%'
            page.update()

        stop_event = threading.Event()

        if not path.exists(output):makedirs(output)
        
        progress = 0
        step = 1/len(selected_files)

        progress_percent_text = ft.Text(f'{progress}%', text_align = ft.TextAlign.CENTER)

        progress_percent = ft.Container(progress_percent_text, alignment = ft.alignment.center)
        
        progress_text = ft.Text(f'0 / {len(selected_files)}')

        cancel_button = ft.ElevatedButton(
            'Cancel', 
            bgcolor = ft.colors.ERROR,
            color = ft.colors.ON_ERROR,
            on_click = stop_processing
        )

        progress_ring = ft.ProgressRing(
            stroke_width = 8,
            width = 80,
            height = 80
        )

        overlay = ft.Container(
            content = ft.Container(
                content = ft.Column(
                    controls = 
                    [
                        ft.Stack(
                            controls = 
                            [
                                progress_ring,
                                progress_percent                     
                            ],
                            width = 80,
                            height = 80
                        ),
                        progress_text,
                        cancel_button                        
                    ],
                    alignment = ft.MainAxisAlignment.CENTER,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER
                ),
                width = 200,
                height = 200,
                border_radius=15,
                bgcolor = ft.colors.ON_SECONDARY
            ),
            blur = 5,
            alignment = ft.alignment.center
        )
        page.overlay.append(overlay)
        page.update()

        for i, (filename, details) in enumerate(selected_files.items()):
            progress_text.value = f'{i+1} / {len(selected_files)}'
            page.update()
            timestamp(filename, details, output, update_progress, stop_event, jsonpath)

        progress_percent.content = ft.Icon(name=ft.icons.CHECK_CIRCLE)
        cancel_button.disabled = True
        page.update()
        sleep(2)
        page.overlay.pop()
        page.update()
        if settings["open_folder"]: open_folder(output)

    files_pick = ft.Container(
        content = ft.Column(
            expand = True,
            controls = [
                ft.Icon(name = ft.icons.UPLOAD, color = '#7078ff', size = 50),
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        ),
        alignment = ft.alignment.center,
        bgcolor = main_color,
        padding = 10,
        border_radius = 15,
        ink = True,
        on_click = lambda _: pick_files_dialog.pick_files(
            file_type = 'CUSTOM', 
            allowed_extensions = ['png','mp4','mpv', 'mod','jpg','jpeg'],
            allow_multiple = True)
    )

    date_picker = ft.DatePicker()
    page.overlay.append(date_picker)

    time_picker = ft.TimePicker()
    page.overlay.append(time_picker)

    pick_files_dialog = ft.FilePicker(on_result = pick_files_result)
    page.overlay.append(pick_files_dialog)

    get_directory_dialog = ft.FilePicker(on_result = get_directory_result)
    page.overlay.append(get_directory_dialog)

    tip = ft.Column(
        controls =
        [
            ft.Text
            (
                "It's empty\nSelect videos or images",
                color = text_color,
                size = 30,
                weight = ft.FontWeight.BOLD,
                text_align = ft.TextAlign.CENTER
            ),
            ft.Text(
                "Supported formats: mp4, mod, mov, png, jpg, jpeg",
                color = text_color, 
                size = 15, 
                italic = True
            )
        ],
        alignment = ft.MainAxisAlignment.CENTER,
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        opacity = 0.75
    )

    list_view = ft.ListView(spacing = 10, padding = 10)

    listofvideos = ft.Container(
        content = tip,
        expand = True,
        border_radius = 15,
        border = ft.Border(top = ft.BorderSide(1, text_color),
                           bottom = ft.BorderSide(1, text_color)),
        alignment = ft.alignment.center
    )

    settings_button = ft.IconButton(
        icon = ft.icons.SETTINGS, 
        icon_color = '#7078ff',
        bgcolor = main_color,
        on_click = open_settings,
        tooltip = 'Settings'
    )
    
    generatetime = ft.IconButton(
        icon = ft.icons.KEYBOARD_ARROW_RIGHT_ROUNDED,
        icon_color = text_color,
        bgcolor = ft.colors.GREY_50,
        on_click = generate,
        disabled = True,
        tooltip = 'Select files before generation'
    )
    
    output_info = ft.Text(
        value = f'Output folder: {output}', 
        color = text_color,
        italic = True
    )

    page.add(
        ft.Column(
            controls=[
                files_pick,
                listofvideos,
                ft.Row(
                    controls = 
                    [
                        settings_button,
                        output_info,
                        generatetime
                    ],
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ], 
            expand=True,
        )
    )

ft.app(target=main, assets_dir="assets", name='TimeStampGenerator')