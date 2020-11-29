import hashlib
import os
import shutil
from pathlib import Path

# =========================================================================== #
#   To detect renames, we’ll have to inspect the content of files. For this,  #
# we can use a hashing function like MD5 or SHA-1. The code to generate a     #
# SHA-1 hash from a file is simple enough:                                    #
# =========================================================================== #

BLOCSIZE = 65536

def hash_file(path):
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCSIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCSIZE)

    return hasher.hexdigest()

# =========================================================================== #
#                             BUSINESS LOGIC                                  #
# =========================================================================== #
def sync(source, dest):
    
    # Walk the source folder and build a dict of filenames and their hashes
    source_hashes = {}
    for folder, _, files in os.walk(source):
        for fn in files:
            source_hashes[hash_file(Path(folder) / fn)] = fn

    seen = set()

    # Walk the target folder and get the filenames and hashes
    for folder, _, files in os.walk(dest):
        for fn in files:
            dest_path = Path(folder) / fn
            dest_hash = hash_file(dest_path)
            seen.add(dest_hash)

            # if there is a file in target that's not in source, delete it
            if dest_hash not in source_hashes:
                dest_path.remove()

            # if there is a file in target that has a different path in source,
            # move it to the correct path
            elif dest_hash in source_hashes and fn != source_hashes[dest_hash]:
                shutil.move(dest_path, Path(folder) / source_hashes[dest_hash])


    # For every file that appears in source but not target, copy the file to,
    # the target:
    for src_hash, fn in source_hashes.items():
        if src_hash not in seen:
            shutil.copy(Path(source) / fn, Path(dest) / fn) 