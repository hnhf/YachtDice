from os import path
import sys


def get_path(f_path):
    bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
    path_to_dat = path.join(bundle_dir, f_path)
    return path_to_dat
get_path("a")