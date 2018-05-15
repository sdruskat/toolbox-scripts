#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
# Copyright 2018ff. Stephan Druskat
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#  Contributors:
#     Stephan Druskat - initial API and implementation
#############################################################################
import re
import os
from collections import defaultdict
import csv


def main():
    """
    Main method
    """
    s = "Directory containing Toolbox text files (recursively): "
    dir_str = input(s)
    s = "Name of directories that may contain Toolbox files [toolbox]: "
    toolbox_dir = input(s)
    if toolbox_dir is "":
        toolbox_dir = "toolbox"
    toolbox_ext = input("Toolbox extension [txt]: ")
    if toolbox_ext is "":
        toolbox_ext = "txt"
    candidates = retrieve_candidates(dir_str, toolbox_ext, toolbox_dir)
    marker_tuple = retrieve_markers(dir_str, candidates)
    language_markers = marker_tuple[0]
    all_markers = marker_tuple[1]
    write_csv(language_markers, all_markers)
    print(len(all_markers))
    print("Goodbye.")


def retrieve_candidates(dir_str, toolbox_ext, toolbox_dir):
    """
    Retrieve the candidate files from the given directory, recursively.

    Requirements are:
    - The path of the directory must include the toolbox_dir string
    - The file must have the toolbox_ext extension
    - The path must not contain the string "/v1/", i.e., only the "/v2/"
      versions of Toolbox files are used, iff versions exist
    """
    candidates = []
    for root, dirs, files in os.walk(dir_str):
        for file in files:
            # if file.endswith(".txt"):
            p = os.path.join(root, file)
            if "/" + toolbox_dir + "/" in p:
                if "/v1/" not in p:
                    if file.endswith("." + toolbox_ext):
                        candidates.append(p)
    return candidates


def retrieve_markers(dir_str, candidates):
    """
    Retrieve the markers from the candidate files, and save them into
    a defaultdict(set) that take the language name (retrieved from the
    root directory's first children, which must be named after the
    corpus language) as key, and a set of markers as value.
    """
    marker_dict = defaultdict(set)
    all_markers = set()
    # The marker regex: At the start of the string, match a backslash
    # then more than one Unicode word, then a string.
    marker = re.compile("^\\\\[\w\[\]_-]+\s")
    # Get the name of the parent directory
    root_split = dir_str.rsplit("/")
    parent_name = ""
    if dir_str.endswith("/"):
        parent_name = root_split[-2]
    else:
        parent_name = root_split[-1]
    # Iterate the candidates and extract the markers
    for c in candidates:
        # This assumes that the parent directory contains directories
        # named after corpus language as first children:
        # Get the index of the parent dir string in the full path string
        # then add the length of the parent name string + one for the
        # suffix "/", i.e., get the index where the directory that is
        # named after the corpus language starts.
        root_i = c.find(parent_name + "/") + len(parent_name) + 1
        # Find the first slash after the calculated index above
        post_lang_slash = c.find("/", root_i)
        # Slice the path to retrieve the directory (= language) name
        language_str = c[root_i:post_lang_slash]
        # Read files, retrieve markers and save them to the language
        # name-keyed set
        with open(c, 'r') as in_file:
            buf = in_file.readlines()
            for line in buf:
                matches = re.match(marker, line)
                if matches:
                    match = matches.group(0)[:-1]
                    all_markers.add(match)
                    marker_dict[language_str].add(match)
    return (marker_dict, all_markers)


def write_csv(markers, all_markers):
    """
    Write a CSV file with rows that contain the key of the set, i.e.,
    the language name, and a sorted list representation of the set
    containing the markers.
    """
    sorted_markers = sorted(list(all_markers))
    csv_dir = input("Directory to save the CSV file to: ")
    if not csv_dir.endswith("/"):
        csv_dir = csv_dir + "/"
    with open(os.path.join(csv_dir, 'markers.csv'), 'w') as f:
        w = csv.writer(f)
        keys = list(markers)
        for key in keys:
            # Construct a list of markers that are actually in the
            # set used for the language
            val_list = []
            for all_key in sorted_markers:
                if all_key in markers[key]:
                    val_list.append(all_key)
                else:
                    val_list.append("")
            val_list.insert(0, key)
            w.writerow(val_list)


if __name__ == '__main__':
    """
    Call main() when run as a script.
    """
    main()
