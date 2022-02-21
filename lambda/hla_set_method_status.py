import utils


def main(event, context):
    utils.setStatus(event['name'], event['status'], event['method'])
    return {"status": "OK"}
