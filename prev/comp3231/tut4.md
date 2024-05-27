<!-- SPDX-License-Identifier: zlib-acknowledgement -->
FAT saves on random access, as has pointers to all file blocks in RAM
FAT backups required

inode (improves from FAT as only has open files in RAM and can quickly lookup file content as don't have to search for file in FAT)
open_files[n][blocks]
open[1][3]
