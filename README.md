# nda-extractor
Extracts data from Neware binary files (.nda)

Run it with ./binary2csv.py (path to input file) (path to output file)

Planned functions:
  * Header metadata extraction
  * Data column finalizing (use for the last 5 bytes?)
  * Variable outputs (database, json, etc.)
  * Graphing and analysis (using numpy)

## Notes about headers
0000:0000-0000:0070 = Software id and date with some other stuff

0000:0070-0000:008D = MTI hardware version?

0000:008E-0000:07F0 = blank/padding

0000:0800-0000:082D = Machine and channel identification of some kind. 
    - 0000:082C and 0000:0800 appear to be channel id.(08, 06, 03, etc)
    - 0000:082B appears to be machine id.
    - The rest might be a serial number. 

0000:084E-0000:0860 = date and time.  format : YYYY.MM.DD HH:MM:SS

0000:0876-0000:08FD = User and cycling id.

0000:08FD-0000:08FF = Data Start marker
