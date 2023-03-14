import requests
import pandas as pd
from tqdm import tqdm

def read_inputs():
    with open('./targets.txt') as f:
        targets = f.read().splitlines()
    with open('./celllines.txt') as f:
        cell_lines = f.read().splitlines()
    return targets, cell_lines

def crawl_experiments(target, cell_line):
    url = 'https://www.encodeproject.org/search/?type=Experiment&target.label='+target+'&biosample_ontology.term_name='+cell_line+'&replicates.library.biosample.donor.organism.scientific_name=Homo+sapiens&format=json'
    response = requests.get(url)
    result = response.json()
    return result

def crawl_file(id):
    url = 'https://www.encodeproject.org/'+id+'/?format=json'
    response = requests.get(url)
    result = response.json()
    return result

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
                                record = {
                                    'accession': file.get('accession', None),
                                    'from_dataset': file.get('dataset', None),
                                    'cell_line': file.get('biosample_ontology', None)['term_name'],
                                    'target': file.get('target', None)['label'],
                                    'assay_term_name': file.get('assay_term_name', None),
                                    'lab': file.get('lab', None)['title'],
                                    'date_created': file.get('date_created', None)[:10],
                                    'file_format': file.get('file_format', None),
                                    'file_size_MB': round(file.get('file_size', 0)/(1024*1024)),
                                    'mapped_read_length': file.get('mapped_read_length', None),
                                    'mapped_run_type': file.get('mapped_run_type', None),
                                    'assembly': file.get('assembly', None),
                                    'download_link': file.get('azure_uri', None),
                                    's3_uri': file.get('s3_uri', None)
                                }
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