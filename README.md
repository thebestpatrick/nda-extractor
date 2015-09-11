# nda-extractor
Extracts data from Neware binary files (.nda)

bin2csv.py: Library functions to allow for the easy converting of binary .nda files (from Neware/MTI) into easy to process csv files.  Can be run from the command line as well, with `./bin2csv.py [binary file] [output csv]`

graph.py: Library functions to allow for the easy graphing of data in the output csv format.

reportgenerator.py: Combines bin2csv and graph to generate a full report, with (somewhat limited) metadata extracted as well.  Can be used as a library, or called from the command line.  Right now, when called with `./reportgenerator.py [binary file]` it will create a directory called 'reports/' and then write the full report into that.

## Planned functions:
  * Header metadata extraction.  Partly done, no time zone info or mass info. Time zone does not appear to be in there anywhere though.
  * Data column finalizing.  'step_name' just needs a few more cases.
  * Directory extraction: Allowing for a full directory to be tracked 'live', generating new reports as changes occur, while skipping unchanged files.

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
