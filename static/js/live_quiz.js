$(document).ready(function () {
    console.log("Loaded")
    $('body').on('click', '.ajax-save-and-next' ,function (event) {
        var btn = $(this)
        event.preventDefault()
            $.ajax({
                type: "GET",
                url: btn.attr('url'),
                data: {
                    'question_id': btn.closest('#ajax-main-container').find('.ajax-question-container').attr('question_id'),
                    'choice_id': $('input:checked').attr('choice_id'),
                    'to_do' : btn.attr('to_do'),
                },
                success: handleFormSuccess,
            });
            function handleFormSuccess(json) {
                console.log(json.message);
            } 
    });
    
    $('body').on('click', '.ajax-markReview-btn' ,function (event) {
        var btn = $(this)
        event.preventDefault()
            $.ajax({
                type: "GET",
                url: btn.attr('url'),
                data: {
                    'question_id': btn.attr('question_id'),
                    'to_do' : btn.attr('to_do'),
                },
                success: handleFormSuccess,
            });
            function handleFormSuccess(json) {
                console.log(json.message);
            } 
    });

    $('body').on('click', '.ajax-dontReview-btn' ,function (event) {
        var btn = $(this)
        event.preventDefault()
            $.ajax({
                type: "GET",
                url: btn.attr('url'),
                data: {
                    'question_id': btn.attr('question_id'),
                    'to_do' : btn.attr('to_do'),
                },
                success: handleFormSuccess,
            });
            function handleFormSuccess(json) {
                console.log(json.message);
            } 
    });
    
    $('body').on('click', '.ajax-btn-page-direct', function (event) {
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
                $('#ajax-main-container').replaceWith($(html).find('#ajax-main-container'));
            } 
    });
});

