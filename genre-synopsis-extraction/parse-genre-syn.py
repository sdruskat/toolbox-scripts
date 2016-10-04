#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
# Copyright 2016 Humboldt-Universität zu Berlin
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

# This script parses a Toolbox text file,
# and extracts information pertaining to the genre and synopsis
# of documents, which is then written into a CSV file.

import os

# Prompt the user for the needed markers
doc_m = raw_input("Please type the marker used for documents [\\id]: ") or "id"
gen_m = raw_input("Please type the marker used for genre [\\gn]: ") or "gn"
syn_m = raw_input("Please type the marker"
                  " used for synopsis [\\syn]: ") or "syn"

# Go through all files in the current workin directory
for f in os.listdir(os.getcwd()):

    # Create the header for the CSV file
    outcsv = "File$ID$Genre$Synopsis"

    # Open the file
    with open(f) as fi:
        doc = ""
        syn = ""
        gen = ""
        concat_to = ""

        print "Processing", f
        # For each line in the file
        for line in fi:
            # Clear any trailing whitespaces
            line = line.strip()
            # The next line is always a candidate for concatenation (i.e.,
            # it might contain content that could belong to the line before),
            # so check if it starts with a backslash, and if it does not,
            # concatenate the string variable of the line before with
            # the contents of this line, else, reset the variable.
            if not line.startswith("\\"):
                if concat_to == "gen":
                    gen = gen + " " + line
                elif concat_to == "syn":
                    syn = syn + " " + line
                elif concat_to == "id":
                    doc = doc + " " + line
            else:
                concat_to = ""
            # If the line contains the \id marker,
            # check if any of the syn and gen variable are not empty,
            # and if so, concatenate the string meant for writing to
            # CSV later with the respective values. Then, set the doc
            # string to the line sans marker.
            # If the line contains either the \gn or \syn marker,
            # set the respective variable to the line sans marker.
            if line.startswith("\\%s" % doc_m):
                if doc != "" and (syn != " " or gen != " "):
                    outcsv = "%s\n%s$%s$%s$%s" % (outcsv, f, doc, gen, syn)
                doc = line.strip()
                doc = doc[len("\\%s" % doc_m):].strip()
                concat_to = "id"
            elif line.startswith("\\%s" % gen_m):
                gen = line.strip()
                gen = gen[len("\\%s" % gen_m):].strip()
                concat_to = "gen"
            elif line.startswith("\\%s" % syn_m):
                syn = line.strip()
                syn = syn[len("\\%s" % syn_m):].strip()
                concat_to = "syn"
    print "Done, writing file"
    # Write the CSV string to file
    to_file = "%s_genre-syopsis.csv" % str(f).rsplit(".", 1)[0]
    out_file = open(to_file, 'w')
    out_file.write(outcsv)
    outcsv = ""
    print "Done writing file"
    print "Filename:", to_file

print ("In order to open the file with a spreadsheet application,"
       "use the dollar sign ('$') as separator.")
