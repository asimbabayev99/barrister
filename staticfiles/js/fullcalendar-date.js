$(document).ready(function () {
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


      $(".modal").find("#event_name_input").val("");
      $(".modal").find("#choose_icon_button").html('<i class="far fa-bell"></i>&downarrow;');
      $(".modal").find("#select_box_baslig").val($("#vaxt_secimi").html());
      $(".checkbox_input_modal").attr("disabled", false);
      $(".modal").find("#input_baslama_vaxti").val("");
      $(".modal").find("#input_bitme_vaxti").val("");
      $(".modal").find("#location_input").val("");
      $(".modal").find("#begin_hour_input").val("");
      $(".modal").find("#end_hour_input").val("");
      $("#select_box_alt_hisse").css("visibility", "initial");
      $("#select_box_alt_hisse").css("display", "none");
      $("#select_box_baslig").text("Vaxt seçin");
      $("#begin_hour_input").prop("disabled", false);
      $("#end_hour_input").prop("disabled", false);
      $("#save-event").show();
      $("#select_box_baslig").css("cursor", "pointer");
      $("#choose_icon_button").prop("disabled", false);
      $(".checkbox_input_modal").prop("checked", false);
      $("input").prop("readonly", false);
      $("#hide_butun_gun").show();
      $("#hide_butun_gun_1").show();

    },

    eventRender: function (event, element) {
      //dynamically prepend close button to event
      element.find(".fc-content").prepend("<span class='closeon material-icons'>x&nbsp</span>");
      element.find(".closeon").on("click", function () {
        $("#calendar-ms").fullCalendar("removeEvents", event._id);
      });
    },

    eventClick: function (calEvent, jsEvent) {
      // Display the modal and set event values.
      $(".modal").modal("show");

      $(".modal").find("#event_name_input").val(calEvent.title);
      $(".modal").find("#location_input").val(calEvent.mekan);
      $(".modal").find("#end_hour_input").val(calEvent.hour);
      $(".modal").find("#begin_hour_input").val(calEvent.begin_hour);
      $(".modal").find("#input_baslama_vaxti").val(calEvent.start.format('DD/MM/YYYY'));
      $(".modal").find("#input_bitme_vaxti").val(calEvent.end.format('DD/MM/YYYY'));
      $(".checkbox_input_modal").val(calEvent.disabled_check);
      $("#save-event").hide();
      $("#select_box_baslig").html(calEvent.vaxt_divi);
      $("#select_box_alt_hisse").css("visibility", "hidden");
      $("#choose_icon_button").prop("disabled", true);
      if ($("#location_input").val() == 0) {
        $("#location_input").val("Məkan yoxdur");
      };
      if ("#")
        $("#select_box_baslig").css("cursor", "default");
      $("#choose_icon_button").html(calEvent.ikonka);
      $("input").prop("readonly", true);


    }
  });

  // Bind the dates to datetimepicker.
  // $("#input_baslama_vaxti, #input_bitme_vaxti").datetimepicker({format: 'DD/MMM/YYYY HH:MM'});
  // $("#input_baslama_vaxti ").datetimepicker({format:'L LT'});
  // $("#input_bitme_vaxti").datetimepicker({format:'L LT'});

  // $("#input_baslama_vaxti").datetimepicker({locale:'az'});
  // $("#input_bitme_vaxti").datetimepicker({locale:'az'});
  $("#input_baslama_vaxti").datetimepicker({ format: 'DD/MM/YYYY', locale: 'az' });
  $("#input_bitme_vaxti").datetimepicker({ format: 'DD/MM/YYYY', locale: 'az' });
  $("#begin_hour_input").datetimepicker({ format: 'HH:mm' });
  $("#end_hour_input").datetimepicker({ format: 'HH:mm' });



  //click to save "save"
  $("#save-event").on("click", function (event) {
    var title = $("#event_name_input").val();
    var begin_gun, end_gun, bas_saat, bit_saat;
    begin_gun = $("#input_baslama_vaxti").val();
    end_gun = $("#input_bitme_vaxti").val();
    bas_saat = $("#begin_hour_input").val();
    bit_saat = $("#end_hour_input").val();
    if (title && begin_gun && end_gun && bas_saat && bit_saat && $("#input_baslama_vaxti").val() < $("#input_bitme_vaxti").val()) {
      var eventData = {
        title: title,
        // start: moment($("#input_baslama_vaxti").val()).utc().format('DD/MM/YYYY')+' '+$("#begin_hour_input").val(),
        // end: moment($("#input_bitme_vaxti").val()).utc().format('DD/MM/YYYY')+' '+$("#end_hour_input").val(),
        // start: $("#input_baslama_vaxti").val()+' '+$("#begin_hour_input").val(),
        // end: $("#input_bitme_vaxti").val()+' '+$("#end_hour_input").val(),
        start: moment($("#input_baslama_vaxti").val(), 'DD/MM/YYYY').format('MM/DD/YYYY') + ' ' + $("#begin_hour_input").val(),
        end: moment($("#input_bitme_vaxti").val(), 'DD/MM/YYYY').format('MM/DD/YYYY') + ' ' + $("#end_hour_input").val(),
        mekan: $("#location_input").val(),
        hour: $("#end_hour_input").val(),
        begin_hour: $("#begin_hour_input").val(),
        disabled_check: $(".checkbox_input_modal").prop("disabled", true),
        vaxt_divi: $("#select_box_baslig").text(),
        ikonka: $("#choose_icon_button").html()
      };
      $.ajax({
        type: 'POST',
        url: '/api/events/',
        data: {
          'name': eventData.title,
          'description': '',
          'location': eventData.mekan, 
          'start': eventData.start,
          'end': eventData.end,
        },
        success: function (data) {
          $("#calendar-ms").fullCalendar("renderEvent", eventData, true); // stick? = tru
        }
      });
    }
    $("#calendar-ms").fullCalendar("unselect");

    // Clear modal inputs

    if (title && begin_gun && end_gun && bas_saat && bit_saat && $("#input_baslama_vaxti").val() < $("#input_bitme_vaxti").val()) {

      $(".modal").modal("hide");

    }
    if (title && begin_gun && end_gun && bas_saat && bit_saat && $("#input_baslama_vaxti").val() >= $("#input_bitme_vaxti").val() && $("#input_baslama_vaxti").val() != 0 && $("#input_bitme_vaxti").val() != 0) confirm("Başlama vaxtı bitmə vaxtına bərabər,və ya böyük olmamalıdır")
  });


  // $("textarea").autosize();

});

function check() {
  if ($(".checkbox_input_modal").is(":checked")) {
    $("#end_hour_input").attr("disabled", true);
    $("#begin_hour_input").attr("disabled", true);
    $("#begin_hour_input").val("00:00");
    $("#end_hour_input").val("23:59");

    // $("#end_hour_input").hide();
    // $("#input_baslama_vaxti").css("width","185px");
    // $("#input_bitme_vaxti").css("width","185px");
    // $("#begin_hour_input").hide();
    $(".modal [class|=bootstrap]").css({ "visibility": " hidden" });

  }
  else {
    $("#end_hour_input").attr("disabled", false);
    $("#begin_hour_input").attr("disabled", false);
    // $("#input_baslama_vaxti").css("width","120px");
    // $("#input_bitme_vaxti").css("width","120px");
    $("#begin_hour_input").val("");
    $("#end_hour_input").val("");
    //Code to disable checkbox after checked

  };
}