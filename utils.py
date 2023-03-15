import requests

def read_inputs():
    with open('./targets.txt') as f:
        targets = f.read().splitlines()
    with open('./celllines.txt') as f:
        cell_lines = f.read().splitlines()
    return targets, cell_lines

def crawl_experiments(target, cell_line):
    url = 'https://www.encodeproject.org/search/?type=Experiment&target.label='+target+'&biosample_ontology.term_name='+cell_line+'&replicates.library.biosample.donor.organism.scientific_name=Homo+sapiens&format=json'
    try:
        response = requests.get(url)
        result = response.json()
    except:
        print('Error of crawling experiments with cell line / target: ', cell_line, '/', target)
        result = {}
    return result

def crawl_file(id):
    url = 'https://www.encodeproject.org/'+id+'/?format=json'
    try:
        response = requests.get(url)
        result = response.json()
    except:
        print('Error of crawling file: ', id)
        result = {'accession': id}
    return result

def get_metadata(file):
    record = {
        'accession': file.get('accession', None),
        'from_dataset': file.get('dataset', None),
        'cell_line': file.get('biosample_ontology', {'term_name':None})['term_name'],
        'target': file.get('target', {'label':None})['label'],
        'assay_term_name': file.get('assay_term_name', None),
        'lab': file.get('lab', {'title':None})['title'],
        'date_created': file.get('date_created', '')[:10],
        'file_format': file.get('file_format', None),
        'file_size_MB': round(file.get('file_size', 0)/(1024*1024)),
        'run_type': file.get('run_type', None),
        'mapped_read_length': file.get('mapped_read_length', None),
        'mapped_run_type': file.get('mapped_run_type', None),
        'assembly': file.get('assembly', None),
        'download_link': file.get('azure_uri', None),
        's3_uri': file.get('s3_uri', None)
    }
    return record