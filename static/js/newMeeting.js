$(document).ready(function () {
  $("#calendar-ms").fullCalendar({
    customButtons: {
      printButton: {
        text: "Çap et",
        click: function () {
          window.print();
        },
      },
    },

    header: {
      left: "prevYear,prev,next,nextYear",
      center: "title",
      right: "today,month,agendaWeek,agendaDay,printButton",
    },
    buttonText: {
      prevYear: new moment().year() - 1,
      nextYear: new moment().year() + 1,
    },
    viewRender: function (view) {
      var y = moment($("#calendar-ms").fullCalendar("getDate")).year();
      $(".fc-prevYear-button").text(y - 1),
        $(".fc-nextYear-button").text(y + 1);
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
      $(".modal").find(".add_event_name_main input").val("");
      $(".choose_all_day_main input").attr("disabled", false);
      $("#save-event").show();
    },
    eventRender: function (event, element) {
      if (event.bgcolor) {
        element.css("background-color", event.bgcolor);
        element.css("color", event.textcolor);
      }
      //dynamically prepend close button to event
      element
        .find(".fc-content")
        .prepend(
          "<span data-id='" +
            event.id +
            "' class='closeon material-icons'>x&nbsp</span>"
        );
      element.find(".closeon").on("click", function () {
        id = $(this).attr("data-id");
        $.ajax({
          type: "DELETE",
          url: "/api/events/" + event.id + "/",
          headers: { "X-CSRFToken": getCookie("csrftoken") },
          success: function (data) {
            $("#calendar-ms").fullCalendar("removeEvents", event._id);
          },
          error: function (jqXhr, textStatus, errorMessage) {
            alert(errorMessage);
          },
        });
        // $("#calendar-ms").fullCalendar("removeEvents", event._id);
      });
    },

    eventClick: function (calEvent, jsEvent) {
      // Display the modal and set event values.
      $(".modal").modal("show");
      $(".add_event_name_main input").attr("readonly", true);
      $(".modal").find(".add_event_name_main input").val(calEvent.meetingName);
      $(".modal").find(".mekan_input input").val(calEvent.meetingLocation);
      $(".modal")
        .find("#input_baslama_vaxti")
        .val(calEvent.start.format("DD/MM/YYYY"));
      $(".modal")
        .find("#input_bitme_vaxti")
        .val(calEvent.end.format("DD/MM/YYYY"));
      $("#save-event").hide();
      $(".slide_main").html(calEvent.vaxt_divi);
      $(".select_bottom").css("visibility", "hidden");
      $(".choose_icon_main span").prop("disabled", true);
      if ($(".mekan_input input").val() == 0) {
        $(".mekan_input input").val("Məkan yoxdur");
      }

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
    },
  });

  $.get("/api/events/list/", function (data) {
    console.log(data);
    for (i = 0; i < data.length; i++) {
      eventData = {
        title: data[i].name,
        start: data[i].start,
        end: data[i].end,
        mekan: data[i].location,
        hour: data[i].end.split(" ")[1],
        begin_hour: data[i].start.split(" ")[1],
        disabled_check: true,
        bgcolor: data[i].category_bgcolor,
        textcolor: data[i].category_textcolor,
        id: data[i].id,
        // vaxt_divi: $(".slide_main").text(),
        // ikonka: $(".choose_icon_main span").html()
      };
      $("#calendar-ms").fullCalendar("renderEvent", eventData, true); // stick? = tru
    }
  });

  $("#save-event").on("click", function (event) {
    
    var meetingName,meetingMail, meetingPhone, meetingLocation, meetingDay, meetingBeginHour, meetingEndHour, meetingStatus, meetingNote;
    meetingName = $("#home #name_input").val();
    meetingMail = $("#home #email_input").val();
    meetingPhone = $("#home #phone_input").val();
    meetingLocation = $("#home #address_input").val();
    meetingDay = $("#home #date_input");
    meetingBeginHour = $("#home .validation-time").text();
    meetingEndHour = $("#home .validation-interval").text();
    meetingStatus = $("#home .validation-reserv").text();
    meetingNote = $("#home .text-area-modal").val();

    var date1, date2, d1, d2, m1, m2, y1, y2, a1, a2;
    var meetinBeginTime, meetingEndTime;
    meetinBeginTime = moment($("#input_baslama_vaxti").val(), "DD/MM/YYYY").format(
      "MM/DD/YYYY"
    );
    
    a1 = date1.split("/");
    a2 = date2.split("/");
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
        end:
          moment($("#input_bitme_vaxti").val(), "DD/MM/YYYY").format(
            "MM/DD/YYYY"
          ) +
          " " +
          $("#end_hour_input").val(),
        start:
          moment($("#input_baslama_vaxti").val(), "DD/MM/YYYY").format(
            "MM/DD/YYYY"
          ) +
          " " +
          $("#begin_hour_input").val(),
        mekan: $(".mekan_main input").val(),
        hour: $("#end_hour_input").val(),
        begin_hour: $("#begin_hour_input").val(),
        disabled_check: $(".choose_all_day_main input").prop("disabled", true),
        vaxt_divi: $(".slide_main").text(),
        ikonka: $(".choose_icon_main span").html(),
      };
      data = {
        name: eventData.title,
        category: 1,
        description: "",
        location: eventData.mekan,
        start:
          moment($("#input_baslama_vaxti").val(), "DD/MM/YYYY").format(
            "YYYY-MM-DD"
          ) +
          "T" +
          $("#begin_hour_input").val(),
        end:
          moment($("#input_bitme_vaxti").val(), "DD/MM/YYYY").format(
            "YYYY-MM-DD"
          ) +
          "T" +
          $("#end_hour_input").val(),
      };
      $.ajax({
        type: "POST",
        url: "/api/events/",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(data),
        success: function (data) {
          $("#calendar-ms").fullCalendar("renderEvent", eventData, true); // stick? = tru
        },
        error: function (jqXhr, textStatus, errorMessage) {
          alert(errorMessage);
        },
      });
    }
    $("#calendar-ms").fullCalendar("unselect");

    // Clear modal inputs
    var date1, date2, d1, d2, m1, m2, y1, y2, a1, a2;
    date1 = moment($("#input_baslama_vaxti").val(), "DD/MM/YYYY").format(
      "MM/DD/YYYY"
    );
    date2 = moment($("#input_bitme_vaxti").val(), "DD/MM/YYYY").format(
      "MM/DD/YYYY"
    );
    a1 = date1.split("/");
    a2 = date2.split("/");
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
      date1 = moment($("#input_baslama_vaxti").val(), "DD/MM/YYYY").format(
        "MM/DD/YYYY"
      );
      date2 = moment($("#input_bitme_vaxti").val(), "DD/MM/YYYY").format(
        "MM/DD/YYYY"
      );
      a1 = date1.split("/");
      a2 = date2.split("/");
      d1 = a1[1];
      m1 = a1[0];
      y1 = a1[2];
      d2 = a2[1];
      m2 = a2[0];
      y2 = a2[2];
      console.log(u1 + " " + u2);
    }
    if (
      title &&
      begin_gun &&
      end_gun &&
      bas_saat &&
      bit_saat &&
      u1 >= u2 &&
      $("#input_baslama_vaxti").val() != 0 &&
      $("#input_bitme_vaxti").val() != 0
    )
      confirm("Başlama vaxtı bitmə vaxtına bərabər,və ya böyük olmamalıdır");
  });

});
