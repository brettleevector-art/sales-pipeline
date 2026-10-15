"""Run the whole pipeline:  python pipeline.py"""
from etl.extract import extract
from etl.transform import transform
from etl.load import load

if __name__ == "__main__":
    load(transform(extract()))
