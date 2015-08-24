sendTrees = function(event){
    // TODO: validation
    $.ajax({
        type: "POST",
        url: 'api/draw/',
        data: JSON.stringify($(event.currentTarget).serializeArray()),
        success: renderResults,
        contentType: 'application/json'
    });
    return false;
}

renderResults = function(data){
    reaults = React.render(
        <Results data={data} />, document.getElementById('results')
    );
    $('#alerts').empty()
}

$(document).ajaxError(function(cos, resp) {
    error = resp.responseJSON || resp.responseText
    PubSub.publish('newError', error);
    // $('#alerts').append('<li class="danger alert">Error processing input: ' + error + '</li>');
});

$(function(){
    $('#input-form').submit(sendTrees);
    errorList = React.render(
        <ErrorList bla={3} />, document.getElementById('alerts')
    );
})
