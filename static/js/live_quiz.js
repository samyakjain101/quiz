$(document).ready(function () {
    console.log("Loaded");

    // below are for timer
    var years = document.getElementById("timerDetails").getAttribute("years");
    var months = document.getElementById("timerDetails").getAttribute("months");
    var days = document.getElementById("timerDetails").getAttribute("days");
    var hours = document.getElementById("timerDetails").getAttribute("hours");
    var minutes = document.getElementById("timerDetails").getAttribute("minutes");
    var seconds = document.getElementById("timerDetails").getAttribute("seconds");
    var expiryUrl = document.getElementById("timerDetails").getAttribute("expiryUrl");
    var timerDuration = new Date(years, months-1, days, hours,minutes,seconds,0);
    $('#defaultCountdown').countdown({until: timerDuration, compact: true, format: 'HMS',expiryText: 'TEST EXPIRED',expiryUrl: expiryUrl,}); 
    console.log(hours + " : " + minutes + " : " + seconds);
    console.log(timerDuration);
    // above are for timer

    $('body').on('click', '.ajax-save-mark' ,function (event) {
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
                $(".skipbtn").click();
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

