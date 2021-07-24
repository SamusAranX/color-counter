#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from os.path import exists, basename
from PIL import Image

def int_to_rgba(i):
	a =  i & 255
	b = (i >> 8) & 255
	g = (i >> 16) & 255
	r = (i >> 24) & 255
	return (r, g, b, a)

def rgba_to_int(rgba):
	r, g, b, a = rgba
	return (r<<24) + (g<<16) + (b<<8) + a

def int_to_rgb(i):
	b =  i & 255
	g = (i >> 8) & 255
	r = (i >> 16) & 255
	return (r, g, b)

def rgb_to_int(rgb):
	r, g, b = rgb
	return (r<<16) + (g<<8) + b

def supports_truecolor():
	colorterm = os.environ.get("COLORTERM")
	return colorterm == "truecolor"

def main(image_paths, verbose=False):
	colors_dict = {}

	for path in image_paths:
		if not exists(path):
			sys.exit(f"File {path} does not exist")

		with Image.open(path) as img:
			img = img.convert("RGB")
			pix = img.load()
			w, h = img.size

			for y in range(h):
				for x in range(w):
					p = pix[x, y]
					i = rgb_to_int(p)
					if i in colors_dict:
						colors_dict[i] += 1
					else:
						colors_dict[i] = 1

	if not args.verbose:
		print(len(colors_dict))
	else:
		sorted_colors = sorted(colors_dict, key=colors_dict.get)
		for col in sorted_colors:
			r, g, b = int_to_rgb(col)
			amounts = colors_dict[col]

			print(f"#{r:02X}{g:02X}{b:02X}: {amounts}×")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Automate ffmpeg stuff")
	parser.add_argument("input", metavar="input", type=str, nargs="+", help="Image file(s)")
	parser.add_argument("-v", "--verbose", action="store_true", help="List all colors, sorted by number of occurrences")
	args = parser.parse_args()