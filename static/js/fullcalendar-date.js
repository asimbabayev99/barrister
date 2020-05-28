$(document).ready(function() {
  
  $("#calendar-ms").fullCalendar({
    customButtons: {
      printButton: {
        text: 'Çap et',
        click: function() {
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

                   
      $(".modal").find(".add_event_name_main input").val("");
      // $(".modal").find(".choose_icon_main span").html('<i class="far fa-bell"></i>&downarrow;');
      // $(".modal").find("#select_box_baslig").val($("#vaxt_secimi").html());
      $(".choose_all_day_main input").attr("disabled",false);
      $(".modal").find("#input_baslama_vaxti").val("");
      $(".modal").find("#input_bitme_vaxti").val("");
      $(".modal").find(".mekan_input input").val("");
      $(".modal").find("#begin_hour_input").val("");
      $(".modal").find("#end_hour_input").val(""); 
      $(".select_bottom").css("visibility","initial");
      $(".select_bottom").css("display","none");
      $(".slide_main").text("Vaxt seçin");
      $("#begin_hour_input").prop("disabled",false);
      $("#end_hour_input").prop("disabled",false);
      $("#save-event").show();
      $(".slide_main").css("cursor","pointer");
      $(".choose_icon_main span").prop("disabled", false);
      $(".choose_all_day_main input").prop("checked",false);
      $(".modal input").prop("readonly", false);
      $(".choose_icon_main span").css("cursor","pointer");
      $(".icon_slider").css("visibility","visible");
      $(".icon_slider").css("display","none");
      $(".less_icons").css("display","none");
      $(".less_main").css("display","none");
      $(".show_more").slideDown();
    },
    
    eventRender: function(event, element) {
      //dynamically prepend close button to event
      element.find(".fc-content").prepend("<span class='closeon material-icons'>x&nbsp</span>");
      element.find(".closeon").on("click", function() {
        $("#calendar-ms").fullCalendar("removeEvents", event._id);
      });
    },
    
    eventClick: function(calEvent, jsEvent) {
      // Display the modal and set event values.
      $(".modal").modal("show");
      $(".add_event_name_main input").attr("readonly",true);
      $(".modal").find(".add_event_name_main input").val(calEvent.title);
      $(".modal").find(".mekan_input input").val(calEvent.mekan);  
      $(".modal").find("#end_hour_input").val(calEvent.hour);
      $(".modal").find("#begin_hour_input").val(calEvent.begin_hour);
      $(".modal").find("#input_baslama_vaxti").val(calEvent.start.format('DD/MM/YYYY'));
      $(".modal").find("#input_bitme_vaxti").val(calEvent.end.format('DD/MM/YYYY'));
      $(".choose_all_day_main input").val(calEvent.disabled_check);
      $("#save-event").hide();
      $(".slide_main").html(calEvent.vaxt_divi);
      $(".select_bottom").css("visibility","hidden");
      $(".choose_icon_main span").prop("disabled", true);
      if($(".mekan_input input").val()==0) {
        $(".mekan_input input").val("Məkan yoxdur");
      };
      
      $(".slide_main").css("cursor","default");
      $(".choose_icon_main span").html(calEvent.ikonka);
      $("input").attr("readonly", true);
      $("#end_hour_input").attr("readonly",true);
      $("#begin_hour_input").attr("readonly",true);
      $("#input_baslama_vaxti").prop("readonly",true);
      $("#input_bitme_vaxti").attr("readonly",true);
      $(".mekan_input input").attr("readonly",true);
      $(".choose_icon_main span").css("cursor","default");
      $(".icon_slider").css("visibility","hidden");
      
      // $(".choose").attr("readonly",true);
      

    }
  });

  // Bind the dates to datetimepicker.
  // $("#input_baslama_vaxti, #input_bitme_vaxti").datetimepicker({format: 'DD/MMM/YYYY HH:MM'});
  // $("#input_baslama_vaxti ").datetimepicker({format:'L LT'});
  // $("#input_bitme_vaxti").datetimepicker({format:'L LT'});

  // $("#input_baslama_vaxti").datetimepicker({locale:'az'});
  // $("#input_bitme_vaxti").datetimepicker({locale:'az'});
   $("#input_baslama_vaxti").datetimepicker({ format: 'DD/MM/YYYY',locale:'az'});
  $("#input_bitme_vaxti").datetimepicker({ format: 'DD/MM/YYYY',locale:'az'});
  $("#begin_hour_input").datetimepicker({ format: 'HH:mm'});
  $("#end_hour_input").datetimepicker({ format: 'HH:mm'});
  
  

  //click to save "save"
  $("#save-event").on("click", function(event) {
    console.log('1- '+$("#input_baslama_vaxti").val()+'s<- ->e'+$("#input_bitme_vaxti").val())
    var title = $(".add_event_name_main input").val();
    var begin_gun,end_gun,bas_saat,bit_saat;
    begin_gun = $("#input_baslama_vaxti").val();
    end_gun = $("#input_bitme_vaxti").val();
    bas_saat = $("#begin_hour_input").val();
    bit_saat = $("#end_hour_input").val();
    var date1,date2,d1,d2,m1,m2,y1,y2,a1,a2;
    date1= moment($("#input_baslama_vaxti").val(), 'DD/MM/YYYY').format('MM/DD/YYYY');
    date2=moment($("#input_bitme_vaxti").val(), 'DD/MM/YYYY').format('MM/DD/YYYY');
    a1=date1.split('/');
    a2=date2.split('/');
    d1=a1[1];
    m1=a1[0];
    y1=a1[2];
    d2=a2[1];
    m2=a2[0];
    y2=a2[2];
    var u2=y2 + "" +m2+"" + d2;
    var u1= y1+""+m1+""+d1;
    if (title && begin_gun && end_gun && bas_saat && bit_saat && u2>u1 ) {
      var eventData = {
        title: title,

        // start: moment($("#input_baslama_vaxti").val()).utc().format('DD/MM/YYYY')+' '+$("#begin_hour_input").val(),
        // end: moment($("#input_bitme_vaxti").val()).utc().format('DD/MM/YYYY')+' '+$("#end_hour_input").val(),
        // start: $("#input_baslama_vaxti").val()+' '+$("#begin_hour_input").val(),
        // end: $("#input_bitme_vaxti").val()+' '+$("#end_hour_input").val(),
        start:moment($("#input_baslama_vaxti").val(), 'DD/MM/YYYY').format('MM/DD/YYYY')+' '+$("#begin_hour_input").val(),      
        end:moment($("#input_bitme_vaxti").val(), 'DD/MM/YYYY').format('MM/DD/YYYY')+' '+$("#end_hour_input").val(),      
        mekan: $(".mekan_main input").val(),
        hour : $("#end_hour_input").val(),
        begin_hour : $("#begin_hour_input").val(),
        disabled_check:$(".choose_all_day_main input").prop("disabled",true),
        vaxt_divi:$(".slide_main").text(),
        ikonka:$(".choose_icon_main span").html()
      };
      $("#calendar-ms").fullCalendar("renderEvent", eventData, true); // stick? = true
    }
    $("#calendar-ms").fullCalendar("unselect");

    // Clear modal inputs
    var date1,date2,d1,d2,m1,m2,y1,y2,a1,a2;
    date1= moment($("#input_baslama_vaxti").val(), 'DD/MM/YYYY').format('MM/DD/YYYY');
    date2=moment($("#input_bitme_vaxti").val(), 'DD/MM/YYYY').format('MM/DD/YYYY');
    a1=date1.split('/');
    a2=date2.split('/');
    d1=a1[1];
    m1=a1[0];
    y1=a1[2];
    d2=a2[1];
    m2=a2[0];
    y2=a2[2];
    var u2=y2 + "" +m2+"" + d2;
    var u1= y1+""+m1+""+d1;
    if(u2>u1 ) {
     
    $(".modal").modal("hide");
    var date1,date2,d1,d2,m1,m2,y1,y2,a1,a2;
    date1= moment($("#input_baslama_vaxti").val(), 'DD/MM/YYYY').format('MM/DD/YYYY');
    date2=moment($("#input_bitme_vaxti").val(), 'DD/MM/YYYY').format('MM/DD/YYYY');
    a1=date1.split('/');
    a2=date2.split('/');
    d1=a1[1];
    m1=a1[0];
    y1=a1[2];
    d2=a2[1];
    m2=a2[0];
    y2=a2[2];
    console.log(u1 + " " + u2);
    

    }
    if (title && begin_gun && end_gun && bas_saat && bit_saat && u1>=u2
    && $("#input_baslama_vaxti").val()!=0 && $("#input_bitme_vaxti").val()!=0) 
    confirm("Başlama vaxtı bitmə vaxtına bərabər,və ya böyük olmamalıdır")
  });
  

  // $("textarea").autosize();

});

function check() {
  if($(".choose_all_day_main input").is(":checked")){
    $("#end_hour_input").attr("disabled",true);
    $("#begin_hour_input").attr("disabled",true);
    $("#begin_hour_input").val("00:00");
    $("#end_hour_input").val("23:59");
    
    // $("#end_hour_input").hide();
    // $("#input_baslama_vaxti").css("width","185px");
    // $("#input_bitme_vaxti").css("width","185px");
    // $("#begin_hour_input").hide();
    $(".modal [class|=bootstrap]").css({"visibility":" hidden"});
  
  }
    else {
      $("#end_hour_input").attr("disabled",false);
      $("#begin_hour_input").attr("disabled",false);
      // $("#input_baslama_vaxti").css("width","120px");
      // $("#input_bitme_vaxti").css("width","120px");
      $("#begin_hour_input").val("");
      $("#end_hour_input").val("");
    //Code to disable checkbox after checked
    
  };}
  $(function() {
    $(".select_bottom").css("display","none");
    $("#modal_main_divs, #modal_main_divs_2, #modal_main_div_3, .modal_time_icon").click(function() {
        $(".select_bottom").slideUp(100)
    });
    $(".slide_main").click(function() {
        $(".select_bottom").slideToggle()
    });
    $(".choose_icon_main").click(function() {
        $(".icon_slider").slideToggle(200)
    });
    $(".title_modal, .add_event_name_main, .choose_all_day_main,#modal_main_div_3,.mekan_main,#modal_main_div_4,#modal_main_divs_2").click(function() {
        $(".icon_slider").slideUp(200);
        $(".less_icons").slideUp(100);
          $(".less_main").slideUp();
          $(".show_more").slideDown();

    });
    // $(".show_more a").
    $(".show_more span").click(function() {
      $(".less_icons").slideDown(200);
      $(".show_more").slideUp(100);
      $(".less_main").slideDown(200);

    });
    
    $(".less_main span").click(function() {
      $(".less_icons").slideUp(100);
      $(".show_more").slideDown();
      $(".less_main").slideUp()
    });
    $(".select_item").click(function() {
      $(".select_bottom").slideUp(100);
    });
    for (let i = 1; i<9; i++) {
      $("#time"+i).click(function() {
        $(".slide_main").html($("#time"+i).html());
      });
      };
    for (let i = 1; i <33; i++) {
        $("#icon"+i).click(function() {
          $(".choose_icon_main span").html($("#icon"+i).html());
          $(".icon_slider").slideUp(100);
          $(".less_icons").slideUp(100);
          $(".less_main").slideUp();
          $(".show_more").slideDown();
        });
        }


});