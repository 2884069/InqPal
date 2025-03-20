const user_input = $("#search_box_input");
const users_div = $('#add_pal_results');
const delay_by_in_ms = 500;
let scheduled_function = false;

let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            users_div.html(response['html_from_view']);
        });
};

user_input.on('keyup', function () {
    const request_parameters = {
        q: $(this).val()  // value of user_input: the HTML element with ID user-input
    };

    // If scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function);
    }

    // Set a timeout to delay the function call by the specified time (debouncing)
    scheduled_function = setTimeout(function() {
        ajax_call(endpoint, request_parameters); // Pass the correct parameters to ajax_call
    }, delay_by_in_ms);
});
