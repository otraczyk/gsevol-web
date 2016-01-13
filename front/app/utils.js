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
