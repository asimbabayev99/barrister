$(document).ready(function () {
    $("#date_input").mask("xx/xx/xxxx");
    $("#time_input").mask("xx:xx");
    $("#date_input").datetimepicker({ format: 'DD/MM/YYYY', locale: 'az' });
    $(".calendar-save-button").on("click", function (e) {
        var a = 1;
        e.preventDefault();
        setInterval(() => {
            if ($("#name_input").val().length === 0) {
                $("#name_alert").show();

            };
            if ($(".time-input").text().length === 0 || $(".validation-time").text().length() === 0 || $(".validation-date").val().length === 0) {
                $("#date-alert-2").show()
            };
            if ($(".validation-reserv").text().length === 0) {
                $("#last-alert").show()
            };
        }, 1);
        setInterval(function () {
            if ($("#name_input").val().length > 0) {
                $("#name_alert").hide();


            };
            if ($(".validation-date").val().length > 0 && $(".validation-time").text().length > 0 && $(".validation-interval").text().length > 0) {
                $("#date-alert-2").hide();
            };
            if ($(".validation-reserv").text().length > 0) {
                $("#last-alert").hide();
            };
        }, 1);
        if ($("#name_input").val().length > 0 && $(".validation-date").val().length > 0 && $(".validation-time").text().length > 0 && $(".validation-interval").text().length > 0 && $(".validation-reserv").text().length > 0) {
            $("#exampleModalLong").modal("hide");
            $.ajax({
                type: "POST",
                url: "api/appointments/",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                data: {
                    'contact': {
                        'name': $("#name_input").val(),
                        'phone': $("#phone_input").val(),
                        'email': $("#email_input").val(),
                        'address': '',
                    },
                    'status': $('.validation-reserv').val(),
                    'address': $('#address_input').val(),
                    'start': $(".validation-date").val() + ' ' + $(".validation-time"),
                    'end': $(".validation-date").val()
                },
                error: function (jqXhr, textStatus, errorMessage) {
                    alert(errorMessage)
                },
                success: function (data) {

                }

            })
        };

    })
})