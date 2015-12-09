var initialize = function(navigator){
    console.log(navigator);
    $('#id_login').on('click', function(){
        navigator.id.request();
    });
    navigator.id.watch();
};

window.Superlists = {
    Accounts: {
        initialize: initialize
    }
};