from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import pandas as pd
import numpy as np
import functools as ft

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
        "Singlefamily-Census-Fannie": f"fnma_sf{year}c_loans.txt",
        "Singlefamily-National-A-Fannie": f"fnma_sf{year}a_loans.txt",
        "Singlefamily-National-A-Freddie": f"fhlmc_sf{year}a_loans.txt"
        # TODO
    }
    filename = file_map.get(dataset)

    # TODO: we can define how we parse each type of file differently
    # for now, we assume we are only parsing a single file at a time
    parser_map = {
        "Singlefamily-Census-Freddie": parse_singlefamily_census,
        "Singlefamily-Census-Fannie": parse_singlefamily_census,
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

def parse_singlefamily_census(fileobj):
    # documentation: https://www.fhfa.gov/DataTools/Downloads/Documents/Enterprise-PUDB/Single-Family_Census_Tract_File_/2022_Single_Family_Census_Tract_File.pdf
    # note: check documentation for the specific year you are pulling data from. Not all columns are present for all years
    colnames = ["enterprise_flag",
                "record_num",
                "state_fips_code",
                "msa_code",
                "county_fips_code",
                "census_tract", # pre-2012: 2000 census data; 2012-2021: 2010 census data; 2022: 2020 census data
                "tract_pct_minority",
                "tract_median_income",
                "local_median_income",
                "tract_income_ratio",
                "borrower_income",
                "local_median_family_income",
                "borrower_income_ratio",
                "upb",
                "purpose",
                "federal_guarantee",
                "num_borrowers",
                "first_time_buyer",
                "borrower_race_1", # 5 columns for borrower race; first 4 seem mostly N/A
                "borrower_race_2", # TODO: is there a better way to parse these 5 cols?
                "borrower_race_3",
                "borrower_race_4",
                "borrower_race", # use this
                "borrower_ethnicity",
                "co-borrower_race_1", # 5 columns for co-borrower race; see above
                "co-borrower_race_2",
                "co-borrower_race_3",
                "co-borrower_race_4",
                "co-borrower_race",
                "co-borrower_ethnicity",
                "borrower_gender",
                "co-borrower_gender",
                "borrower_age",
                "co-borrower_age",
                "occupancy_code",
                "rate_spread",
                "HOEPA_status",
                "property_type",
                "lien_status",
                "borrower_62+",
                "co-borrower_62+",
                "ltv",
                "date_of_note",
                "term_at_orig",
                "num_units",
                "rate_at_orig",
                "note_amount",
                "preapproval",
                "application_channel",
                "AUS_name",
                "borrower_credit_model",
                "co-borrower_credit_model",
                "dti",
                "discount_points",
                "intro_rate_period",
                "land_property_interest",
                "property_value",
                "rural_tract",
                "mississippi_delta_county",
                "mid_appalachia_county",
                "persistent_poverty_county",
                "area_concentrated_poverty",
                "high_opportunity_area",
                "qualified_opportunity_zone_tract"]
    return pd.read_csv(fileobj, names=colnames, delimiter='\s+') # TODO: clean
                


        

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

def map_dti_to_label(dti):
    if dti in {10,20,30}:
        return '<= 35%'
    elif 36 <= dti <= 98:
        return '> 35%'

def clean_df(df): # based on code by Ning Xia
    df_clean = df.copy()
    df_clean = df_clean.iloc[:, 2:63]
    df_clean = df_clean.replace('', np.nan)

    # TODO filter columns

    cols_wt_missing_vals = ['state_fips_code', 'borrower_income', 'upb', 'purpose', 'federal_guarantee', 'num_borrowers',
                            'occupancy_code', 'HOEPA_status', 'property_type', 'lien_status', 'date_of_note',
                            'term_at_orig', 'num_units', 'rural_tract', 'mississippi_delta_county', 'mid_appalachia_county',
                            'persistent_poverty_county', 'area_concentrated_poverty', 'high_opportunity_area']  #19

    cols_missing_vals_gt_5pct = ['borrower_race_1', 'borrower_race_2', 'borrower_race_3', 'borrower_race_4',
                                'borrower_race', 'borrower_ethnicity', 'co-borrower_race_1', 'co-borrower_race_2',
                                'co-borrower_race_3', 'co-borrower_race_4', 'co-borrower_race', 'co-borrower_ethnicity',
                                'borrower_gender', 'co-borrower_gender', 'co-borrower_age', 'rate_spread',
                                'co-borrower_62+', 'preapproval', 'borrower_credit_model', 'co-borrower_credit_model',
                                'discount_points', 'intro_rate_period', 'land_property_interest'] #23

    cols_missing_vals_le_5pct = ['msa_code', 'county_fips_code', 'census_tract', 'tract_pct_minority',
                                'tract_median_income', 'local_median_income', 'tract_income_ratio',
                                'local_median_family_income', 'borrower_income_ratio', 'first_time_buyer', 'borrower_age',
                                'borrower_62+', 'ltv', 'rate_at_orig', 'note_amount', 'application_channel', 'AUS_name',
                                'property_value', "dti"] #19

    cols_keep = df_clean.columns.difference(cols_missing_vals_gt_5pct)

    df_clean = df_clean[cols_keep]

    df_clean = df_clean.drop(['HOEPA_status', 'lien_status'], axis=1)   # 36 cols
    cols_wt_missing_vals = list(set(cols_wt_missing_vals) - set(['HOEPA_status', 'lien_status']))

    # map dti
    df_clean.loc[:, 'dti'] = df_clean['dti'].apply(map_dti_to_label)
    df_clean.rename(columns={'dti': 'dti_cat'}, inplace=True)
    df_clean.loc[:, 'dti_num'] = df.loc[:, 'dti']

    # set these column types as categorical: 24 cols
    cols_categ = ['msa_code', 'census_tract', 'purpose', 'federal_guarantee',
                'borrower_age', 'occupancy_code', 'property_type', 'borrower_62+', 'date_of_note',
                'application_channel', 'AUS_name', 'dti_cat', 'rural_tract', 'mississippi_delta_county',
                'mid_appalachia_county', 'persistent_poverty_county', 'area_concentrated_poverty',
                'high_opportunity_area', "num_units", "num_borrowers", "term_at_orig"]

    df_clean[cols_categ] = df_clean[cols_categ].apply(lambda x: x.astype('category'))

    cols_fips = ['state_fips_code', 'county_fips_code']

    # numerical variables which need imputation
    cols_imput_num = ['tract_pct_minority', 'tract_median_income', 'local_median_income', 'tract_income_ratio',
                    'local_median_family_income', 'borrower_income_ratio', 'ltv', 'rate_at_orig', 'note_amount',
                    'property_value', 'dti_num']  # 11 cols
    # categorical variables which need imputation
    cols_imput_cat = ['msa_code', 'county_fips_code', 'census_tract', 'first_time_buyer', 'borrower_age',
                    'borrower_62+', 'application_channel', 'AUS_name', "dti_cat"] # 9 cols

    # imputation for numerical variables
    df_cols_imput_num = df_clean[cols_imput_num]
    df_cols_imput_num.loc[:, 'tract_pct_minority'] = [np.nan if val == 9999.0 else val for val in df_cols_imput_num['tract_pct_minority']]
    df_cols_imput_num.loc[:, 'tract_median_income'] = [np.nan if val == 999999 else val for val in df_cols_imput_num['tract_median_income']]
    df_cols_imput_num.loc[:, 'local_median_income'] = [np.nan if val == 999999 else val for val in df_cols_imput_num['local_median_income']]
    df_cols_imput_num.loc[:, 'tract_income_ratio'] = [np.nan if val == 9999.000 else val for val in df_cols_imput_num['tract_income_ratio']]
    df_cols_imput_num.loc[:, 'local_median_family_income'] = [np.nan if val == 999999 else val for val in df_cols_imput_num['local_median_family_income']]
    df_cols_imput_num.loc[:, 'borrower_income_ratio'] = [np.nan if val == 9999.000 else val for val in df_cols_imput_num['borrower_income_ratio']]
    df_cols_imput_num.loc[:, 'ltv'] = [np.nan if val == 999.00 else val for val in df_cols_imput_num['ltv']]
    df_cols_imput_num.loc[:, 'rate_at_orig'] = [np.nan if val == 99.000 else val for val in df_cols_imput_num['rate_at_orig']]
    df_cols_imput_num.loc[:, 'note_amount'] = [np.nan if val == 999999999 else val for val in df_cols_imput_num['note_amount']]
    df_cols_imput_num.loc[:, 'property_value'] = [np.nan if val == 999999999 else val for val in df_cols_imput_num['property_value']]
    df_cols_imput_num.loc[:, 'dti_num'] = [np.nan if val == 99 else val for val in df_cols_imput_num['dti_num']]
    # median values for numerical columns which need imputation
    median_vals_num = df_cols_imput_num.median()
    # replace NAs with median values in each numerical columns
    df_cols_imputed_num = df_cols_imput_num.fillna(median_vals_num)

    # imputation for categorical variables
    df_cols_imput_cat = df_clean[cols_imput_cat]
    df_cols_imput_cat.loc[:, 'msa_code'] = [np.nan if val == 0 else val for val in df_cols_imput_cat['msa_code']]
    df_cols_imput_cat.loc[:, 'county_fips_code'] = [np.nan if val == 0 else val for val in df_cols_imput_cat['county_fips_code']]
    df_cols_imput_cat.loc[:, 'census_tract'] = [np.nan if val == 0 else val for val in df_cols_imput_cat['census_tract']]
    df_cols_imput_cat.loc[:, 'first_time_buyer'] = [np.nan if val == 9 else val for val in df_cols_imput_cat['first_time_buyer']]
    df_cols_imput_cat.loc[:, 'borrower_age'] = [np.nan if val == 9 else val for val in df_cols_imput_cat['borrower_age']]
    df_cols_imput_cat.loc[:, 'borrower_62+'] = [np.nan if val == 9 else val for val in df_cols_imput_cat['borrower_62+']]
    df_cols_imput_cat.loc[:, 'application_channel'] = [np.nan if val == 9 else val for val in df_cols_imput_cat['application_channel']]
    df_cols_imput_cat.loc[:, 'AUS_name'] = [np.nan if (val == 6) | (val == 9) else val for val in df_cols_imput_cat['AUS_name']]
    df_cols_imput_cat.loc[:, 'dti_cat'] = [np.nan if val == 99 else val for val in df_cols_imput_cat['dti_cat']]
    # mode values for categorical columns which need imputation
    mode_vals_cat = df_cols_imput_cat.mode()
    # replace NAs with mode values in each categorical columns
    df_cols_imputed_cat = df_cols_imput_cat.fillna({k: v[0] for k, v in mode_vals_cat.to_dict().items()})

    df_clean = pd.concat([df_clean[cols_wt_missing_vals], df_cols_imputed_num,
                                    df_cols_imputed_cat], axis=1)

    df_clean[cols_fips] = df_clean[cols_fips].apply(lambda x: x.astype('int'))

    return df_clean

def get_county_averages(raw_df):
    df = raw_df.copy()
    df['county'] =  df['state_fips_code'].mul(1000).add(df['county_fips_code']).astype('str').str.zfill(5)

    #print(df.head(3))

    # exclude territories
    groupby = df[df['state_fips_code'] <= 56].groupby(['county'])

    out = pd.DataFrame({
        'dti_avg': groupby['dti_num'].mean().round(3),
        'ltv_avg': groupby['ltv'].mean().round(3),
        'income_estimate': groupby['local_median_income'].mean().round(0).astype('int'), # not a good estimate
        'pct_nonwhite_estimate': groupby['tract_pct_minority'].mean().round(3), # not a good estimate
        'pct_first_time_buyer': groupby['first_time_buyer'].mean().mul(-100).add(200).round(3)
    })

    out.reset_index()

    return out


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


datasets = ['Singlefamily-Census-Fannie', 'Singlefamily-Census-Freddie']
years = range(2018, 2023) # 2018-2022

yearly_data = {}

for year in years:
    raw_data = pd.concat([get_data(dataset, year) for dataset in datasets])
    cleaned_data = clean_df(raw_data)
    county_averages = get_county_averages(cleaned_data)
    #cols_to_rename = ['dti_avg', 'income_estimate', 'pct_nonwhite_estimate', 'pct_first_time_buyer']
    county_averages = county_averages.rename(columns=lambda x: f'{x}_{year}' if x != 'county' else x)
    print(county_averages.head(3))
    yearly_data[year] = county_averages


df_final = ft.reduce(lambda left, right: pd.merge(left, right, on='county'), [v for (k,v) in yearly_data.items()])
df_final.to_csv('county_averages_by_year.csv')
