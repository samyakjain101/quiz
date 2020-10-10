$(document).ready(function () {
    console.log("Loaded")
    $('body').on('click', '.ajax-save-btn' ,function (event) {
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
    $('body').on('click', '.ajax-btn-page', function (event) {
        var btn = $(this)
        console.log("WOrking");
        event.preventDefault()
            $.ajax({
                type: "GET",
                url: btn.attr('url'),
                // data: {
                // },
                success: handleFormSuccess,
            });
            function handleFormSuccess(html) {
                btn.closest('.container').html($(html).find('.main-container').html())
            } 
    });
});

