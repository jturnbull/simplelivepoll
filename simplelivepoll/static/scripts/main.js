$(function() {
    // Add a close button to all messages
    $('.messages li, .alert.alert-block li').prepend('<a href="#" class="message-close">&times;</a>');
    // Bind a click event to the close button, to the close the message
    $(document).on('click', '.message-close', function(e) {
        e.preventDefault();
        $(this).closest('li').fadeOut('fast');
    });
});