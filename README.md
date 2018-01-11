# SAM PRM Generator

This repository contains a simple script that can be used to generate PRM Files.

## Requirements

This script is meant to run under Python 2.7+ and Python 3.5+. It uses 
the following libraries:

* `argparser`
* `astropy > 2`
* `datetime`

You may install these libraries on your system or install them within 
a Python Virtual Environment. The easiest way to install a library is using 
the `pip` command available in modern systems:

    $ pip install $PACKAGE
    
This will install the PACKAGE in your system or inside your Virtual 
Environment. For more details, please refer to the 
[PIP Documentation](https://pip.pypa.io/en/stable/reference/pip_install/).

## Install

Since the PRM Generator is a single script, there is no need to 
install it. Simply copy and paste it wherever you want. Remember 
that you may have to add permission to execute the file if you want 
to run it as script (using `chmod a+x sam_prm_generator.py`).

## Run

Please be sure that the script has permission to be executed. 
If not, just give the permission by following the instructions 
on [Install](#Install). 

The script needs the follwoing parameters:
* File name of the list of targets;
* Year at the beginning of observing night;
* Month (as integer) at the beginning of the observing night;
* Day at the beginning of the observing night;
* UT time at the beginning of the observing night with the format HH:MM:SS;
* UT time at the end of the observing night with the format HH:MM:SS

Here is an example:

    $ ./prepare_PRM_file.py list_of_targets.txt 2018 12 25 23:00:00 09:00:00


