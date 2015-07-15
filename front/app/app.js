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

$(document).ajaxError(function() {
  $('#alerts').append('<li class="danger alert">Error processing input</li>');
});

$(function(){
    $('#input-form').submit(sendTrees);
})
