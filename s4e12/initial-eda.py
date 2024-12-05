# import
import polars as pl
import polars.selectors as cs
import seaborn as sns
import matplotlib.pyplot as plt

# improve polars output
pl.Config.set_tbl_rows(30)
pl.Config.set_tbl_width_chars(1000)
pl.Config.set_tbl_cols(-1)

# load
raw_train = pl.read_parquet('data/train.parquet')
raw_test = pl.read_parquet('data/test.parquet')

# preview
raw_train.head()
raw_test.head()

# combine train/test for eda
raw_combo = raw_train.with_columns(dataset = pl.lit('train')).vstack(raw_test.with_columns(pl.lit(None).alias("Premium Amount")).with_columns(dataset = pl.lit('test')))

# rename the column names so they're not shitty
raw_combo.columns = [i.lower().replace(' ','_') for i in raw_combo.columns]

raw_combo.head()

# CHECK: missing values
null_counts = raw_combo \
    .group_by(['dataset']) \
    .agg([pl.col(col).is_null().sum().alias(f"{col}") for col in raw_combo.columns if col != "dataset"]) \
    .select(pl.exclude('premium_amount')) \
    .sort(by = 'dataset', descending=True) \
    .transpose(include_header=True, header_name='column', column_names=['train','test']) \
    .slice(1) \
    .with_columns(
        test = pl.col('test').cast(pl.Int64), 
        train = pl.col('train').cast(pl.Int64)
    ) \
    .with_columns(
        pct_train = ((pl.col('train')/(pl.col('train').sum())*100).round(2)), 
        pct_test = ((pl.col('test')/(pl.col('test').sum())*100).round(2)) 
    )

null_counts \
    .filter(pl.col('train') > 0) \
    .sort(by=pl.col('pct_train'), descending=True) \
    .join(pl.DataFrame({'column':raw_combo.columns, 'type':raw_combo.dtypes}), left_on = ['column'], right_on=['column'], how='inner')

# both train/test have same columns of missing info
# previous_claims, occupation, and credit score all have 10% or more missing data
# previous_claims is 30% missing data (train & test)
# 8 numerical columns with missing data (highest is age)
# 3 categorical columns with missing data (highest is marital status)

# CHECK: unique values
raw_combo.group_by(['dataset']).agg([pl.col(col).n_unique().alias(f"{col}") for col in raw_combo.columns if col != 'dataset']).select(pl.exclude('premium_amount')).sort(by = 'dataset', descending=True).transpose(include_header=True, header_name = 'column', column_names = ['unique_train','unique_test']).slice(1)



