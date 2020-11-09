
// sidebar js begin
$(".sidebar-dropdown > a").click(function () {
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

$("#close-sidebar").click(function () {
  $(".page-wrapper").removeClass("toggled");
});
$("#show-sidebar").click(function () {
  $(".page-wrapper").addClass("toggled");
});

$("#minicalendaricon").click(function () {
  $(".page-wrapper").addClass("toggled");
  $(".calendarr").addClass("active");
  $(".calendaropen").css("display", "block");
});
$("#newevent").click(function () {
  $(".page-wrapper").addClass("toggled");
  $(".nevevent").addClass("active");
});
// sidebar js end


// choose file begin
$('#chooseFile2').bind('change', function () {
  var filename = $("#chooseFile2").val();
  if (/^\s*$/.test(filename)) {
    $("#file1").removeClass('active');
    $("#noFile1").text("No file chosen...");
  }
  else {
    $("#file1").addClass('active');
    $("#noFile1").text(filename.replace("C:\\fakepath\\", ""));
  }
});

$('#chooseFile1').bind('change', function () {
  var filename = $("#chooseFile1").val();
  if (/^\s*$/.test(filename)) {
    $("#file2").removeClass('active');
    $("#noFile2").text("No file chosen...");
  }
  else {
    $("#file2").addClass('active');
    $("#noFile2").text(filename.replace("C:\\fakepath\\", ""));
  }
});



// choose file end

// user-table begin
$(window).on("load resize ", function () {
  var scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
  $('.tbl-header').css({ 'padding-right': scrollWidth });
}).resize();
// user-table end


// phone mask begin
$(document).ready(function () {
  $("#clientPhoneInput").mask("(xxx) xxx-xx-xx");
  $("#telnum").mask("+ 994" + " (xx) xxx-xx-xx");
  $("#input_baslama_vaxti").mask("xx/xx/xxxx");
  $("#input_bitme_vaxti").mask("xx/xx/xxxx");
  $("#begin_hour_input").mask("xx:xx");
  $("#end_hour_input").mask("xx:xx");
  $("#phone_input").mask("(xxx) xxx-xx-xx");


  // https://codepen.io/asrulnurrahim/pen/WOyzxy
  var $uploadCrop, rawImg, tempFilename, imageId;
  var readURL = function (input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
        // $('.contragent_single_picture').attr('src', e.target.result);
        $('.contragent_single_picture').addClass('ready');
        $('#modal_image_pop').modal('show');
        rawImg = e.target.result;
      }

      reader.readAsDataURL(input.files[0]);
    }
  }
  $uploadCrop = $('#upload_demo').croppie({
    viewport: {
      width: 120,
      height: 120,
      type: 'circle',
      enableResize: true,
      enableOrientation: true
    },
    boundary: {
      width: 200,
      height: 200
    }
  });
  $('#modal_image_pop').on('shown.bs.modal', function () {
    // alert('Shown pop');
    $uploadCrop.croppie('bind', {
      url: rawImg
    }).then(function () {
      console.log('jQuery bind complete');
    });
  });
  $('.contragent_single_picture').on('change', function () {
    imageId = $(this).data('id'); tempFilename = $(this).val();
    $('#cancelCropBtn').data('id', imageId); readFile(this);
  });

  $('#cropImageBtn').on('click', function (ev) {
    $uploadCrop.croppie('result', {
      type: 'base64',
      format: 'jpeg',
      size: { width: 120, height: 120 }
    }).then(function (resp) {
      $('.contragent_single_picture').attr('src', resp);
      $('#modal_image_pop').modal('hide');
    });

  });


  $(".file-upload").on('change', function () {
    readURL(this);
  });

  $(".upload-button").on('click', function () {
    $(".file-upload").click();
  });
});
// phone mask end







$(function () {

  'use strict';

  var aside = $('.side-nav'),
    showAsideBtn = $('.show-side-btn'),
    contents = $('#contents'),
    _window = $(window)

  showAsideBtn.on("click", function () {
    $("#" + $(this).data('show')).toggleClass('show-side-nav');
    contents.toggleClass('margin');
  });

  if (_window.width() <= 767) {
    aside.addClass('show-side-nav');
  }

  _window.on('resize', function () {
    if ($(window).width() > 767) {
      aside.removeClass('show-side-nav');
    }
  });

  // dropdown menu in the side nav
  var slideNavDropdown = $('.side-nav-dropdown');

  $('.side-nav .categories li').on('click', function () {

    var $this = $(this)

    $this.toggleClass('opend').siblings().removeClass('opend');

    if ($this.hasClass('opend')) {
      $this.find('.side-nav-dropdown').slideToggle('fast');
      $this.siblings().find('.side-nav-dropdown').slideUp('fast');
    } else {
      $this.find('.side-nav-dropdown').slideUp('fast');
    }
  });

  $('.side-nav .close-aside').on('click', function () {
    $('#' + $(this).data('close')).addClass('show-side-nav');
    contents.removeClass('margin');
  });


  // Start chart
  var chart = document.getElementById('myChart');
  Chart.defaults.global.animation.duration = 2000; // Animation duration
  Chart.defaults.global.title.display = false; // Remove title
  Chart.defaults.global.title.text = "Chart"; // Title
  Chart.defaults.global.title.position = 'bottom'; // Title position
  Chart.defaults.global.defaultFontColor = '#999'; // Font color
  Chart.defaults.global.defaultFontSize = 10; // Font size for every label

  // Chart.defaults.global.tooltips.backgroundColor = '#FFF'; // Tooltips background color
  Chart.defaults.global.tooltips.borderColor = 'white'; // Tooltips border color
  Chart.defaults.global.legend.labels.padding = 0;
  Chart.defaults.scale.ticks.beginAtZero = true;
  Chart.defaults.scale.gridLines.zeroLineColor = 'rgba(255, 255, 255, 0.1)';
  Chart.defaults.scale.gridLines.color = 'rgba(255, 255, 255, 0.02)';
  Chart.defaults.global.legend.display = false;

  var myChart = new Chart(chart, {
    type: 'bar',
    data: {
      labels: ["Yanvar", "Fevral", "Mart", "Aprel", "May", 'Iyun'],
      datasets: [{
        label: "Lost",
        fill: false,
        lineTension: 0,
        data: [45, 25, 40, 20, 45, 20],
        pointBorderColor: "#4bc0c0",
        borderColor: '#4bc0c0',
        borderWidth: 2,
        showLine: true,
      }, {
        label: "Succes",
        fill: false,
        lineTension: 0,
        startAngle: 2,
        data: [20, 40, 20, 45, 25, 60],
        // , '#ff6384', '#4bc0c0', '#ffcd56', '#457ba1'
        backgroundColor: "transparent",
        pointBorderColor: "#ff6384",
        borderColor: '#ff6384',
        borderWidth: 2,
        showLine: true,
      }]
    },
  });

  //  Chart ( 2 )
  var Chart2 = document.getElementById('myChart2').getContext('2d');
  var chart = new Chart(Chart2, {
    type: 'line',
    data: {
      labels: ["January", "February", "March", "April", 'test', 'test', 'test', 'test'],
      datasets: [{
        label: "My First dataset",
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 79, 116)',
        borderWidth: 2,
        pointBorderColor: false,
        data: [5, 10, 5, 8, 20, 30, 20, 10],
        fill: false,
        lineTension: .4,
      }, {
        label: "Month",
        fill: false,
        lineTension: .4,
        startAngle: 2,
        data: [20, 14, 20, 25, 10, 15, 25, 10],
        // , '#ff6384', '#4bc0c0', '#ffcd56', '#457ba1'
        backgroundColor: "transparent",
        pointBorderColor: "#4bc0c0",
        borderColor: '#4bc0c0',
        borderWidth: 2,
        showLine: true,
      }, {
        label: "Month",
        fill: false,
        lineTension: .4,
        startAngle: 2,
        data: [40, 20, 5, 10, 30, 15, 15, 10],
        // , '#ff6384', '#4bc0c0', '#ffcd56', '#457ba1'
        backgroundColor: "transparent",
        pointBorderColor: "#ffcd56",
        borderColor: '#ffcd56',
        borderWidth: 2,
        showLine: true,
      }]
    },

    // Configuration options
    options: {
      title: {
        display: false
      }
    }
  });

  var chart = document.getElementById('chart3');
  var myChart = new Chart(chart, {
    type: 'line',
    data: {
      labels: ["One", "Two", "Three", "Four", "Five", 'Six', "Seven", "Eight"],
      datasets: [{
        label: "Lost",
        fill: false,
        lineTension: .5,
        pointBorderColor: "transparent",
        pointColor: "white",
        borderColor: '#d9534f',
        borderWidth: 0,
        showLine: true,
        data: [0, 40, 10, 30, 10, 20, 15, 20],
        pointBackgroundColor: 'transparent',
      }, {
        label: "Lost",
        fill: false,
        lineTension: .5,
        pointColor: "white",
        borderColor: '#5cb85c',
        borderWidth: 0,
        showLine: true,
        data: [40, 0, 20, 10, 25, 15, 30, 0],
        pointBackgroundColor: 'transparent',
      },
      {
        label: "Lost",
        fill: false,
        lineTension: .5,
        pointColor: "white",
        borderColor: '#f0ad4e',
        borderWidth: 0,
        showLine: true,
        data: [10, 40, 20, 5, 35, 15, 35, 0],
        pointBackgroundColor: 'transparent',
      },
      {
        label: "Lost",
        fill: false,
        lineTension: .5,
        pointColor: "white",
        borderColor: '#337ab7',
        borderWidth: 0,
        showLine: true,
        data: [0, 30, 10, 25, 10, 40, 20, 0],
        pointBackgroundColor: 'transparent',
      }]
    },
  });

});
// Chart end


// Inspiration: https://tympanus.net/codrops/2012/10/04/custom-drop-down-list-styling/


function DropDown(el) {
  this.dd = el;
  this.placeholder = this.dd.children('span');
  this.opts = this.dd.find('ul.drop li');
  this.val = '';
  this.index = -1;
  this.initEvents();
}

DropDown.prototype = {
  initEvents: function () {
    var obj = this;
    obj.dd.on('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      $(this).toggleClass('active');
    });
    obj.opts.on('click', function () {
      var opt = $(this);
      obj.val = opt.text();
      obj.index = opt.index();
      obj.placeholder.text(obj.val);
      opt.siblings().removeClass('selected');
      opt.filter(':contains("' + obj.val + '")').addClass('selected');
    }).change();
  },
  getValue: function () {
    return this.val;
  },
  getIndex: function () {
    return this.index;
  }
};

$(function () {
  // create new variable for each menu
  var dd1 = new DropDown($('#noble-gases'));
  // var dd2 = new DropDown($('#other-gases'));
  $(document).click(function () {
    // close menu on document click
    $('.wrap-drop').removeClass('active');
  });
});

$(document).ready(function() {
  
  $(".hidden_main .show_more_btn").click(function() {
    $($(this).parent().children()[2]).toggle();
    if($($(this).parent().children()[3]).text()==="Show more") {
      $(this).text("Show less")
    } else if($($(this).parent().children()[3]).text()==="Show less") {
      $(this).text("Show more")
    }
  });
  
  // Open email types in email.html begin


  var isTypeOpen = true;
  $(".openTypes").click(function() {
    $(".emailTypesContainer").slideToggle();
    if(isTypeOpen) {
      $(".openTypes").removeClass("fa-minus");
      $(".openTypes").addClass("fa-plus");
      isTypeOpen = false;
      
    } else {
      $(".openTypes").removeClass("fa-plus");
      $(".openTypes").addClass("fa-minus");
      isTypeOpen = true;
    }
    
  });
  
  // Open email types in email.html end


  // Open email kinds begin 

  
  var isKindOpen = true;
  $(".openKinds").click(function() {
    $(".emailKindsContainer").slideToggle();
    if(isKindOpen) {
      $(".openKinds").removeClass("fa-minus");
      $(".openKinds").addClass("fa-plus");
      isKindOpen = false;
      
    } else {
      $(".openKinds").removeClass("fa-plus");
      $(".openKinds").addClass("fa-minus");
      isKindOpen = true;
    }
  });
  
  
  // Open email kinds end


  // clients table collapsing begin 

 $(".open-collapse").click(function() {

   let id = $(this).attr("data-target");
   let newId = id.replace("#","");
   $(".client-table tr").each(function() {
     if($(this).attr("id") == newId) {
      $(this).toggle(300)
     }
   })
 })

 $("#add_new_client_btn").click(function() {
   let client_name = $("#new_client_name").val();
   let client_email = $("#new_client_email").val();
   let client_phone = $("#clientPhoneInput").val();
   let client_address = $("#new_client_address").val();
   let client_id = Math.floor(Math.random() * 100000)
   console.log(client_id)
   
   $("#client_table").prepend(
     "<tr>" +
     "<td>"     +
     client_name +
     "</td>"    +
     "<td>" + client_email  + "</td>" +
     "<td>" +  client_phone + "</td>" +
     "<td class = 'table-success'>" + "Aktiv" + "</td>" +
     "<td class = 'text-center'>" + "<i class = ' far fa-comments' data-toggle = 'modal' data-target = '#modal_aside_right'></i>" + "</td>" +
     "<td class='text-center'>" + "<i data-target='#active_table_" + client_id + "' class='fas open-collapse fa-ellipsis-h'></i>" + "</td>" + 
     "</tr>"

   )
 })
  // clients table collapsing end 
});

