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

$(document).ready(function(){
  $("#telnum").mask("+ 994" +  " (xx) xxx-xx-xx");
     });   

