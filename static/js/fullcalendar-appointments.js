$(document).ready(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    $(".times-div .begin-time-choices").click(function () {
        $(".times-div #time_input").text($(this).text())
    })
    $(".times-div-2 .begin-time-choices").click(function () {
        $(".times-div-2 #time_input").text($(this).text())
    })
    $(".times-div-3 .begin-time-choices").click(function () {
        $(".times-div-3 #time_input").text($(this).text())
    })
    $("#date_input").mask("xx/xx/xxxx");
    $("#time_input").mask("xx:xx");
    $("#name_input").keyup(function () {
        if ($("#name_input").val().length === 0) {
            $("#name_alert").show();

        } else {
            $("#name_alert").hide();

        };
    });



    $("#date_input").datetimepicker({ format: 'DD/MM/YYYY', locale: 'az' });
    $(".calendar-save-button").on("click", function (e) {
        var a = 1;

        e.preventDefault();
        if ($("#name_input").val().length === 0) {
            $("#name_alert").show();

        };
        if ($(".time-input").text().length === 0 || $(".validation-time").text().length === 0 || $(".validation-date").val().length === 0) {
            $("#date-alert-2").show()
        };
        if ($(".validation-reserv").text().length === 0) {
            $("#last-alert").show()
        };


        if ($("#name_input").val().length > 0) {
            $("#name_alert").hide();


        };
        if ($(".validation-date").val().length > 0 && $(".validation-time").text().length > 0 && $(".validation-interval").text().length > 0) {
            $("#date-alert-2").hide();
        };
        if ($(".validation-reserv").text().length > 0) {
            $("#last-alert").hide();
        };

        if ($("#name_input").val().length > 0 && $(".validation-date").val().length > 0 && $(".validation-time").text().length > 0 && $(".validation-interval").text().length > 0 && $(".validation-reserv").text().length > 0) {
            $("#exampleModalLong").modal("hide");
            $.ajax({
                type: "POST",
                url: "/api/appointments/",
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

    });

    /**Checkbox whole day */
    $("#whole_day_checkbox").click(function () {
        if ($(this).is(":checked")) {
            $("#asim").attr("disabled", true);
            $("#asim").val("00:00");
            $("#modal_2_end_hour").val("23:59");
            $("#modal_2_end_hour").attr("disabled", true);

        } else {
            $("#asim").attr("disabled", false);
            $("#modal_2_end_hour").attr("disabled", false);
            $("#asim").val("");
            $("#modal_2_end_hour").val("");
        }
    })
    //Checkbox end
    $("#modal_2_begin").mask("xx/xx/xxxx");
    $("#modal_2_end").mask("xx/xx/xxxx");
    $("#modal_2_end_hour").mask("xx:xx");
    $("#asim").mask("xx:xx");
    // CAlendar data save begin
    $(".icons-contents-main .icons").click(function() {
        var icon = $(this);
        $(".icon-content").html(icon.html())
    });


    $("#calendar-ms").fullCalendar({
        customButtons: {
          printButton: {
            text: 'Çap et',
            click: function () {
              window.print();
            }
          }
        },
    
        header: {
          left: "prevYear,prev,next,nextYear",
          center: "title",
          right: "today,month,agendaWeek,agendaDay,printButton"
        },
        buttonText: {
          prevYear: new moment().year() - 1,
          nextYear: new moment().year() + 1
        },
        viewRender: function (view) {
          var y = moment($('#calendar-ms').fullCalendar('getDate')).year();
          $(".fc-prevYear-button").text(y - 1),
            $(".fc-nextYear-button").text(y + 1)
        },
        defaultView: "month",
        navLinks: true, // can click day/week names to navigate views
        selectable: true,
        selectHelper: true,
        editable: true,
        eventLimit: true, // allow "more" link when too many events
    
        select: function (start, end) {
          // Display the modal.
          // You could fill in the start and end fields based on the parameters
          $(".modal").modal("show");    
          $(".modal").find(".calendar-modal #event_title").val("");
          $(".modal").find(".calendar-modal .icon-content").html('<i class="fas fa-angle-down"></i>');
          $(".modal").find(".calendar-modal input").val("");
          $(".modal").find(".calendar-modal input").attr("disabled",false);
          $(".modal").find(".calendar-modal #whole_day_checkbox").attr("checked",false);
          $(".modal").find(".calendar-modal #modal_2_end_hour").attr("disabled",false);
          $(".modal").find(".calendar-modal #modal_2_end_hour").attr("disabled",false);
          

          
        },
    
        eventRender: function (event, element) {
          if (event.bgcolor) {
            element.css('background-color', event.bgcolor)
            element.css('color', event.textcolor)
          }
          //dynamically prepend close button to event
          element.find(".fc-content").prepend("<span data-id='" + event.id + "' class='closeon material-icons'>x&nbsp</span>");
          element.find(".closeon").on("click", function () {
            id = $(this).attr('data-id')
            $.ajax({
              type: 'DELETE',
              url: '/api/events/' + event.id + '/',
              headers: { "X-CSRFToken": getCookie('csrftoken') },
              success: function (data) {
                $("#calendar-ms").fullCalendar("removeEvents", event._id);
              },
              error: function (jqXhr, textStatus, errorMessage) {
                alert(errorMessage)
              }
            });
            // $("#calendar-ms").fullCalendar("removeEvents", event._id);
          });
        },
    
        eventClick: function (calEvent, jsEvent) {
          // Display the modal and set event values.
          $(".modal").modal("show");
          $(".add_event_name_main input").attr("readonly", true);
          $(".modal").find(".calendar-modal #event_title").val(calEvent.title);
          $(".modal").find(".calendar-modal #event_location").val(calEvent.mekan);
          $(".modal").find(".calendar-modal #modal_2_end_hour").val(calEvent.hour);
          $(".modal").find(".calendar-modal #").val(calEvent.begin_hour);
          $(".modal").find(".calendar-modal #modal_2_begin").val(calEvent.start.format('DD/MM/YYYY'));
          $(".modal").find(".calendar-modal #modal_2_end").val(calEvent.end.format('DD/MM/YYYY'));
          $(".choose_all_day_main input").val(calEvent.disabled_check);
          $(".calendar-modal .calendar-save-button").hide();
          $(".calendar-modal #time_choices").val(calEvent.vaxt_divi);
          $(".choose_icon_main span").prop("disabled", true);
          $(".slide_main").css("cursor", "default");
          $(".choose_icon_main span").html(calEvent.ikonka);
          $("input").attr("readonly", true);
          $("#end_hour_input").attr("readonly", true);
          $("#begin_hour_input").attr("readonly", true);
          $("#input_baslama_vaxti").prop("readonly", true);
          $("#input_bitme_vaxti").attr("readonly", true);
          $(".mekan_input input").attr("readonly", true);
          $(".choose_icon_main span").css("cursor", "default");
          $(".icon_slider").css("visibility", "hidden");
    
          // $(".choose").attr("readonly",true);
    
    
        }
      });
    
   
      
      $("#date_input").datetimepicker({ format: 'DD/MM/YYYY', locale: 'az' });
      $("#modal_2_begin").datetimepicker({ format: 'DD/MM/YYYY', locale: 'az' });
      $("#asim").datetimepicker({ format: 'HH:mm', locale: 'az' });
      $("#modal_2_end_hour").datetimepicker({ format: 'HH:mm', locale: 'az' });
      $("#modal_2_end").datetimepicker({ format: 'DD/MM/YYYY', locale: 'az' });
      
      
    
      $.get("/api/events/list/", function (data) {
        console.log(data)
        for (i = 0; i < data.length; i++) {
          eventData = {
            title: data[i].name,
            start: data[i].start,
            end: data[i].end,
            mekan: data[i].location,
            hour: data[i].end.split(' ')[1],
            begin_hour: data[i].start.split(' ')[1],
            disabled_check: true,
            bgcolor: data[i].category_bgcolor,
            textcolor: data[i].category_textcolor,
            id: data[i].id
            // vaxt_divi: $(".slide_main").text(),
            // ikonka: $(".choose_icon_main span").html()
          };
          $("#calendar-ms").fullCalendar("renderEvent", eventData, true); // stick? = tru
        }
      });
    
      //click to save "save"
      $(".calendar-modal #modal_2_save").on("click", function (event) {
        var title = $(".calendar-modal #event_title").val();
        var begin_gun, end_gun, bas_saat, bit_saat;
        begin_gun = $(".calendar-modal #modal_2_begin").val();
        end_gun = $(".calendar-modal #modal_2_end").val();
        bas_saat = $(".calendar-modal #asim").val();
        bit_saat = $(".calendar-modal #modal_2_end_hour").val();
        var date1, date2, d1, d2, m1, m2, y1, y2, a1, a2;
        date1 = moment($(".calendar-modal #modal_2_begin").val(), 'DD/MM/YYYY').format('MM/DD/YYYY');
        date2 = moment($(".calendar-modal #modal_2_end_hour").val(), 'DD/MM/YYYY').format('MM/DD/YYYY');
        a1 = date1.split('/');
        a2 = date2.split('/');
        d1 = a1[1];
        m1 = a1[0];
        y1 = a1[2];
        d2 = a2[1];
        m2 = a2[0];
        y2 = a2[2];
        var u2 = y2 + "" + m2 + "" + d2;
        var u1 = y1 + "" + m1 + "" + d1;
        if (title && begin_gun && end_gun && bas_saat && bit_saat && u2 > u1) {
          var eventData = {
            title: title,
            start: moment($(".calendar-modal #modal_2_begin").val(), 'DD/MM/YYYY').format('MM/DD/YYYY') + ' ' + $(".calendar-modal #asim").val(),
            end: moment($(".calendar-modal #modal_2_end").val(), 'DD/MM/YYYY').format('MM/DD/YYYY') + ' ' + $(".calendar-modal #modal_2_end_hour").val(),
            mekan: $(".calendar-modal #event_location").val(),
            hour: $("#end_hour_input").val(),
            begin_hour: $("#begin_hour_input").val(),
            disabled_check: $(".choose_all_day_main input").prop("disabled", true),
            vaxt_divi: $(".slide_main").text(),
            ikonka: $(".choose_icon_main span").html()
          };
          
          data = {
            'name': eventData.title,
            'category': 1,
            'description': '',
            'location': eventData.mekan,
            'start': moment($(".calendar-modal #modal_2_begin").val(), 'DD/MM/YYYY').format('YYYY-MM-DD') + 'T' + $('#modal_2_end_hour').val(),
            'end': moment($(".calendar-modal #modal_2_end").val(), 'DD/MM/YYYY').format('YYYY-MM-DD') + 'T' + $(".calendar-modal #modal_2_end_hour").val(),
          };
          $.ajax({
            type: 'POST',
            url: '/api/events/',
            headers: { "X-CSRFToken": getCookie('csrftoken') },
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(data),
            success: function (data) {
              console.log(eventData);
              
              $("#calendar-ms").fullCalendar("renderEvent", eventData, true); // stick? = tru
            },
            error: function (jqXhr, textStatus, errorMessage) {
              alert(errorMessage)
            }
          });
        }
        $("#calendar-ms").fullCalendar("unselect");
    
        // Clear modal inputs
        var date1, date2, d1, d2, m1, m2, y1, y2, a1, a2;
        date1 = moment($(".calendar-modal #modal_2_begin").val(), 'DD/MM/YYYY').format('MM/DD/YYYY');
        date2 = moment($(".calendar-modal #modal_2_end").val(), 'DD/MM/YYYY').format('MM/DD/YYYY');
        a1 = date1.split('/');
        a2 = date2.split('/');
        d1 = a1[1];
        m1 = a1[0];
        y1 = a1[2];
        d2 = a2[1];
        m2 = a2[0];
        y2 = a2[2];
        var u2 = y2 + "" + m2 + "" + d2;
        var u1 = y1 + "" + m1 + "" + d1;
        if (title && begin_gun && end_gun && bas_saat && bit_saat && u2 > u1) {
    
          $(".modal").modal("hide");
          var date1, date2, d1, d2, m1, m2, y1, y2, a1, a2;
          date1 = moment($(".calendar-modal #modal_2_begin").val(), 'DD/MM/YYYY').format('MM/DD/YYYY');
          date2 = moment($(".calendar-modal #modal_2_end").val(), 'DD/MM/YYYY').format('MM/DD/YYYY');
          a1 = date1.split('/');
          a2 = date2.split('/');
          d1 = a1[1];
          m1 = a1[0];
          y1 = a1[2];
          d2 = a2[1];
          m2 = a2[0];
          y2 = a2[2];
          console.log(u1 + " " + u2);
    
    
        }
        if (title && begin_gun && end_gun && bas_saat && bit_saat && u1 >= u2
          && $("#input_baslama_vaxti").val() != 0 && $("#input_bitme_vaxti").val() != 0)
          confirm("Başlama vaxtı bitmə vaxtına bərabər,və ya böyük olmamalıdır")
      });
    
    
      // $("textarea").autosize();
    
    });
    
    // CAlendar data save end
