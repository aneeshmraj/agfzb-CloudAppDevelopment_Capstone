/**
 * Get all dealerships
 */
const http = require('http');
const Cloudant = require('@cloudant/cloudant');
const url = require('url');
const cred = require('./../../../functions/.creds-sample.json')

const requestListener = async function (req, res) {

    const cloudant = Cloudant({
        url: cred.COUCH_URL,
        plugins: { iamauth: { iamApiKey: cred.IAM_API_KEY } }
    });
    console.log(req.url);
    if (req.url === '/api/dealership'){
        getAllDealerships(req,res,cloudant);
    }
    else if (req.url.startsWith('/api/dealership?state=')){
        getAllDealershipsByState(req,res,cloudant);;
    }
    else{
        res.end();
    }
}

async function getAllDealerships(req, res, cloudant){
    var db = cloudant.db.use('dealerships');
    let dealerships = [];
    const doclist = await db.list({include_docs: true})
    doclist.rows.forEach((doc) => {
    let dealer = doc["doc"];
    delete dealer['_id'];
    delete dealer['_rev'];    
    dealerships.push(dealer);
    });
    res.end(JSON.stringify(dealerships));
}

async function getAllDealershipsByState(req,res, cloudant){
    var db = cloudant.db.use('dealerships');
    const queryObject = url.parse(req.url,true).query;
    var query = {
        "selector":{            
            "st": queryObject['state']       
        }
    }    
    let dealerships = [];
    const doclist = await db.find(query);
    doclist.docs.forEach(doc => {
    let dealer = doc;
    delete dealer['_id'];
    delete dealer['_rev'];    
    dealerships.push(dealer);
    });
    res.end(JSON.stringify(dealerships));
    
}
const port = 8080;
const server = http.createServer(requestListener);
console.log('server listening on port: ' + port);
server.listen(port);