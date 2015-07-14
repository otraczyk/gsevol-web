sendTrees = function(event){
    // TODO: validation
    event.preventDefault();
    $.post('api/draw/', $(event.currentTarget).serialize(), renderResults);
}

renderResults = function(data){
    console.log(data);
}

$(function(){
    $('#input-form').submit(sendTrees);
})
