#!/usr/bin/env python
#
# redebug.py
#
# Jiyong Jang, 2012
#
import argparse
import sys
import os
import time

from tqdm import tqdm

import common
import config
import old_new_funcs
import patchloader
import sourceloader
import reporter

if __name__ == '__main__':

    # parse arguments
    parser = argparse.ArgumentParser(description="Extract data from project dir")
    parser.add_argument("project", type=str, help="Path to the project dir")
    args = parser.parse_args()

    Config = config.load_config()
    start_time = time.time()
    old_new_funcs_dataset = old_new_funcs.OldNewFuncsDataset(Config.get("DEFAULT", "old_new_func_dataset_path"))
    source_path = args.project

    # initialize a magic cookie pointer
    common.verbose_print('[-] initialized magic cookie\n')

    diff_dir = os.path.join(os.getcwd(), "cache", "diff")
    if not os.path.exists(diff_dir):
        os.makedirs(diff_dir)
    # dump_patch_file_to_tmp_dir
    for vul_path, patch_path in tqdm(old_new_funcs_dataset.get_func_pairs().items()):
        diff_file = vul_path.split("/")[-1].replace("_OLD.vul", ".diff")
        sig = os.system('diff -uw "%s" "%s" > "%s"' % (vul_path, patch_path, os.path.join(diff_dir, diff_file)))

    # traverse patch files
    patch = patchloader.PatchLoader()
    npatch = patch.traverse(diff_dir)
    if npatch == 0:
        print('[!] no patch to be queried')
        sys.exit(1)

    # traverse source files
    source = sourceloader.SourceLoader()
    nmatch = source.traverse(source_path, patch)
    if nmatch == 0:
        print('[!] no match to be checked')
        sys.exit(1)

    # generate a report
    report = reporter.Reporter(patch, source)
    exact_nmatch = report.output()
    if exact_nmatch == 0:
        print('[!] no exact match found')
        sys.exit(1)

    elapsed_time = time.time() - start_time
    print '[+] %d matches given %d patches ... %.1fs' % (exact_nmatch, npatch, elapsed_time)
