# coding=utf-8
# reporter.py
#   Reporter class
#
# Jiyong Jang, 2012
#
import sys
import time
from collections import defaultdict

import common


class Reporter(object):

    def __init__(self, patch, source):
        self._patch_list = patch.items()
        self._npatch = patch.length()
        self._source_list = source.items()
        self._nsource = source.length()
        self._match_dict = source.match_items()
        self._context_dict = defaultdict(list)

    def _exact_match(self):
        '''
        Exact-matching test to catch Bloom filters errors
        '''
        print '[+] performing an exact matching test'
        start_time = time.time()
        exact_nmatch = 0

        for patch_id, source_id_list in self._match_dict.items():
            patch_norm_lines = self._patch_list[patch_id].norm_lines
            patch_norm_length = len(patch_norm_lines)
            for source_id in source_id_list:
                source_norm_lines = self._source_list[source_id].norm_lines
                source_norm_length = len(source_norm_lines)

                for i in range(0, (source_norm_length-patch_norm_length+1)):
                    patch_line = 0
                    source_line = i
                    while patch_norm_lines[patch_line] == source_norm_lines[source_line]:
                        patch_line += 1
                        source_line += 1

                        if patch_line == patch_norm_length:
                            self._context_dict[patch_id].append(common.ContextInfo(source_id, max(0, i-common.context_line), i, source_line, min(source_line+common.context_line, source_norm_length-1)))
                            exact_nmatch += 1
                            break

                        while source_line<source_norm_length-patch_norm_length and source_norm_lines[source_line]=='':
                            source_line += 1

                        if source_line == source_norm_length-patch_norm_length:
                            break

        elapsed_time = time.time() - start_time
        print '[+] %d exact matches ... %.1fs\n' % (exact_nmatch, elapsed_time)
        return exact_nmatch

    def _html_escape(self, string):
        '''
        Escape HTML
        '''
        return ''.join(common.html_escape_dict.get(c,c) for c in string)

    def output(self, outfile='vul.log'):
        '''
        Perform an exact matching test and generate a report
        '''
        exact_nmatch = self._exact_match()
        if exact_nmatch == 0:
            return exact_nmatch

        print '[+] generating vul logs'
        start_time = time.time()
        j = 0

        out = open(outfile, 'w')

        for patch_id, context_list in self._context_dict.items():
            p = self._patch_list[patch_id]

            for context in context_list:
                s = self._source_list[context.source_id]
                # source info - prev_context
                j += 1
                out.write("[NO. %d] Vulnerable found in %s, VUL: %s\n".encode("utf-8") % (j, s.file_path, p.file_path))
                sys.stdout.flush()

        out.close()

        elapsed_time = time.time() - start_time
        print '[+] \"%s\" ... %.1fs\n' % (outfile, elapsed_time)
        return exact_nmatch

