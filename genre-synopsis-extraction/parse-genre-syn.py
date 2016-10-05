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

# Create an output directory, which is the sibling
# of the current working directory,
# called "genre-synopsis-extraction"
cwd = os.path.dirname(os.getcwd())
par = os.path.dirname(cwd)
outdir = os.path.join(par, "analysis", "genre-synopsis-extraction")
if not os.path.exists(outdir):
    os.makedirs(outdir)

# Compile the name of the output file
outfilename = cwd.rsplit(os.path.sep, 1)[1] + ".csv"

# Create the var and header for the CSV file
outcsv = "File$ID$Genre$Synopsis"

# Numer of occurrences of the \syn marker, for sanity check
syn_occ = 0

# Go through all files in the current workin directory
for f in os.listdir(os.getcwd()):

    # Open the file
    with open(f) as fi:
        doc = ""
        syn = " "
        gen = " "
        concat_to = ""

        print "\n##########\n\nProcessing", f
        # For each line in the file
        for line in fi:
            # Clear any trailing whitespaces
            line.strip()
            # Convert any line breaks to Unix (\n)
            line = line.replace('\r\n', '\n')
            line = line.replace('\r', '\n')

            # The next line is always a candidate for concatenation (i.e.,
            # it might contain content that could belong to the line before),
            # so check if it starts with a backslash, and if it does not,
            # concatenate the string variable of the line before with
            # the contents of this line, else, reset the variable.
            if not (line.startswith("\\") or line.startswith("\n")):
                if concat_to == "gen":
                    gen = gen + " " + line.replace("\n", " ")
                elif concat_to == "syn":
                    syn = syn + " " + line.replace("\n", " ")
                elif concat_to == "id":
                    doc = doc + " " + line.replace("\n", " ")
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
                    gen = " "
                    syn = " "
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
        # At this point, check whether the contents of doc, gen, and syn have
        # already been written to outcsv, as it will not have happened if the
        # file only contained one single \id.
        index_last_lb = outcsv.rfind("\n")
        if outcsv[index_last_lb:] != "%s$%s$%s$%s" % (f, doc, gen, syn):
            if doc != "" and (syn != " " or gen != " "):
                outcsv = "%s\n%s$%s$%s$%s" % (outcsv, f, doc, gen, syn)
                gen = " "
                syn = " "
        # Quick sanity check
        # NOTE: Not reliable (No. of \id with just
        # either \syn or \gn may differ)
        syn_occ += open(f).read().count("\%s" % syn_m)
        if syn_occ == outcsv.count("\n"):
            print "Sanity check passed"
        print "Finished processing", f

# Write the CSV string to file
out_file = open(os.path.join(outdir, outfilename), 'w')
out_file.write(outcsv)
print "\n#####\n\nDone!"
print "Filename:", outdir + os.path.sep + outfilename

print ("In order to open the file with a spreadsheet application,"
       "use the dollar sign ('$') as separator.\n")
