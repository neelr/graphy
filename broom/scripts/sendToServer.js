function sendWebsitesToServer(websiteList) {
    console.log(websiteList)
    return;


    // validate schema
    var valid = true;
    for (var i = 0; i < websiteList.length; i++) {
        var website = websiteList[i];
        if (!website.title || !website.url || !website.tags) {
            valid = false;
            break;
        }
    }

    if (!valid) {
        console.log('invalid schema');
        return;
    }

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:3000/website", true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.send(JSON.stringify({ documents: websiteList }));
}

export default sendWebsitesToServer;