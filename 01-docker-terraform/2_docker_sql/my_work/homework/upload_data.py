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
    zurl = params.zurl
    csv_name = "output.csv.gz"
    zones = "zones.csv"
    os.system(f'wget {url} -O {csv_name}')
    os.system(f'wget {zurl} -O {zones}')

    df = pd.read_csv(csv_name, compression='gzip', low_memory=False)
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100_000, compression='gzip')
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    try:
        while True:
            t_start = time()
            df = next(df_iter)
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
            df.to_sql(name=table_name, con=engine, if_exists='append')
            t_end = time()

            print('Insertion done in %.3f seconds' % (t_end - t_start))
    except (StopIteration):
        df_zones = pd.read_csv(zones)
        df_zones.to_sql(name='zones', con=engine, if_exists='replace')
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
    parser.add_argument('--zurl', help='url for zones')

    args = parser.parse_args()

main(args)
