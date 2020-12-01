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
  $(".beginChoices .begin-time-choices").click(function () {
    $(".beginChoices #time_input").text($(this).text())
    // console.log($(".beginChoices #time_input").text())
  });
  $(".intervalChoices .begin-time-choices").click(function () {
    $(".intervalChoices #time_input").attr($(this).attr('value'))
    $(".intervalChoices #time_input").text($(this).text())
  });
  $("#profile .times-div-3 .times-2 .begin-time-choices").click(function () {
    $(".times-div-3  .remember-timer").text($(this).text())
  });
  $(".times-div-3 #chosen_1 .begin-time-choices").click(function () {
    $(".times-div-3 .client-status").text($(this).text())
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
  $(".icons-contents-main .icons").click(function () {
    var icon = $(this);
    $(".icon-content").attr('data-id', icon.attr('data-id'))
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
      $(".event_save").modal("show");
      $(".modal").find(".calendar-modal #event_title").val("");
      $(".modal").find(".calendar-modal .icon-content").html('<i class="fas fa-angle-down"></i>');
      $(".modal").find(".calendar-modal input").val("");
      $(".modal").find(".calendar-modal input").attr("disabled", false);
      $(".modal").find(".calendar-modal #modal_2_save").css({
        display: "inline-block"
      });
      $(".modal").find(".calendar-modal #whole_day_checkbox").prop("checked", false);
      $(".modal").find(".calendar-modal #profile .dropdown-menu").css({
        visibility: "visible",
        opacity: "1"
      });
      $(".modal").find(".calendar-modal .auto_name").css({
        display: "none"
      });
      $(".modal").find(".calendar-modal .auto-information").css({
        display: "none"
      });
      $(".modal").find(".calendar-modal #name_input").css({
        display: "block"
      });
      $(".modal").find(".calendar-modal #email_input").css({
        display: "block"
      });
      $(".modal").find(".calendar-modal #phone_input").css({
        display: "block"
      });
      $(".modal").find(".calendar-modal #address_input").css({
        display: "block"
      });
      
      $(".modal").find(".calendar-modal .validation-reserv").text("");
      $(".modal").find(".calendar-modal .validation-interval").text("");
      $(".modal").find(".calendar-modal .text-area-modal").val("");
      $(".modal").find(".calendar-modal .auto_name_2").css("display", "none");
      $(".modal").find(".calendar-modal .alert").css("display", "none");

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
      console.log(calEvent)
      if (calEvent.type == "event") {
        $('#updateEvent').modal('show');
      } else if (calEvent.type == "appointment") {
        $('#updateAppointment').modal('show');
      }
      // Display the modal and set event values.
      // $(".modal").modal("show");
      // $(".modal").find(".calendar-modal #profile #event_title").val(calEvent.title);
      // $(".modal").find(".calendar-modal #profile #event_location").val(calEvent.mekan);
      // $(".modal").find(".calendar-modal #profile #modal_2_end_hour").val(calEvent.hour);
      // $(".modal").find(".calendar-modal #profile #modal_2_begin_hour").val(calEvent.begin_hour);
      // $(".modal").find(".calendar-modal #profile #modal_2_begin").val(calEvent.start.format('DD/MM/YYYY'));
      // $(".modal").find(".calendar-modal #profile #modal_2_end").val(calEvent.end.format('DD/MM/YYYY'));
      // $(".modal").find(".calendar-modal #profile input").attr("disabled", true);
      // $(".modal").find(".calendar-modal #profile .dropdown-menu").css({
      //   visibility: "hidden",
      //   opacity: "0"
      // });
      // $(".modal").find(".calendar-modal #modal_2_save").css({
      //   display: "none"
      // });

    }
  });



  $("#date_input").datetimepicker({ format: 'DD/MM/YYYY', locale: 'az' });
  $("#modal_2_begin").datetimepicker({ format: 'DD/MM/YYYY', locale: 'az' });
  $("#asim").datetimepicker({ format: 'HH:mm', locale: 'az' });
  $("#modal_2_end_hour").datetimepicker({ format: 'HH:mm', locale: 'az' });
  $("#modal_2_end").datetimepicker({ format: 'DD/MM/YYYY', locale: 'az' });


  // load event to calendar
  $.get("/api/events/list/", function (data) {
    // console.log(data)
    for (i = 0; i < data.length; i++) {
      eventData = {
        type: 'event',
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
      };
      $("#calendar-ms").fullCalendar("renderEvent", eventData, true); // stick? = tru
    }
  });

  // load appointments to calendar
  $.get("/api/appointments/list/", function (data) {
    console.log(data)
    for (i = 0; i < data.length; i++) {
      eventData = {
        start: data[i].start,
        end: data[i].end,
        address: data[i].address,
        phone : data[i].phone,
        id: data[i].id,
        type: 'appointment'
      };
      $("#calendar-ms").fullCalendar("renderEvent", eventData, true); // stick? = tru
    }
  });

  //click to save "save"
 
  $(".calendar-modal #modal_2_save").on("click", function (event) {
    var title = $(".calendar-modal #event_title").val();
    var begin_gun, end_gun, bas_saat, bit_saat, location_modal;
    begin_gun = $(".calendar-modal #modal_2_begin").val();
    end_gun = $(".calendar-modal #modal_2_end").val();
    bas_saat = $(".calendar-modal #asim").val();
    location_modal = $("#event_location").val();
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
    if (title && begin_gun && end_gun && bas_saat && bit_saat && u2 > u1 && location_modal) {
      var eventData = {
        title: title,
        start: moment($(".calendar-modal #modal_2_begin").val(), 'DD/MM/YYYY').format('MM/DD/YYYY') + ' ' + $(".calendar-modal #asim").val(),
        end: moment($(".calendar-modal #modal_2_end").val(), 'DD/MM/YYYY').format('MM/DD/YYYY') + ' ' + $(".calendar-modal #modal_2_end_hour").val(),
        mekan: $(".calendar-modal #event_location").val(),
        hour: $(".calendar-modal #profile #modal_2_end_hour").val(),
        begin_hour: $(".calendar-modal #profile #modal_2_begin_hour").val(),
        disabled_check: $(".choose_all_day_main input").prop("disabled", true),
        vaxt_divi: $(".slide_main").text(),
        ikonka: $(".choose_icon_main span").html(),
        category: $('.icon-content').attr('data-id'),
      };

      data = {
        'name': eventData.title,
        'category': eventData.category,
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
    if (title && begin_gun && end_gun && bas_saat && bit_saat && u2 > u1 && location_modal) {
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


  $('.calendar-save-button').on("click", function () {
    let beginingTime = $(".validation-date").val().split("/");
    let timeInterval = parseInt($(".validation-interval").text().split(" ")[0])
    start_date = new Date(beginingTime[2] + "-" + beginingTime[1] + "-" + beginingTime[0] + " " + $(".beginChoices #time_input").text().trim()+":00");
    end_date =  new Date(start_date.getTime() + timeInterval*60000);
        
    var data = {
      'contact': {
        'name': $('#name_input').val(),
        'email': $('#email_input').val(),
        'phone': $('#phone_input').val(),
        'address': $('#address_input').val()
      },
      'start': start_date.toISOString(),
      'end': end_date.toISOString(),
      'status': $('.validation_input_meeting').text(),
      'detail': $('#detail_input').val() 
    }
    console.log(data)
    $.ajax({
      type: 'POST',
      url: '/api/appointments/',
      headers: { "X-CSRFToken": getCookie('csrftoken') },
      contentType: "application/json; charset=utf-8",
      data: JSON.stringify(data),
      success: function (data) {
        console.log(data);
        // $("#calendar-ms").fullCalendar("renderEvent", eventData, true); // stick? = tru
      },
      error: function (data) {
        console.log(data)
      }
    }); 

  })

  // $("textarea").autosize();

});

// CAlendar data save end


// Modal 2 validation begin
$(document).ready(function () {
  $("#modal_2_save").click(function () {
    if ($("#event_title").val().length === 0) {
      $("#name_alert_modal_2").css("display", "block");
    } else {

      $("#name_alert_modal_2").css("display", "none");
    }
    if ($("#event_location").val().length === 0) {
      $("#event_location_alert").css({
        display: "block"
      })
    }
    else {
      $("#event_location_alert").css({
        display: "none"
      });
    }
  })
  $("#event_title").keyup(function () {
    if ($(this).val().length > 0) {
    } else {

      $("#name_alert_modal_2").css("display", "block");
    }
  })
})


// Modal 2 validation end



//  Auto complete modal in 1 begin
$(document).ready(function () {
  $("#name_input").keyup(function () {
    if ($(this).val() !== 0) {
      $(".auto_name").css({
        display: "block"
      });
      if ($(this).val().length === 0) {
        $(".auto_name").css({
          display: "none"
        });
      }
    }
  });

  $(".auto_name").click(function () {
    $(".auto_name_2").css({
      display: "block"
    });
    $(this).css({
      display: "none"
    });
    $("#name_input, #email_input,#phone_input,#address_input").css({
      display: "none"
    })
  });


  $(".close-information").click(function () {
    $(".calendar-modal #name_input").css({
      display: "block"
    });
    $(".calendar-modal #address_input").css({
      display: "block"
    });
    $(".calendar-modal .auto_name_2").css({
      display: "none"
    });
    $(".calendar-modal #email_input, #phone_input").css({
      display: "block"
    })
  })


})

//  Auto complete modal in 1 end