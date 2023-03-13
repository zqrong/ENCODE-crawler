# ENCODE-crawler

A python script to crawl the ENCODE project files metadata with given targets (like epigenomic features) and cell lines. This script will try to crawl all files with any combination of the targets and the cell lines.

## How to use

1. Enter the targets you want to query in `targets.txt`, one target per line (Existing records in this file are just examples, feel free to delete them, as well as the following `celllines.txt`).
2. Enter the cell lines you want to query in `celllines.txt`, one cell line per line.
3. Run the script by `python3 crawl.py`. You will see the progress bars.
4. When finished, the results will be saved to `results.csv`.

## Contact
[Ziqi Rong](https://www.zqrong.com) ([ziqirong@umich.edu](mailto:ziqirong.umich.edu))