#!/usr/bin/env python

import os
import argparse

version = "0.1"


def walker(dirname, files = []):
    """
    Recursively walk `dirname` and find files' creation time. Produces a list of tuples like:

    [
      (1507555345.7189517, '/some/src/path', 'filename.txt'),
      (1507555344.7189517, '/other/src/path', 'filename.dat'),
      etc
    ]
    """
    for dirpath, dirnames, filenames in os.walk(dirname):
        for filename in filenames:
            if not os.path.islink(os.path.join(dirpath, filename)):
                st = os.stat(os.path.join(dirpath, filename))
                files.append( (st.st_ctime, dirpath, filename) )
    return files


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Make symlinks to latest files")
    parser.add_argument('-n,--nr',
                        metavar='NR_OF_LINKS',
                        dest='nr_of_links',
                        type=int,
                        default=20,
                        help='Number of symlinks to create')
    parser.add_argument(metavar='dst',
                        dest='dst',
                        type=str,
                        default=None,
                        help='Dir in which to create symlinks')
    parser.add_argument(metavar='srcs',
                        dest='srcs',
                        default=[],
                        nargs="*",
                        help='Source dir(s) to recursively scan')
    args = parser.parse_args()

    # Recursively get all files and their mtimes for all dirs
    files = []
    for dirname in args.srcs:
        walker(dirname, files)
    files.sort(reverse=True)

    # Clean dest dir of old symlinks
    for filename in os.listdir(args.dst):
        path = os.path.join(args.dst, filename)
        if os.path.islink(path):
            os.unlink(os.path.join(args.dst, filename))

    # Create new symlinks
    for nr, file in enumerate(files[0:args.nr_of_links]):
        ctime = file[0]
        dirname = file[1]
        filename = file[2]
        dst_fname = os.path.join(args.dst, '%05i - %s' % (nr, filename))
        os.symlink(os.path.join(dirname, filename), dst_fname)
