$(function() {
    $("input,textarea").jqBootstrapValidation();
});


/*When clicking on Full hide fail/success boxes */
$('#name').focus(function() {
    $('#success').html('');
});
