# PHI-Masker: Protected Health Information (PHI) Masker


## Digital Object Identifier (DOI)



## Introduction
------------

This software masks Protected Health Information (PHI) in documents that have been 
previously annotated with Brat. It replaces the span of text of the annotations by 
the label assigned to that span. For instance, it replaces a common name annotation
by the label PERSON or the name of a city by CITY.


Additionally, it is possible to use a mask file to provide custom sustitution masks
for the Brat labels. See `Custom Masking` below for more detailed information.


## Prerequisites
-------------

This software requires to have Python 3 installed on your system.


## Directory structure
-------------------

<pre>
custom_masks/
This folder contains the text files defined custom label-mask substitutions. See 
`Custom Masking` below for more detailed information. 

input/
This folder contains the original corpus in plain text format. These files must have
be stored with `.txt` suffix.

tagged/
This folder contains the annotation files in Brat annotation format. These files must 
be stored with `.ann` suffix.

output/
Default folder to store the output masked files, with `.txt` suffix.
</pre> 


## Usage
-----

It is possible to configure the behavior of this software using the different options.

  - The `input`, `tagged`, and `output` folder options allow to change the default folders.
  
  - `Verbose` and `quiet` options allows to control the verbosity level of the software.
  
  - `Custom Masking` option allows to provide a file with custom label-mask substitutions.
  See `Custom Masking` below for more detailed information.


The user can select the different options using the command line:

	python masker.py [options] 

Options:
<pre>
-h, --help            show this help message and exit
-i INPUT_DIR, --input_dir INPUT_DIR	Folder with the original input files
-t TAGGED_DIR, --tagged_dir TAGGED_DIR	Folder with Brat annotation files
-o OUTPUT_DIR, --output_dir OUTPUT_DIR	Folder to store the output masked files
-c CUSTOM_FILE, --custom_file CUSTOM_FILE	Path to file with custom masks for annotations
-co, --custom-only	Use only labels in custom masks file
-v, --verbose         Increase output verbosity (not allowed with argument -q/--quiet)
-q, --quiet           Do not print anything (not allowed with argument -v/--verbose)
</pre>


## Examples
--------

<pre>
$ python masker.py -h
$ python masker.py --help
$ python masker.py -c custom_masks/ehr-clinic.txt 
$ python masker.py -c custom_masks/ehr-clinic.txt --custom-only
$ python masker.py -i ../MyCorpus/EHR-docs/original/ -t ../MyCorpus/EHR-docs/Brat-annotations/ -v
</pre>


## Custom Masking
------

In some cases the user may need to use masks that are different to the labels used in Brat. Moreover, 
PHI annotation may be annotated together with other type or annotation. To handle that scenarios, 
`PHI-masker` allows the user to use a file to define que label you want to substitute. User can provide
these custom mask files to mask some text span with mask that are not the label used in brat.

The custom mask file is a TSV file with key-value structure. The first column is the entity label used 
in Brat, and the second column is the mask that is going to be used to mask the span of the annotation.
This is an example of a custom mask file:

<pre>
NAME	XXXXX
CITY	LOCATION
COUNTRY	LOCATION
</pre> 

If `--custom-only` option is selected, `PHI-masker` will mask only the labels that are present in the
custom masks file. Otherwise, `PHI-masker` will mask all the annotations in the `.ann`, but changing
the masks by the ones in the custom masks files (if defined in the file, otherwise it will use the 
original Brat label).

## Contact
------

Aitor Gonzalez-Agirre (aitor.gonzalez@bsc.es)


## License
-------

Copyright (c) 2017-2018 Secretaría de Estado para el Avance Digital (SEAD)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

