import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
from time import time


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = "output.csv.gz"
    os.system(f'wget {url} -O {csv_name}')

    df = pd.read_csv(csv_name, compression='gzip', low_memory=False)
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100_000, compression='gzip')

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    try:
        while True:
            t_start = time()
            df = next(df_iter)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.to_sql(name=table_name, con=engine, if_exists='append')
            t_end = time()

            print('Insertion done in %.3f seconds' % (t_end - t_start))
    except (StopIteration):
        print('Insertion compleat')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest CVS data to Postgres")

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='db for postgres')
    parser.add_argument('--table_name', help='table_name for postgres')
    parser.add_argument('--url', help='url for data')

    args = parser.parse_args()

main(args)
