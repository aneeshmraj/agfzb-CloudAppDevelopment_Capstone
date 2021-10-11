/**
 * Get all dealerships
 */
const Cloudant = require('@cloudant/cloudant');
/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
async function main(params) {
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });
	var db = cloudant.db.use('dealerships');
	if(params.state != null){
	    var query = {
            "selector":{            
                "st": params.state       
            }
	    }
        const doclist = await db.find(query);
        return doclist;
    }
    else if (params.dealer_id !=null){
        var query = {
            "selector":{            
                "id": parseInt(params.dealer_id)
            }
	    }
        const doclist = await db.find(query);
        return doclist;
    }
    else{
	    const doclist = await db.list({include_docs: true})
	    return doclist;
	}
}
