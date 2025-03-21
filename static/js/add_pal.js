const user_input = $("#search_box_input");
const users_div = $('#add_pal_results');
const delay_by_in_ms = 200;
let scheduled_function = false;

let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            users_div.html(response['html_from_view']);
        });
};

user_input.on('keyup', function () {
    const request_parameters = {
        q: $(this).val()
    };

    if (scheduled_function) {
        clearTimeout(scheduled_function);
    }

    
    scheduled_function = setTimeout(function() {
        ajax_call(endpoint, request_parameters);
    }, delay_by_in_ms);
});

$('.watch-btn').on('click', function () {
    const button = $(this);
    const palId = button.data('user-id');
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

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
                } else {
                    button.text('Watch');
                }
            } else {
                alert('An error occurred while adding pal');
            }
        },

        error: function () {
            alert('An error occurred while processing your request.');
        }
    });

});