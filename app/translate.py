import json
import requests
from flask_babel import _
from app import flaskApp

def translate(text, source_language, dest_language):
    # if translator key is not configured, return error.
    if "MS_TRANSLATOR_KEY" not in flaskApp.config or not flaskApp.config["MS_TRANSLATOR_KEY"]:
        return _("Error: the translation service is not configured.")
    # create auth dictionary to store header Ocp-Apim.. value.
    auth = {"Ocp-Apim-Subscription-Key": flaskApp.config["MS_TRANSLATOR_KEY"]}
    # sends a get request w/ query string args, returns a response object.
    # response object contains status code (200, 404) and JSON token w/ translation.
    r = requests.get("https://api.microsofttranslator.com/V2/Ajax.svc/Translate?text={}&from={}&to={}".format(text, source_language,
        dest_language), headers = auth)
    # non-200 status code means error.
    if r.status_code != 200:
        return _("Error: the translation service failed.")

    # content attribute of response object is a byte object. decode into UTF-8.
    # json.loads decodes JSON into raw python string.
    return json.loads(r.content.decode("utf-8-sig"))
