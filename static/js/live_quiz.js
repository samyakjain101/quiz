$(document).ready(function () {
    console.log("Loaded")
    $('.ajax-save-btn').on('click', function (event) {
        var btn = $(this)
        event.preventDefault()
            $.ajax({
                type: "GET",
                url: btn.attr('url'),
                data: {
                    'question_id': btn.attr('question_id'),
                    'choice_id': $('input:checked').attr('choice_id'),
                },
                success: handleFormSuccess,
            });
            function handleFormSuccess(json) {
                console.log(json.message);
            } 
    });
});

