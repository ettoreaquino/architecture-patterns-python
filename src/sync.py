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
#     ABSTRACTION 1:     A function that just does I/O                        #
# =========================================================================== #
def read_paths_and_hashes(root):
    hashes = {}
    for folder, _, files in os.walk(root):
        for fn in files:
            hashes[hash_file(Path(folder) / fn)] = fn
    return hashes


# =========================================================================== #
#     ABSTRACTION 2:     A function that handles business logic               #
# =========================================================================== #
def determine_actions(src_hashes, dst_hashes, src_folder, dst_folder):
    for sha, filename in src_hashes.items():
        if sha not in dst_hashes:
            sourcepath = Path(src_folder) / filename
            destpath = Path(dst_folder) / filename
            yield 'copy', sourcepath, destpath

        elif dst_hashes[sha] != filename:
            olddestpath = Path(dst_folder) / dst_hashes[sha]
            newdestpath = Path(dst_folder) / filename
            yield 'move', olddestpath, newdestpath

    for sha, filename in dst_hashes.items():
        if sha not in src_hashes:
            yield 'delete', dst_folder / filename

# =========================================================================== #
#                             BUSINESS LOGIC                                  #
# =========================================================================== #
def sync(source, dest):
    # imperative shell step 1, gather inputs
    source_hashes = read_paths_and_hashes(source)  
    dest_hashes = read_paths_and_hashes(dest)  

    # step 2: call functional core
    actions = determine_actions(source_hashes, dest_hashes, source, dest)  

    # imperative shell step 3, apply outputs
    for action, *paths in actions:
        if action == 'copy':
            shutil.copyfile(*paths)
        if action == 'move':
            shutil.move(*paths)
        if action == 'delete':
            os.remove(paths[0])