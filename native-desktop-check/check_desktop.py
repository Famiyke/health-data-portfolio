"""Open the supplied workbook in its native Windows desktop application.

The report is evidence from actual windows. A started process alone does not
count as a passed test. Power BI's loaded data is checked separately by DAX.
"""
import argparse
import base64
import json
import os
from pathlib import Path
import subprocess
import time

from PIL import ImageGrab
from pywinauto import Desktop
import win32api
import win32con
import win32gui


def improve_resolution():
    try:
        modes = []
        i = 0
        while True:
            try:
                mode = win32api.EnumDisplaySettings(None, i)
            except Exception:
                break
            if mode.PelsWidth >= 1440 and mode.PelsHeight >= 900 and mode.BitsPerPel >= 24:
                modes.append(mode)
            i += 1
        if modes:
            mode = min(modes, key=lambda m: abs(m.PelsWidth - 1600) + abs(m.PelsHeight - 900))
            print('Display mode change:', win32api.ChangeDisplaySettings(mode, 0), flush=True)
    except Exception as exc:
        print('Display modes unavailable:', str(exc), flush=True)
    print('Display resolution:', win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1), flush=True)


def titles():
    windows = []
    def collect(handle, _):
        if win32gui.IsWindowVisible(handle):
            title = win32gui.GetWindowText(handle)
            if title:
                windows.append((handle, title))
    win32gui.EnumWindows(collect, None)
    return windows


def window_controls(handle):
    try:
        window = Desktop(backend='uia').window(handle=handle)
        controls = window.descendants()
        return window, [(control, control.element_info.name or '', control.element_info.control_type) for control in controls]
    except Exception as exc:
        print('Accessibility scan:', str(exc)[:240], flush=True)
        return None, []


def capture(handle, output, filename):
    win32gui.ShowWindow(handle, win32con.SW_MAXIMIZE)
    try:
        win32gui.SetForegroundWindow(handle)
    except Exception:
        pass
    time.sleep(2)
    left, top, right, bottom = win32gui.GetWindowRect(handle)
    bbox = (max(0, left), max(0, top), min(right, win32api.GetSystemMetrics(0)), min(bottom, win32api.GetSystemMetrics(1)))
    frame = ImageGrab.grab(bbox=bbox)
    dest = output / (filename + '.png')
    frame.save(dest)
    return str(dest)


def read_controls(handle, output, filename):
    _, controls = window_controls(handle)
    records = [{'name': name, 'type': kind} for _, name, kind in controls if name]
    (output / (filename + '.json')).write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding='utf-8')
    print('Visible names:', json.dumps(records[:90], ensure_ascii=False), flush=True)
    return controls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--kind', choices=['powerbi', 'tableau'], required=True)
    parser.add_argument('--exe', type=Path, required=True)
    parser.add_argument('--file', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    improve_resolution()
    expected = 'Workforce' if args.kind == 'powerbi' else 'Retail Sales Forecasting'
    pages = (
        ['Vacancy rates by industry (%)', 'Health and social assistance vacancy rate (%)', 'Offered wages by industry (CAD/hour)', 'Hospital overtime hours (% of regular + overtime)', 'Paid hospital sick leave hours per FTE', 'Registered nurses per 100,000 residents']
        if args.kind == 'powerbi' else
        ['Retail Sales Forecasting', 'Canada actual and forecast sales (CAD billions)', 'Manitoba actual and forecast sales (CAD billions)', 'Regional sales · Sep 2026 (CAD billions)', 'Canada model accuracy · holdout WAPE (%)']
    )
    proc = subprocess.Popen([str(args.exe), str(args.file.resolve())])
    print('Started native executable:', args.exe, 'PID', proc.pid, flush=True)
    end = time.monotonic() + 210
    previous = None
    handle = None
    while time.monotonic() < end:
        found = titles()
        if found != previous:
            print('Top-level windows:', found, flush=True)
            previous = found
        candidates = [(h, title) for h, title in found if expected.casefold() in title.casefold()]
        if candidates:
            handle = candidates[0][0]
            break
        # A first-launch configuration panel may expose an explicit "Skip" or
        # "Not now" button; these are ordinary dismissal options.
        for h, title in found:
            if (args.kind == 'powerbi' and 'power bi' in title.lower()) or (args.kind == 'tableau' and 'tableau' in title.lower()):
                _, controls = window_controls(h)
                for control, name, kind in controls:
                    if kind == 'Button' and name.strip().lower() in ('skip', 'not now', 'maybe later', 'skip for now', 'close welcome screen'):
                        try:
                            control.click_input()
                            print('Dismissed optional welcome panel:', name, flush=True)
                            break
                        except Exception:
                            pass
        time.sleep(4)
    status = {'kind': args.kind, 'expected_title': expected, 'title_opened': bool(handle), 'pages_selected': [], 'refresh_clicked': False, 'windows': titles()}
    if handle is None:
        print('Expected workbook title was not observed.', flush=True)
        app_words = ('power bi', 'tableau')
        for h, title in titles():
            if any(word in title.lower() for word in app_words):
                try:
                    capture(h, args.output, 'opening-state')
                    read_controls(h, args.output, 'opening-state-controls')
                except Exception as exc:
                    print('Capture failed:', str(exc), flush=True)
                break
        (args.output/'ui-status.json').write_text(json.dumps(status, indent=2), encoding='utf-8')
        return 2
    print('Opened expected workbook window:', win32gui.GetWindowText(handle), flush=True)
    capture(handle, args.output, 'initial-workbook')
    controls = read_controls(handle, args.output, 'initial-controls')
    if args.kind == 'powerbi':
        refresh = [(c, n) for c, n, kind in controls if n.strip().casefold() == 'refresh' and kind == 'Button']
        if refresh:
            try:
                refresh[0][0].click_input()
                status['refresh_clicked'] = True
                print('Clicked Power BI Desktop Refresh', flush=True)
                time.sleep(15)
            except Exception as exc:
                print('Refresh control did not respond:', str(exc)[:200], flush=True)
    for i, name in enumerate(pages, 1):
        _, controls = window_controls(handle)
        candidates = [(c, kind) for c, n, kind in controls if n.strip().casefold() == name.casefold()]
        for control, kind in candidates:
            if kind in ('TabItem','Button','ListItem','Text','Pane'):
                try:
                    control.click_input()
                    time.sleep(3)
                    capture(handle, args.output, f'page-{i}')
                    status['pages_selected'].append(name)
                    print('Selected page or sheet:', name, flush=True)
                    break
                except Exception as exc:
                    print('Could not select', name, str(exc)[:100], flush=True)
    last = capture(handle, args.output, 'final-workbook')
    read_controls(handle, args.output, 'final-controls')
    status['windows'] = titles()
    (args.output/'ui-status.json').write_text(json.dumps(status, indent=2), encoding='utf-8')
    print('UI evidence:', json.dumps(status, ensure_ascii=False), flush=True)
    # Leave the app running for the Power BI model query.
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
