var initialize = function () {
    $('input[name="title"]').on('keypress', function () {
        $('.has-error').hide()
    })
}