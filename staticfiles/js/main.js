$(document).ready(function() {
  $('#calendar').fullCalendar({
    header: {
      left: 'prevYear,prev,next,nextYear, today',
      center: 'title',
      right: 'year,month,agendaWeek,agendaDay,listWeek'
    },
    buttonText:{
      prevYear: new moment().year()-1,
      nextYear: new moment().year()+1,
    },
    viewRender: function(view) {
      var y=moment($('#calendar').fullCalendar('getDate')).year();
      $(".fc-prevYear-button").text(y-1);
      $(".fc-nextYear-button").text(y+1);
    },
    locale:'az',
    navLinks: true, // can click day/week names to navigate views
    selectable: true,
    selectHelper: true,
    select: function(start, end) {
      var title = prompt('Event Title:');
      var eventData;
      if (title) {
        eventData = {
          title: title,
          start: start,
          end: end
        };
        $('#calendar').fullCalendar('renderEvent', eventData, true); // stick? = true
      }
      $('#calendar').fullCalendar('unselect');
    },
    editable: true,
    eventLimit: true, // allow "more" link when too many events
    events: [
      {
        title: 'All Day Event',
        start: '2019-01-01'
      },
      {
        title: 'Long Event',
        start: '2019-01-07',
        end: '2019-01-10'
      },
      {
        id: 999,
        title: 'Repeating Event',
        start: '2019-01-09T16:00:00'
      },
      {
        id: 999,
        title: 'Repeating Event',
        start: '2019-01-16T16:00:00'
      },
      {
        title: 'Conference',
        start: '2019-01-11',
        end: '2019-01-13'
      },
      {
        title: 'Meeting',
        start: '2019-01-12T10:30:00',
        end: '2019-01-12T12:30:00'
      },
      {
        title: 'Lunch',
        start: '2019-01-12T12:00:00'
      },
      {
        title: 'Meeting',
        start: '2019-01-12T14:30:00'
      },
      {
        title: 'Happy Hour',
        start: '2019-01-12T17:30:00'
      },
      {
        title: 'Dinner',
        start: '2019-01-12T20:00:00'
      },
      {
        title: 'Birthday Party',
        start: '2019-01-13T07:00:00'
      },
      {
        title: 'Click for Google',
        url: 'http://google.com/',
        start: '2019-01-28'
      }
    ]
  });
});
 $(document).ready(function(){
  $("#id_phone_number").mask("xxx-xx-xx");
   });   