import csv
import multiprocessing as mp
from tqdm import tqdm
from utils import *

fp = open('results.csv', 'w')
writer = csv.DictWriter(fp, fieldnames=get_metadata({}).keys())
writer.writeheader()
fp.flush()

def record_file(id):
    file = crawl_file(id)
    record = get_metadata(file)
    writer.writerow(record)
    fp.flush()

def main():
    pool = mp.Pool(processes=mp.cpu_count())
    targets, cell_lines = read_inputs()
    try:
        for cell_line in tqdm(cell_lines, desc='cell lines', position=0):
            for target in tqdm(targets, desc='targets', position=1, leave=False):
                result = crawl_experiments(target, cell_line)
                if '@graph' in result.keys():
                    experiments = result['@graph']
                    for experiment in tqdm(experiments, desc='experiments', position=2, leave=False):
                        if 'files' in experiment.keys():
                            files = experiment['files']
                            file_ids = map(lambda x: x['@id'], files)
                            pool.map(record_file, file_ids)
    except Exception as ex:
        print('Error with cell line / target: ', cell_line, '/', target)
        print('Error with Experiment: ', experiment.get('accession', None))
        print('Error detected, files may not be complete.')
        raise(ex)
    pool.close()
    pool.join()
    fp.close()
    return None

if __name__ == "__main__":
    main()