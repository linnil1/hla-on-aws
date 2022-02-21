import shutil
import utils
import settings


def main(event, context):
    name = event['name']
    utils.setStatus(name, "Done")
    # shutil.rmtree(f'{settings.data_folder}/{name}/')
    return {"status": "OK"}
