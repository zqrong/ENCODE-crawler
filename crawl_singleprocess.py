import pandas as pd
from tqdm import tqdm
from utils import *

def main():
    targets, cell_lines = read_inputs()
    records = []
    try:
        for cell_line in tqdm(cell_lines, desc='cell lines', position=0):
            for target in tqdm(targets, desc='targets', position=1, leave=False):
                result = crawl_experiments(target, cell_line)
                if '@graph' in result.keys():
                    experiments = result['@graph']
                    for experiment in tqdm(experiments, desc='experiments', position=2, leave=False):
                        if 'files' in experiment.keys():
                            files = experiment['files']
                            for file in tqdm(files, desc='files', position=3, leave=False):
                                file = crawl_file(file['@id'])
                                record = get_metadata(file)
                                records.append(record)
    except Exception as ex:
        print('Error with cell line / target: ', cell_line, '/', target)
        print('Error with Experiment: ', experiment.get('accession', None))
        pd.DataFrame.from_records(records).to_csv('./results.csv')
        print('Error detected, files may not be complete.')
        raise(ex)

    pd.DataFrame.from_records(records).to_csv('./results.csv')
    print(len(records),'files found. Saved to results.csv successfully.')
    return None

if __name__ == "__main__":
    main()