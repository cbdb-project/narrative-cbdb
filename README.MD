# Narrative CBDB

Create narrative biographies by using CBDB sqlite database

## Usage

1. Download [CBDB sqlite](https://huggingface.co/datasets/cbdb/cbdb-sqlite/blob/main/latest.7z) database

2. Uncompress the sqlite database

3. Rename the uncompressed database as cbdb.db and put it to the root of this project directory

4. Run 1 na-cbdb-chn-short-sentences.py to get the text file

5. Run 2 remove-zero-none-chn.py to clean the result. You will get the text like [this](https://github.com/cbdb-project/narrative-cbdb/blob/main/sample-result-chn.txt)

If you want to sperate output to small files, after getting output.txt, please run split-data.py

## Sample result

https://github.com/cbdb-project/narrative-cbdb/blob/main/sample-result.txt

## License
Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license
