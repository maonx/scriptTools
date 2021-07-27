#!/usr/bin/env python3
# This script use to print image file
# which path you set silently.
# Test successful on Windows 10

import os, time
import sys

import win32print
import win32ui
import win32con
from PIL import Image, ImageWin

def print_image(file_name):
    #
    # Constants for GetDeviceCaps
    #
    #
    # HORZRES / VERTRES = printable area
    #
    HORZRES = win32con.HORZRES
    VERTRES = win32con.VERTRES

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
    path_to_watch = sys.argv[1] if len(sys.argv) > 1 else '.'
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    try:
        while True:
            time.sleep (1)
            after = dict ([(f, None) for f in os.listdir (path_to_watch)])
            added = [f for f in after if not f in before]
            removed = [f for f in before if not f in after]
            if added:
                for i in added:
                    print("Added: %s" % i)
                    print_image(os.path.join(path_to_watch,i))
            if removed: print("Removed: ", ", ".join (removed))
            before = after
    except KeyboardInterrupt:
        sys.exit(1)
