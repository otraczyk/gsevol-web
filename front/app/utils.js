function getUrlParams() {
    var queryDict = {}
    location.search.substr(1).split("&")
        .forEach(function(item) {
            queryDict[item.split("=")[0]] = decodeURIComponent(item.split("=")[1])
        });
    return queryDict;
}

function jsonPostRequest(url) {
    var request = new XMLHttpRequest();
    request.open('POST', url, true);
    request.setRequestHeader("Content-type", "application/json");
    return request;
}

function JsonRequestPromise(url, params, method) {
    return new Promise(function(resolve, reject) {
        var request = new XMLHttpRequest();
        request.open(method, url, true);
        request.setRequestHeader("Content-type", "application/json");
        request.onload = function() {
            if (request.status == 200){
                resolve(JSON.parse(request.responseText));
            } else {
                console.log(request.responseText);
                reject(request.responseText);
            }
        };
        request.send(JSON.stringify(params))
    });
}
