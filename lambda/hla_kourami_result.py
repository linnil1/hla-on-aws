from glob import glob
from collections import defaultdict
import utils
import settings


def readResult(path_file):
    """
    Example file content
    A*01:01:01G	546	1.0	546	546	31.0	13.0	15.0
    A*11:01:01G	546	1.0	546	546	31.0	13.0	15.0
    """
    result = map(lambda a: a.split('\t')[0], open(path_file))
    result = map(lambda a: a.split('*'), result)
    # data = {'A': ['A*11:01:01:01', 'A*31:01:02:01']}
    data = defaultdict(list)
    for allele_gene, allele_type in result:
        if len(data[allele_gene]) < 2:
            data[allele_gene].append(f"{allele_gene}*{allele_type}")
    return dict(data)


def findResult(method, name):
    """ Find 'test1/kourami/test1.aln.panel.kourami.result' """
    files = glob(f"{settings.data_folder}/{name}/{method}/*.result")
    assert len(files) == 1
    return files[0]


def main(event, context):
    name = event['name']
    method = "kourami"
    new_filename = f"{name}.{method}.txt"

    file_name = findResult(method, name)
    utils.upload(file_name, new_filename)
    result = {
        'status': "success",
        'result_file': new_filename,
        'result': readResult(file_name),
    }
    utils.setMethodResult(name, method, result)
    return result
