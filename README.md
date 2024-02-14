# CSE6242-Group-Project

`pull_data.py`

Requires python 3.x (tested on 3.9) with pandas

Contains a function, `get_data`, which we can use to pull Federal Housing Finance Agency data into a pandas dataframe. 

Currently only works for single family home data found in "National File A" (URL: https://www.fhfa.gov/DataTools/Downloads/Pages/Single-Family-Mortgage-Level-Owner-Occupied-1-Unit-Property-(National-File-A).aspx)

Example usage:

```
python3 pull_data.py

         enterprise_flag  record_num  ...  num_units  affordability
0                      1           1  ...          1              4
1                      1           2  ...          1              4
2                      1           3  ...          1              4
3                      1           4  ...          1              1
4                      1           5  ...          1              4
...                  ...         ...  ...        ...            ...
1864257                1     1864258  ...          1              4
1864258                1     1864259  ...          1              4
1864259                1     1864260  ...          1              4
1864260                1     1864261  ...          1              4
1864261                1     1864262  ...          1              4

[1864262 rows x 15 columns]

```
