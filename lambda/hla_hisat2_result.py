import re
from glob import glob
from collections import defaultdict
import utils
import settings


def readResult(path_file):
    # result = list of [gene, allele, abundance] -> [A, 31:01:01:01, "12.54"]
    result = filter(lambda a: "ranked" in a, open(path_file))
    result = map(lambda a: re.findall(r".*?(\w+)\*(.*?) .*?(\d+\.\d+)", a)[0],
                 result)
    # data = {'A': ['A*11:01:01:01', 'A*31:01:02:01']}
    data = defaultdict(list)
    for allele_gene, allele_type, _ in result:
        if len(data[allele_gene]) < 2:
            data[allele_gene].append(f"{allele_gene}*{allele_type}")
    return dict(data)


def findResult(method, name):
    """ Find 'tmp/assembly_graph-hla.test3_R1_fq-hla-extracted-1_fq.report' """
    files = glob(f"{settings.data_folder}/{name}/{method}/*.report")
    assert len(files) == 1
    return files[0]


def main(event, context):
    name = event['name']
    method = "hisat2"
    new_filename = f"{name}.{method}.txt"

    file_name = findResult(method, name)
    utils.upload(file_name, new_filename)
    result = {
        'status': "success",
        'result_file': new_filename,
        'result': readResult(file_name),
    }
    utils.setMethodResult(name, method, result)
    # rm -rf data/name
    return result
