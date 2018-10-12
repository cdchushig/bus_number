# -*- coding: utf-8 -*-
import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from ..utils import save_json, load_json
import click

from ..logging import logger
from ..paths import model_path, model_output_path
from . import run_model

@click.command()
@click.argument('model_list')
@click.option('--output_file', '-o', nargs=1, type=str, default='predictions.json')
@click.option('--hash-type', '-H', type=click.Choice(['md5', 'sha1']), default='sha1')
def main(model_list, *, output_file, hash_type):
    logger.info(f'Executing models from {model_list}')

    os.makedirs(model_output_path, exist_ok=True)

    predict_list = load_json(model_path / model_list)

    saved_meta = {}
    metadata_keys = ['dataset_name', 'hash_type', 'data_hash', 'target_hash', 'experiment']
    for exp in predict_list:
        ds = run_model(**exp)
        name = ds.metadata['dataset_name']
        metadata = {}
        for key in metadata_keys:
            metadata[key] = ds.metadata[key]
            saved_meta[name] = metadata

    save_json(model_path / output_file, saved_meta)
    logger.info(f"Predict complete! Results in {model_path / output_file}")
    
if __name__ == '__main__':

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
