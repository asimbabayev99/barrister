$(document).ready(function() {
  $("#calendar-ms").fullCalendar({
    header: {
      left: "prevYear,prev,next,nextYear, today",
      center: "title",
      right: "month,agendaWeek,agendaDay"
    },
    buttonText: {
        prevYear: new moment().year() - 1,
        nextYear: new moment().year() + 1
    },
    viewRender: function(view) {
        var y = moment($('#calendar-ms').fullCalendar('getDate')).year();
        $(".fc-prevYear-button").text(y-1),
        $(".fc-nextYear-button").text(y+1)
    },
    defaultView: "month",
    navLinks: true, // can click day/week names to navigate views
    selectable: true,
    selectHelper: true,
    editable: true,
    eventLimit: true, // allow "more" link when too many events

    select: function(start, end) {
      // Display the modal.
      // You could fill in the start and end fields based on the parameters
      $(".modal").modal("show");
      $(".modal")
        .find("#event_name_input")
        .val("");
      $(".modal")
        .find("#input_baslama_vaxti")
        .val("");
      $(".modal")
        .find("#input_bitme_vaxti")
        .val("");
      $("#save-event").show();
      $("input").prop("readonly", false);
    },

    eventRender: function(event, element) {
      //dynamically prepend close button to event
      element
        .find(".fc-content")
        .prepend("<span class='closeon material-icons'>x&nbsp</span>");
      element.find(".closeon").on("click", function() {
        $("#calendar-ms").fullCalendar("removeEvents", event._id);
      });
    },

    eventClick: function(calEvent, jsEvent) {
      // Display the modal and set event values.
      $(".modal").modal("show");
      $(".modal")
        .find("#event_name_input")
        .val(calEvent.title);
      $(".modal")
        .find("#input_baslama_vaxti")
        .val(calEvent.start.format('DD/MMM/YYYY HH:MM'));
      $(".modal")
        .find("#input_bitme_vaxti")
        .val(calEvent.end.format('DD/MMM/YYYY HH:MM'));
      $("#save-event").hide();
      $("input").prop("readonly", true);
    }
  });

  // Bind the dates to datetimepicker.
  // $("#input_baslama_vaxti, #input_bitme_vaxti").datetimepicker({format: 'DD/MMM/YYYY HH:MM'});
  // $("#input_baslama_vaxti ").datetimepicker({format:'L LT'});
  // $("#input_bitme_vaxti").datetimepicker({format:'L LT'});

  // $("#input_baslama_vaxti").datetimepicker({locale:'az'});
  // $("#input_bitme_vaxti").datetimepicker({locale:'az'});
   $("#input_baslama_vaxti ").datetimepicker({ format: 'DD/MMM/YYYY, HH:MM'});
  $("#input_bitme_vaxti").datetimepicker({ format: 'DD/MMM/YYYY, HH:MM'});
  
 
  

  //click to save "save"
  $("#save-event").on("click", function(event) {
    var title = $("#event_name_input").val();
    if (title) {
      var eventData = {
        title: title,
        start: $("#input_baslama_vaxti").val(),
        end: $("#input_bitme_vaxti").val()
      };
      $("#calendar-ms").fullCalendar("renderEvent", eventData, true); // stick? = true
    }
    $("#calendar-ms").fullCalendar("unselect");

    // Clear modal inputs
    $(".modal")
      .find("input")
      .val("");
    // hide modal
    $(".modal").modal("hide");
  });

  // $("textarea").autosize();
});
