import utils
import settings


def readResult(path_file):
    # origin: tmp/bwakit/tmp.hla	HLA-A*11:01:49	HLA-A*31:01:02	0	2	3
    # hla = {'A': ['A*11:01:01:01', 'A*31:01:02:01']}
    hla = {}
    for row in open(path_file):
        data = filter(lambda i: i.startswith("HLA"), row.split("\t"))
        data = map(lambda i: i[4:], data)
        data = list(data)
        print(data)
        if data:
            gene = data[0].split("*")[0]
            hla[gene] = data[:2]
    return hla


def findResult(method, name):
    return f"{settings.data_folder}/{name}/{method}/{name}.hla.top"


def main(event, context):
    name = event['name']
    method = "bwakit"
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
