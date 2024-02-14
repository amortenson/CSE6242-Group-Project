from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import pandas as pd

def get_url(dataset, year):
    base_url = "https://www.fhfa.gov/DataTools/Downloads/Documents/Enterprise-PUDB/"

    dataset_map = {
        "Multifamily-Census": f"Multi-Family_Census_Tract_File_/{year}_MFCensusTract{year}.zip",
        "Multifamily-National": f"Multi-Family_National_File_/{year}_MFNationalFile{year}.zip",
        "Singlefamily-Census-Fannie": f"Single-Family_Census_Tract_File_/{year}_SFCensusTractFNM{year}.zip",
        "Singlefamily-Census-Freddie": f"Single-Family_Census_Tract_File_/{year}_SFCensusTractFRE{year}.zip",
        "Singlefamily-National-A-Fannie": f"National-File-A/{year}_SFNationalFileA{year}.zip",
        "Singlefamily-National-A-Freddie": f"National-File-A/{year}_SFNationalFileA{year}.zip",
        "Singlefamily-National-B-Fannie": f"National-File-B/{year}_SFNationalFileB{year}.zip",
        "Singlefamily-National-B-Freddie": f"National-File-B/{year}_SFNationalFileB{year}.zip",
        "Singlefamily-National-C-Fannie": f"National-File-C/{year}_SFNationalFileC{year}.zip",
        "Singlefamily-National-C-Freddie": f"National-File-C/{year}_SFNationalFileC{year}.zip"
    }

    return base_url + dataset_map.get(dataset)


def get_data(dataset, year):
    # the name of the file within the downloaded zip file
    file_map = {
        "Singlefamily-Census-Freddie": f"fhlmc_sf{year}c_loans.txt",
        "Singlefamily-National-A-Fannie": f"fnma_sf{year}a_loans.txt",
        "Singlefamily-National-A-Freddie": f"fhlmc_sf{year}a_loans.txt"
        # TODO
    }
    filename = file_map.get(dataset)

    # TODO: we can define how we parse each type of file differently
    # for now, we assume we are only parsing a single file at a time
    parser_map = {
        # "Singlefamily-Census-Freddie": parse_singlefamily_census,
        "Singlefamily-National-A-Fannie": parse_national_a,
        "Singlefamily-National-A-Freddie": parse_national_a
    }
    parser = parser_map.get(dataset, parse_default)

    url = get_url(dataset, year)
    resp = urlopen(url)
    zipreader = ZipFile(BytesIO(resp.read()))
    
    return parser(zipreader.open(filename))

def parse_default(fileobj):
    return pd.read_csv(fileobj)

def parse_national_a(fileobj):
    # documentation: https://fhfa.gov/DataTools/Downloads/Documents/Enterprise-PUDB/National-File-A/2022_Single_Family_National_File_A.pdf
    colnames = ["enterprise_flag",
               "record_num",
               "msa_code",
               "tract_pct_minority", # pre-2012: 2000 census data; 2012-2021: 2010 census data; 2022: 2020 census data
               "tract_income_ratio",
               "borrower_income_ratio",
               "ltv",
               "purpose",
               "federal_guarantee",
               "borrower_race",
               "co-borrower_race",
               "borrower_gender",
               "co-borrower_gender",
               "num_units",
               "affordability"]
    return pd.read_csv(fileobj, names=colnames, delimiter='\s+')

# example calls below
singlefamily_a_freddie_2015 = get_data("Singlefamily-National-A-Freddie", 2015)
singlefamily_a_fannie_latest = get_data("Singlefamily-National-A-Fannie", 2022)
singlefamily_a_freddie_latest = get_data("Singlefamily-National-A-Freddie", 2022)

print(singlefamily_a_fannie_latest)
