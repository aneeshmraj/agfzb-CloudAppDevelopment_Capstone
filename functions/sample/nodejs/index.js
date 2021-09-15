/**
 * Get all dealerships
 */
const http = require('http');
const Cloudant = require('@cloudant/cloudant');
const cred = require('./../../../functions/.creds-sample.json')

const requestListener = async function (req, res) {
    console.log(cred.COUCH_URL)
    console.log(cred.IAM_API_KEY)
    const cloudant = Cloudant({
        url: cred.COUCH_URL,
        plugins: { iamauth: { iamApiKey: cred.IAM_API_KEY } }
    });
    var db = cloudant.db.use('dealerships');
    const doclist = await db.list({include_docs: true})
    doclist.rows.forEach((doc) => {
    console.log(doc["doc"]);
    });
    res.end(doclist.toString());
}

const port = 8080;
const server = http.createServer(requestListener);
console.log('server listening on port: ' + port);
server.listen(port);