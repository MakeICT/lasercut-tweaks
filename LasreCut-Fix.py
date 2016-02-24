# -*- coding: utf-8 -*-

# Launch lasercut software and hide the "Stop" button (which doesn't work correctly)
# Dominic Canare <dom@makeict.org>
# Written for MakeICT

import win32gui
import re
import subprocess
import time

LASERCUT_PATH = 'C:\\LaserCut53\\Lasercut53.exe'

SW_HIDE = 0

itemsToTranslate = {
	'DownLoad': 'Download',
	'Datum': 'Home',
	'Z Datum': 'Focus',
	'X+': '>',
	'X-': '<',
	'Y+': 'Λ',
	'Y-': 'V',
	'Z+': 'Bed ▲',
	'Z-': 'Bed ▼'
}

itemsToHide = ['Stop']

mainWindowHWND = None

def setText(hwnd, text):
	win32gui.SetWindowText(hwnd, text)
	win32gui.InvalidateRect(hwnd, None, False)
	
def find_lasercut_window_callback(hwnd, wildcard):
	global mainWindowHWND
	if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
		mainWindowHWND = hwnd
		
def process_controls_callback(hwnd, lparam):
	global mainWindowHWND, downloadButtonHWND

	try:
		text = win32gui.GetWindowText(hwnd)
		if text in itemsToHide:
			win32gui.ShowWindow(hwnd, SW_HIDE)
			itemsToHide.remove(text)
		elif text in itemsToTranslate:
			setText(hwnd, itemsToTranslate[text])
			itemsToTranslate.pop(text, None)
	except Exception as exc:
		print(exc)

print('Launching...')
subprocess.Popen([LASERCUT_PATH])

print('Finding main window...')
while mainWindowHWND == None:
	time.sleep(0.01)
	win32gui.EnumWindows(find_lasercut_window_callback, "Lasercut 5\\.3 .*Rabbit Laser.*")

print('Processing items...')
while len(itemsToHide) + len(itemsToTranslate) > 0:
	win32gui.EnumChildWindows(mainWindowHWND, process_controls_callback, None)

print('Done!')
