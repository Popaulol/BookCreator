# Book Creator

This thing converts a PDF File of A4 Pages to one that can be used with double sided printing to create an A5 booklet.

The UI, whilst horrid, should be self explanatory.

If the Input PDF isn't A4, your results may vary.
A PDF that only contains DIN A Paper sizes *should* work with the Output file having the same Page size as the Input File but I can't guarantee that.
Any other Paper formats and it's most likely gonna break horribly. 

## Setup
1. Install [Python](https://www.python.org/)
2. Install PyPDF2:

This does depend on your system Setup but
```
pip install PyPDF2
```
*Should* work on Winshit, CrackOS and some Linux Distros.
If this doesn't work on your system, you can probably figure out how to install something from [PyPI](https://pypi.org/) on your system yourself.


# Running
```
python3 main.py
```

If that doesn't work your system, go figure it out yourself.
