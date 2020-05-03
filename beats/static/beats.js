window.Superbeats = {}
window.Superbeats.initialize = function () {
    $('input[name="title"]').on('keypress', function () {
        $('.has-error').hide()
    })
}