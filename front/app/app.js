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
    $('#results').html(data.svg);
    $('#alerts').empty()
}

$(document).ajaxError(function(cos, resp) {
    error = resp.responseJSON.error
    $('#alerts').append('<li class="danger alert">Error processing input: ' + error + '</li>');
});

$(function(){
    $('#input-form').submit(sendTrees);
})
