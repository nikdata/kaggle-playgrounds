import polars as pl
import polars.selectors as cs

train = pl.read_csv('data/train.csv')
test = pl.read_csv('data/test.csv')

# write out to parquet
train.write_parquet('data/train.parquet')
test.write_parquet('data/test.parquet')
