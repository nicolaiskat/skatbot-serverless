import logging
from modules.matchservice import findNewMatchesManually

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ids = req.params.get('ids')
    if not ids:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            ids = req_body.get('ids')

    if ids:
        if findNewMatchesManually(ids):
            return func.HttpResponse(f"Matches inserted succesfully.",
                status_code=201
            )
        else:
            return func.HttpResponse(f"No new matches inserted.",
                status_code=200
            )
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass an array of ids in the request body.",
             status_code=200
        )
