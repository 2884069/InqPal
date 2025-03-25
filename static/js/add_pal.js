const user_input = $("#search_box_input");
const users_div = $('#add_pal_results');
const delay_by_in_ms = 200;
let scheduled_function = false;
const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            users_div.html(response['html_from_view']);
        });
};

let search = function () {
    const request_parameters = {
        q: user_input.val()
    };

    if (scheduled_function) {
        clearTimeout(scheduled_function);
    }

    scheduled_function = setTimeout(function() {
        ajax_call(endpoint, request_parameters);
    }, delay_by_in_ms);
};

user_input.on('keyup', search);

let watch = function () {
    const button = $(this);
    const palId = button.data('user-id');

    $.ajax({
        url: endpoint,
        method: 'POST',
        data: {
            'pal_id': palId,
            'do': button.text().trim(),
            'csrfmiddlewaretoken': csrfToken
        },

        success: function (response) {
            if (response.success) {
                if (button.text().trim() === 'Watch') {
                    button.text('Unwatch');
                    button.removeClass('watch_button').addClass('unwatch_button');
                } else {
                    button.text('Watch');
                    button.removeClass('unwatch_button').addClass('watch_button');
                }
            } else {
                alert('An error occurred while adding pal');
            }
        },

        error: function () {
            alert('An error occurred while processing your request.');
        }
    });
};


users_div.on('click', '.watch_button, .unwatch_button', watch);

$('#clear_button').on('click', function () {
    user_input.val('');
    search();
});
