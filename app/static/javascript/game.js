$(document).ready(function () {
    var timeToAnswer = $.cookie('time');
    var rotates = 0;
    var counter;
    var count = timeToAnswer;


    $("body").on("click", ".submit-button", function () {
        if (timeToAnswer != 123) {
            clearInterval(counter); // Selection is made. Stop the timer
        }
        var jqxhr = $.ajax({
            type: "POST",
            url: "/game",
            dataType: "json",
            data: {id: parseInt($(this).attr('id').match(/\d+$/)[0])}
        })
            .done(function(data) {
                var right = data['previous']['right'];
                var yours = data['previous']['yours'];
                console.log(data['persons']);
                $("#failed-count").text(data['statistic']['failed']);
                $("#correct-count").text(data['statistic']['correct']);

                var delayTime = 500;
                if(right != yours) {
                     $("#select-"+yours).addClass("ui red label");
                    delayTime = 1500;
                }
                $("#select-"+right).addClass("ui green label");
                //game over
                 console.log(data['over']);
                if(data['over'] != false) {
                    if(data['over'] == 'limit') {
                        $("#go-modal-header").text("Вы проиграли.");
                        $("#go-modal-content").text("Допустимое количество неверных ответов превышено!");
                    } else if (data['over'] == 'end') {
                        $("#go-modal-header").text("Конец игры.");
                        $("#go-modal-content").text("Больше нет знаменитостей в базе(");
                    }
                    $("#game-over-modal").modal('show');
                    $(".submit-button").unbind('click');

                    console.log('Game over');
                    return;
                }

                //$("#select-"+yours).addClass("ui green label");
                setTimeout(function() {
                    $(".submit-button").removeClass("ui green red label");
                    $("#photo-back").attr('src', '/static/images/waiting.gif');
                    $("#photo-front").attr('src', '/static/images/waiting.gif');
                    if(rotates%2 == 0) {
                        $("#photo-back").attr('src', data['photo']);
                    } else {
                        $("#photo-front").attr('src', data['photo']);
                    }
                    $("#category-name").text(data['category']);
                    rotates++;
//                    document.querySelector("#myCard").classList.toggle("flip");
//                    $("#photo").fadeOut("fast", function() {
//                        $("#photo").attr('src', data['photo']);
//                    }).fadeIn("fast");

                    var personsDiv = $("#persons-list");
                    personsDiv.empty();
                    $.each(data['persons'], function(index, person) {
                        console.log(person);
                        var personDiv = $("<a>", {
                            id: "select-" + person.id,
                            text: person.name,
                            class: "item submit-button"
                        });
                        personsDiv.append(personDiv);
                    });
                    document.querySelector("#myCard").classList.toggle("flip");

                    // Reset timer
                    if(timeToAnswer != 123) {
                        count = timeToAnswer;
                        $("#time-count").text(timeToAnswer);
                        counter = setInterval(timer, 1000); //New level ready. Start the counter
                    }
                }, delayTime); // do something after ~1.5 seconds


            })
    });


    // Countdown
    if (timeToAnswer == 123) {
        $("#time-button").hide();
    }
    else {
        $("#time-count").text(timeToAnswer);
        counter = setInterval(timer, 1000); //1000 will  run it every 1 second
    }

    function timer() {
        count = count - 1;
        $("#time-count").text(count);
        if (count <= 0) {
            $("#game-over-modal").modal('show');
            //Send game-over message ??
            $.get("/endgame", function(data) {
                console.log(data);
            });
            // Stop timer
            clearInterval(counter);
        }
    }
});