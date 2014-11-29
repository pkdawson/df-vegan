from __future__ import print_function

import os
import sys
import shutil

import diff_match_patch

def copy_file(fpath, dest_root):
    src_dir = os.path.split(fpath)[0]
    dest_dir = os.path.join(dest_root, src_dir)
    shutil.copy(fpath, dest_dir)

def apply_diff(fpath, dest_root):
    dest_file = os.path.join(dest_root, os.path.splitext(fpath)[0]) + ".txt"
    print(dest_file)

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


def main():
    if len(sys.argv) < 2:
        print('Usage: %s <path of Dwarf Fortress>' % sys.argv[0])
        return

    dest = sys.argv[1]
    dest_raw = os.path.join(dest, 'raw')
    if not os.path.isdir(dest_raw):
        print('Raw directory not found: %s' % dest_raw)
        return

    for root, dirs, files in os.walk('raw'):
        for fn in files:
            fpath = os.path.join(root, fn)
            ext = os.path.splitext(fn)[1].lower()
            if ext in ('.txt'):
                copy_file(fpath, dest)
            elif ext in ('.diff', '.patch'):
                apply_diff(fpath, dest)

if __name__ == '__main__':
    main()
