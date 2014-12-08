from __future__ import print_function

import os
import sys
import shutil

from hashlib import sha256
import pickle

import diff_match_patch

patched_files = {}

def copy_file(fpath, dest_root):
    src_dir = os.path.split(fpath)[0]
    dest_dir = os.path.join(dest_root, src_dir)
    shutil.copy(fpath, dest_dir)

def apply_diff(fpath, dest_root):
    dest_file = os.path.join(dest_root, os.path.splitext(fpath)[0]) + ".txt"

    with file(dest_file, 'r') as fi:
        h = sha256(fi.read()).hexdigest()
        if h == patched_files.get(fpath):
            print('Already applied: %s' % fpath)
            return

    dmp = diff_match_patch.diff_match_patch()
    patches = []
    orig_text = None

    with file(fpath, 'r') as fi:
        patches = dmp.patch_fromText(fi.read())

    with file(dest_file, 'r') as fi:
        orig_text = fi.read()

    patched_text, rvals = dmp.patch_apply(patches, orig_text)
    for rv in rvals:
        if not rv:
            raise Exception('Patch failed: %s' % fpath)

    with file(dest_file, 'w') as fout:
        fout.write(patched_text)
    patched_files[fpath] = sha256(patched_text).hexdigest()

def do_patch(patch_name, dest):
    os.chdir(patch_name)
    try:
        with file('patched_files.pickle', 'r') as fi:
            global patched_files
            patched_files = pickle.load(fi)
    except IOError:
        pass

    for root, dirs, files in os.walk('.'):
        for fn in files:
            fpath = os.path.join(root, fn)
            ext = os.path.splitext(fn)[1].lower()
            if ext in ('.txt', '.lua'):
                copy_file(fpath, dest)
            elif ext in ('.diff', '.patch'):
                apply_diff(fpath, dest)

    with file('patched_files.pickle', 'w') as fi:
        pickle.dump(patched_files, fi, 0)
    os.chdir('..')

def main():
    if len(sys.argv) < 3:
        print('Usage: %s <patch name> <Dwarf Fortress directory>' % sys.argv[0])
        return

    patch_dir = sys.argv[1]
    if not os.path.isdir(patch_dir):
        print('Patch not found: %s' % patch_dir)
        return

    dest = sys.argv[2]
    dest_raw = os.path.join(dest, 'raw')
    if not os.path.isdir(dest_raw):
        print('Raw directory not found: %s' % dest_raw)
        return

    do_patch(patch_dir, dest)


if __name__ == '__main__':
    main()
