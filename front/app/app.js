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
}

$(function(){
    $('#input-form').submit(sendTrees);
})
