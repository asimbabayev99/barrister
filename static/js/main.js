
// sidebar js begin
$(".sidebar-dropdown > a").click(function() {
  $(".sidebar-submenu").slideUp(200);
  if (
    $(this)
      .parent()
      .hasClass("active")
  ) {
    $(".sidebar-dropdown").removeClass("active");
    $(this)
      .parent()
      .removeClass("active");
  } else {
    $(".sidebar-dropdown").removeClass("active");
    $(this)
      .next(".sidebar-submenu")
      .slideDown(200);
    $(this)
      .parent()
      .addClass("active");
  }
});

$("#close-sidebar").click(function() {
  $(".page-wrapper").removeClass("toggled");
});
$("#show-sidebar").click(function() {
  $(".page-wrapper").addClass("toggled");
});

$("#minicalendaricon").click(function() {
  $(".page-wrapper").addClass("toggled");
  $(".calendarr").addClass("active");
  $(".calendaropen").css("display","block");
});
$("#newevent").click(function() {
  $(".page-wrapper").addClass("toggled");
  $(".nevevent").addClass("active");
});
// sidebar js end


// choose file begin
$('#chooseFile').bind('change', function () {
  var filename = $("#chooseFile").val();
  if (/^\s*$/.test(filename)) {
    $(".file-upload").removeClass('active');
    $("#noFile").text("No file chosen..."); 
  }
  else {
    $(".file-upload").addClass('active');
    $("#noFile").text(filename.replace("C:\\fakepath\\", "")); 
  }
});
// choose file end

// user-table begin
$(window).on("load resize ", function() {
  var scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
  $('.tbl-header').css({'padding-right':scrollWidth});
}).resize();
// user-table end


// phone mask begin
$(document).ready(function(){
  $("#telnum").mask("+ 994" +  " (xx) xxx-xx-xx");
     });   
// phone mask end


//Choose icon via jquery begin
$(document).ready(function() {
  $("#choose_icon_button").click(function() {
    $("#icon_secmek_ucun").slideToggle()    
  });
    for (let i = 1; i <21; i++) {
      $("#icon"+i).click(function() {
        $("#choose_icon_button").html($("#icon"+i).html());
        $("#icon_secmek_ucun").slideUp(200)
      });
      }
});
//Choose icon via jquery begin


//Vaxt secimi intervallar ile begin
$(document).ready(function() {
  $("#select_box_baslig").click(function() {
    $("#select_box_alt_hisse").slideToggle()
  })
})

$(document).ready(function() {
  $(".deqiqe_0").click(function() {
    $("#select_box_baslig").html($(".deqiqe_0").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".deqiqe_hec").click(function() {
    $("#select_box_baslig").html($(".deqiqe_hec").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".deqiqe_5").click(function() {
    $("#select_box_baslig").html($(".deqiqe_5").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
   
  $(".deqiqe_10").click(function() {
    $("#select_box_baslig").html($(".deqiqe_10").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".deqiqe_15").click(function() {
    $("#select_box_baslig").html($(".deqiqe_15").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".deqiqe_30").click(function() {
    $("#select_box_baslig").html($(".deqiqe_30").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".deqiqe_45").click(function() {
    $("#select_box_baslig").html($(".deqiqe_45").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".saat_1").click(function() {
    $("#select_box_baslig").html($(".saat_1").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".saat_3").click(function() {
    $("#select_box_baslig").html($(".saat_3").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".saat_6").click(function() {
    $("#select_box_baslig").html($(".saat_6").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".saat_12").click(function() {
    $("#select_box_baslig").html($(".saat_12").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".gun_1").click(function() {
    $("#select_box_baslig").html($(".gun_1").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".hefte_1").click(function() {
    $("#select_box_baslig").html($(".hefte_1").html());
    $("#select_box_alt_hisse").slideUp(200)
  })
})
//Vaxt secimi intervallar ile begin

// scrool trigger for click begin
// $(document).ready(function() {
 // https://gist.github.com/shlomohass/22249c0da0f53157dfe9#file-jquery-mousewheel-direction-capture-js
// $('#calendar-ms').on('mousewheel DOMMouseScroll', function(e){
//   if(typeof e.originalEvent.detail == 'number' && e.originalEvent.detail !== 0) {
//     if(e.originalEvent.detail > 0) {
//       $( ".fc-next-button" ).trigger( "click" );     
//     } else if(e.originalEvent.detail < 0){
//       $( ".fc-prev-button" ).trigger( "click" );     
           
//     }
//   } else if (typeof e.originalEvent.wheelDelta == 'number') {
//     if(e.originalEvent.wheelDelta < 0) {
//       $( ".fc-next-button" ).trigger( "click" );     
//     } else if(e.originalEvent.wheelDelta > 0) {
//         $( ".fc-prev-button" ).trigger( "click" );
//     }
//   }
// });
// })
// scrool trigger for click end