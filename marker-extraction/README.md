This script parses a directory recursively and extracts the Toolbox markers from 
the contained Toolbox files.

Requirements apply:

- The provided directory is the parent directory whose first children are 
directories named after the language of the corpora they contain.
- The path of the directory must include the toolbox_dir string
- The files to be parsed must have the toolbox_ext extension
- The path must not contain the string "/v1/", i.e., only the "/v2/"
versions of Toolbox files are used, iff versions exist (this applies to the
way the 
[MelaTAMP research project](https://wikis.hu-berlin.de/melatamp/Hauptseite) 
orders its raw data.)

# How to use

Make sure you have Python 3 installed (run `python --version`). 
This script has been developed against version **3.5.2**.

### Run the script

`python extract-markers.py`

Follow the prompts.

Open the CSV file with a spreadsheet application (e.g., 
[LibreOffice Calc](http://www.libreoffice.org/discover/calc/))