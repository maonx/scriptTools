#!/usr/bin/env python3

from watchdog.observers import Observer
from watchdog.events import *
import time
import sys
import imghdr

import win32print
import win32ui
from PIL import Image, ImageWin

class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))
            print_image(event.src_path)

def print_image(file_name):
    #
    # Constants for GetDeviceCaps
    #
    #
    # HORZRES / VERTRES = printable area
    #
    HORZRES = 8
    VERTRES = 10
    #
    # LOGPIXELS = dots per inch
    #
    LOGPIXELSX = 88
    LOGPIXELSY = 90
    #
    # PHYSICALWIDTH/HEIGHT = total area
    #
    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111
    #
    # PHYSICALOFFSETX/Y = left / top margin
    #
    PHYSICALOFFSETX = 112
    PHYSICALOFFSETY = 113

    printer_name = win32print.GetDefaultPrinter ()

    #
    # You can only write a Device-independent bitmap
    # directly to a Windows device context; therefore
    # we need (for ease) to use the Python Imaging
    # Library to manipulate the image.
    #
    # Create a device context from a named printer
    # and assess the printable size of the paper.
    #
    hDC = win32ui.CreateDC ()
    hDC.CreatePrinterDC (printer_name)
    printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
    printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
    printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)

    #
    # Open the image, rotate it if it's wider than
    # it is high, and work out how much to multiply
    # each pixel by to get it as big as possible on
    # the page without distorting.
    #
    try:
        bmp = Image.open (file_name)
        if bmp.size[0] > bmp.size[1]:
            bmp = bmp.transpose (Image.ROTATE_90)

        ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
        scale = min (ratios)

        #
        # Start the print job, and draw the bitmap to
        # the printer device at the scaled size.
        #
        hDC.StartDoc (file_name)
        hDC.StartPage ()

        dib = ImageWin.Dib (bmp)
        scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
        x1 = int ((printable_area[0] - scaled_width) / 2)
        y1 = int ((printable_area[1] - scaled_height) / 2)
        x2 = x1 + scaled_width
        y2 = y1 + scaled_height
        dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))

        hDC.EndPage ()
        hDC.EndDoc ()
        hDC.DeleteDC ()
    except IOError:
        print("This file %s is not a image file!" % file_name)

if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    observer.schedule(event_handler, path, True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
