sendTrees = function(){
    // TODO: validation
    $.ajax({
        type: "POST",
        url: '/api/draw/',
        data: JSON.stringify(getUrlParams()),
        success: renderResults,
        contentType: 'application/json'
    });
    return false;
}

renderResults = function(data){
    reaults = React.render(
        React.createElement(Results, {data: data}),
        document.getElementById('results')
    );
    $('#alerts').empty()
}

$(document).ajaxError(function(cos, resp) {
    error = resp.responseJSON || resp.responseText
    $('#alerts').append('<li class="danger alert">Error processing input: ' + error + '</li>');
});

$(function(){
    sendTrees();
})
