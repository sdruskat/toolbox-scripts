This script parses a Toolbox text file, and extracts information pertaining to the genre and synopsis of documents, which is then written into a CSV file.

# How to use

Make sure you have Python 2 installed (run `python --version`). This script has been developed against version **2.7.12**.

### Go to the directory where the Toolbox text files are located.

E.g., `cd ~/home/user/toolbox-corpus`

### Run the script

`python parse-genre-syn.py`

### When prompted, provide the markers for documents (default: \id), genre (default: \gn), and synopsis (default: \syn)

    Please type the marker used for documents [\id]: doc<Enter>
    Please type the marker used for genre [\gn]: <Enter>
    Please type the marker used for synopsis [\syn]: <Enter>
    
### If you run into an error/exception, please [report it](https://github.com/sdruskat/toolbox-scripts/issues)!

### Your working directory will now contain a CSV file for each Toolbox file

E.g., `toolbox-file.txt` and `toolbox-file.csv`

### Open the CSV file with a spreadsheet application (e.g., [LibreOffice Calc](http://www.libreoffice.org/discover/calc/))

Use the dollar sign (`$`) as a delimiter, and deselect all other delimiters. Also deselect **Merge delimiters**.

If your `\id`s are numerical and start with `0`, set the **ID** column to *Text* format to keep prefixed `0`s.
