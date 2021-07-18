import logging
import azure.functions as func

#import datetime
import json
from .predict import retourner_reco

def main(req: func.HttpRequest) -> func.HttpResponse:
    USER_ID = req.params.get('userId')
    
    if not USER_ID:
        try:
            req_body = req.get_json()
        except ValueError:
            #USER_ID = 99
            pass
        else:
            USER_ID = req_body.get("userId")

    print("blablabla")

    print(USER_ID)

    if USER_ID:
        
        #logging.info("{}: User ID received {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), USER_ID))
        print("----------------")
        user_id_int = int(USER_ID)
        print("----------------")
        
        print("USER_ID type:", type(USER_ID))
        print("user_id_int type:", type(user_id_int))
        
        #recommendations = reco_articles(user_id_int)
        
        results = [100, 34, 32, 893, 1]
        
        #response = func.HttpResponse(json.dumps({"recommendations": results}))
        #response = response.get_body().decode('utf-8')
        #response = json.loads(response)
        #response = response["recommendations"]
        
        #return json.dumps(response)
        return func.HttpResponse(json.dumps(retourner_reco(user_id_int)))
    
    else:

        return func.HttpResponse("User not found")
