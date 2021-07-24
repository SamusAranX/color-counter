#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from os.path import exists, basename
from PIL import Image, ImageSequence, UnidentifiedImageError

def int_to_rgba(i):
	a =  i & 255
	b = (i >> 8) & 255
	g = (i >> 16) & 255
	r = (i >> 24) & 255
	return (r, g, b, a)

def rgba_to_int(r, g, b, a=255):
	return (r<<24) + (g<<16) + (b<<8) + a

def int_to_rgb(i):
	b =  i & 255
	g = (i >> 8) & 255
	r = (i >> 16) & 255
	return (r, g, b)

def rgb_to_int(r, g, b):
	return (r<<16) + (g<<8) + b

def supports_truecolor():
	colorterm = os.environ.get("COLORTERM")
	return colorterm == "truecolor"

def count_colors(img_path, count_transparent=False):
	colors_dict = {}
	num_frames = 0
	try:
		with Image.open(img_path) as img:
			for frame in ImageSequence.Iterator(img):
				num_frames += 1
				w, h = frame.size
				pix = frame.convert("RGBA").load()

				for y in range(h):
					for x in range(w):
						r, g, b, a = pix[x, y]

						if count_transparent:
							i = rgba_to_int(r, g, b, a)
						else:
							if a < 128:
								continue

							i = rgb_to_int(r, g, b)

						if i in colors_dict:
							colors_dict[i] += 1
						else:
							colors_dict[i] = 1
	except UnidentifiedImageError:
		print(f"{img_path}: can't open file")
		return None, 0

	return colors_dict, num_frames

def main(args):
	colors_dict = {}

	first_item = True

	for path in args.input:
		if first_item:
			first_item = False
		else:
			print()

		colors_dict, num_frames = count_colors(path)
		if not colors_dict:
			continue

		if not args.verbose:
			if num_frames > 1:
				print(f"{path}: {len(colors_dict)} colors in {num_frames} frames")
			else:
				print(f"{path}: {len(colors_dict)} colors")
		else:
			print(f"{path}:")
			sorted_colors = sorted(colors_dict, key=colors_dict.get, reverse=True)
			for col in sorted_colors:
				amounts = colors_dict[col]
				r, g, b = int_to_rgb(col)
				print(f"#{r:02X}{g:02X}{b:02X}: {amounts}×")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Automate ffmpeg stuff")
	parser.add_argument("input", metavar="input", type=str, nargs="+", help="Image file(s)")
	parser.add_argument("-t", "--include-transparency", action="store_true", help="Count 100% transparency as a color")
	parser.add_argument("-v", "--verbose", action="store_true", help="List all colors, sorted by number of occurrences")
	args = parser.parse_args()
	main(args)