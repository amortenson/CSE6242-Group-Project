import pandas as pd

pd.set_option('display.max_columns', None)  

df = pd.read_csv('sf_fred_2022_clean.csv')




df['county'] =  df['state_fips_code'].mul(1000).add(df['county_fips_code']).astype('str').str.zfill(5)

print(df.head(3))

# exclude territories
groupby = df[df['state_fips_code'] <= 56].groupby(['county'])

out = pd.DataFrame({
    'dti_avg': groupby['dti_num'].mean(),
    'ltv_avg': groupby['ltv'].mean(),
    'income_estimate': groupby['local_median_income'].mean().astype('int'), # not a good estimate
    'pct_first_time_buyer': groupby['first_time_buyer'].mean().mul(-1).add(2)
})

print(out.head())

out.to_csv('county_averages.csv')
