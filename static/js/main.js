// sidebar js begin
$(".sidebar-dropdown > a").click(function () {
  $(".sidebar-submenu").slideUp(200);
  if ($(this).parent().hasClass("active")) {
    $(".sidebar-dropdown").removeClass("active");
    $(this).parent().removeClass("active");
  } else {
    $(".sidebar-dropdown").removeClass("active");
    $(this).next(".sidebar-submenu").slideDown(200);
    $(this).parent().addClass("active");
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
$("#chooseFile2").bind("change", function () {
  var filename = $("#chooseFile2").val();
  if (/^\s*$/.test(filename)) {
    $("#file1").removeClass("active");
    $("#noFile1").text("No file chosen...");
  } else {
    $("#file1").addClass("active");
    $("#noFile1").text(filename.replace("C:\\fakepath\\", ""));
  }
});

$("#chooseFile1").bind("change", function () {
  var filename = $("#chooseFile1").val();
  if (/^\s*$/.test(filename)) {
    $("#file2").removeClass("active");
    $("#noFile2").text("No file chosen...");
  } else {
    $("#file2").addClass("active");
    $("#noFile2").text(filename.replace("C:\\fakepath\\", ""));
  }
});

// choose file end

// user-table begin
$(window)
  .on("load resize ", function () {
    var scrollWidth =
      $(".tbl-content").width() - $(".tbl-content table").width();
    $(".tbl-header").css({ "padding-right": scrollWidth });
  })
  .resize();
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
        $(".contragent_single_picture").addClass("ready");
        $("#modal_image_pop").modal("show");
        rawImg = e.target.result;
      };

      reader.readAsDataURL(input.files[0]);
    }
  };
  $uploadCrop = $("#upload_demo").croppie({
    viewport: {
      width: 120,
      height: 120,
      type: "circle",
      enableResize: true,
      enableOrientation: true,
    },
    boundary: {
      width: 200,
      height: 200,
    },
  });
  $("#modal_image_pop").on("shown.bs.modal", function () {
    // alert('Shown pop');
    $uploadCrop
      .croppie("bind", {
        url: rawImg,
      })
      .then(function () {
        console.log("jQuery bind complete");
      });
  });
  $(".contragent_single_picture").on("change", function () {
    imageId = $(this).data("id");
    tempFilename = $(this).val();
    $("#cancelCropBtn").data("id", imageId);
    readFile(this);
  });

  $("#cropImageBtn").on("click", function (ev) {
    $uploadCrop
      .croppie("result", {
        type: "base64",
        format: "jpeg",
        size: { width: 120, height: 120 },
      })
      .then(function (resp) {
        $(".contragent_single_picture").attr("src", resp);
        $("#modal_image_pop").modal("hide");
      });
  });

  $(".file-upload").on("change", function () {
    readURL(this);
  });

  $(".upload-button").on("click", function () {
    $(".file-upload").click();
  });
});
// phone mask end

$(function () {
  "use strict";

  var aside = $(".side-nav"),
    showAsideBtn = $(".show-side-btn"),
    contents = $("#contents"),
    _window = $(window);

  showAsideBtn.on("click", function () {
    $("#" + $(this).data("show")).toggleClass("show-side-nav");
    contents.toggleClass("margin");
  });

  if (_window.width() <= 767) {
    aside.addClass("show-side-nav");
  }

  _window.on("resize", function () {
    if ($(window).width() > 767) {
      aside.removeClass("show-side-nav");
    }
  });

  // dropdown menu in the side nav
  var slideNavDropdown = $(".side-nav-dropdown");

  $(".side-nav .categories li").on("click", function () {
    var $this = $(this);

    $this.toggleClass("opend").siblings().removeClass("opend");

    if ($this.hasClass("opend")) {
      $this.find(".side-nav-dropdown").slideToggle("fast");
      $this.siblings().find(".side-nav-dropdown").slideUp("fast");
    } else {
      $this.find(".side-nav-dropdown").slideUp("fast");
    }
  });

  $(".side-nav .close-aside").on("click", function () {
    $("#" + $(this).data("close")).addClass("show-side-nav");
    contents.removeClass("margin");
  });

  // Start chart
  var chart = document.getElementById("myChart");
  Chart.defaults.global.animation.duration = 2000; // Animation duration
  Chart.defaults.global.title.display = false; // Remove title
  Chart.defaults.global.title.text = "Chart"; // Title
  Chart.defaults.global.title.position = "bottom"; // Title position
  Chart.defaults.global.defaultFontColor = "#999"; // Font color
  Chart.defaults.global.defaultFontSize = 10; // Font size for every label

  // Chart.defaults.global.tooltips.backgroundColor = '#FFF'; // Tooltips background color
  Chart.defaults.global.tooltips.borderColor = "white"; // Tooltips border color
  Chart.defaults.global.legend.labels.padding = 0;
  Chart.defaults.scale.ticks.beginAtZero = true;
  Chart.defaults.scale.gridLines.zeroLineColor = "rgba(255, 255, 255, 0.1)";
  Chart.defaults.scale.gridLines.color = "rgba(255, 255, 255, 0.02)";
  Chart.defaults.global.legend.display = false;

  var myChart = new Chart(chart, {
    type: "bar",
    data: {
      labels: ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun"],
      datasets: [
        {
          label: "Lost",
          fill: false,
          lineTension: 0,
          data: [45, 25, 40, 20, 45, 20],
          pointBorderColor: "#4bc0c0",
          borderColor: "#4bc0c0",
          borderWidth: 2,
          showLine: true,
        },
        {
          label: "Succes",
          fill: false,
          lineTension: 0,
          startAngle: 2,
          data: [20, 40, 20, 45, 25, 60],
          // , '#ff6384', '#4bc0c0', '#ffcd56', '#457ba1'
          backgroundColor: "transparent",
          pointBorderColor: "#ff6384",
          borderColor: "#ff6384",
          borderWidth: 2,
          showLine: true,
        },
      ],
    },
  });

  //  Chart ( 2 )
  var Chart2 = document.getElementById("myChart2").getContext("2d");
  var chart = new Chart(Chart2, {
    type: "line",
    data: {
      labels: [
        "January",
        "February",
        "March",
        "April",
        "test",
        "test",
        "test",
        "test",
      ],
      datasets: [
        {
          label: "My First dataset",
          backgroundColor: "rgb(255, 99, 132)",
          borderColor: "rgb(255, 79, 116)",
          borderWidth: 2,
          pointBorderColor: false,
          data: [5, 10, 5, 8, 20, 30, 20, 10],
          fill: false,
          lineTension: 0.4,
        },
        {
          label: "Month",
          fill: false,
          lineTension: 0.4,
          startAngle: 2,
          data: [20, 14, 20, 25, 10, 15, 25, 10],
          // , '#ff6384', '#4bc0c0', '#ffcd56', '#457ba1'
          backgroundColor: "transparent",
          pointBorderColor: "#4bc0c0",
          borderColor: "#4bc0c0",
          borderWidth: 2,
          showLine: true,
        },
        {
          label: "Month",
          fill: false,
          lineTension: 0.4,
          startAngle: 2,
          data: [40, 20, 5, 10, 30, 15, 15, 10],
          // , '#ff6384', '#4bc0c0', '#ffcd56', '#457ba1'
          backgroundColor: "transparent",
          pointBorderColor: "#ffcd56",
          borderColor: "#ffcd56",
          borderWidth: 2,
          showLine: true,
        },
      ],
    },

    // Configuration options
    options: {
      title: {
        display: false,
      },
    },
  });

  var chart = document.getElementById("chart3");
  var myChart = new Chart(chart, {
    type: "line",
    data: {
      labels: ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"],
      datasets: [
        {
          label: "Lost",
          fill: false,
          lineTension: 0.5,
          pointBorderColor: "transparent",
          pointColor: "white",
          borderColor: "#d9534f",
          borderWidth: 0,
          showLine: true,
          data: [0, 40, 10, 30, 10, 20, 15, 20],
          pointBackgroundColor: "transparent",
        },
        {
          label: "Lost",
          fill: false,
          lineTension: 0.5,
          pointColor: "white",
          borderColor: "#5cb85c",
          borderWidth: 0,
          showLine: true,
          data: [40, 0, 20, 10, 25, 15, 30, 0],
          pointBackgroundColor: "transparent",
        },
        {
          label: "Lost",
          fill: false,
          lineTension: 0.5,
          pointColor: "white",
          borderColor: "#f0ad4e",
          borderWidth: 0,
          showLine: true,
          data: [10, 40, 20, 5, 35, 15, 35, 0],
          pointBackgroundColor: "transparent",
        },
        {
          label: "Lost",
          fill: false,
          lineTension: 0.5,
          pointColor: "white",
          borderColor: "#337ab7",
          borderWidth: 0,
          showLine: true,
          data: [0, 30, 10, 25, 10, 40, 20, 0],
          pointBackgroundColor: "transparent",
        },
      ],
    },
  });
});
// Chart end

// Inspiration: https://tympanus.net/codrops/2012/10/04/custom-drop-down-list-styling/

function DropDown(el) {
  this.dd = el;
  this.placeholder = this.dd.children("span");
  this.opts = this.dd.find("ul.drop li");
  this.val = "";
  this.index = -1;
  this.initEvents();
}

DropDown.prototype = {
  initEvents: function () {
    var obj = this;
    obj.dd.on("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      $(this).toggleClass("active");
    });
    obj.opts
      .on("click", function () {
        var opt = $(this);
        obj.val = opt.text();
        obj.index = opt.index();
        obj.placeholder.text(obj.val);
        opt.siblings().removeClass("selected");
        opt.filter(':contains("' + obj.val + '")').addClass("selected");
      })
      .change();
  },
  getValue: function () {
    return this.val;
  },
  getIndex: function () {
    return this.index;
  },
};

$(function () {
  // create new variable for each menu
  var dd1 = new DropDown($("#noble-gases"));
  // var dd2 = new DropDown($('#other-gases'));
  $(document).click(function () {
    // close menu on document click
    $(".wrap-drop").removeClass("active");
  });
});

$(document).ready(function () {
  $(".hidden_main .show_more_btn").click(function () {
    $($(this).parent().children()[2]).toggle();
    if ($($(this).parent().children()[3]).text() === "Show more") {
      $(this).text("Show less");
    } else if ($($(this).parent().children()[3]).text() === "Show less") {
      $(this).text("Show more");
    }
  });

  // Open email types in email.html begin

  var isTypeOpen = true;
  $(".openTypes").click(function () {
    $(".emailTypesContainer").slideToggle();
    if (isTypeOpen) {
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
  $(".openKinds").click(function () {
    $(".emailKindsContainer").slideToggle();
    if (isKindOpen) {
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

  $(".open-collapse").click(function () {
    let id = $(this).attr("data-target");
    let newId = id.replace("#", "");
    $(".client-table tr").each(function () {
      if ($(this).attr("id") == newId) {
        $(this).toggle(300);
      }
    });
  });

  $(".select_status").on("change", function () {
    $(this).parent().attr("class", "");
    $(this).attr("class", "form-control");
    $(this).css({
      backgroundColor: $(this).parent().css("background-color"),
      border: "none",
    });
    $(this)
      .parent()
      .addClass("table-" + $(this).val());
    $(this).parents("td").addClass("py-0");
    if ($(this).parent().hasClass("table-dark")) {
      $(this).css("color", "#dc3545");
    } else {
      $(this).css("color", "#303f48");
    }
  });
  // clients table collapsing end


  // clients table searching begin
  $("#search_client_input").keyup(function(e){
    let value = $(this).val().toLowerCase()
    $(".main_tr").each(function(){
    if($(this).children("td.name").text().toLowerCase().includes(value)) {
        $(this).css("display", "table-row")
        $(this).children().css("display","table-cell")
      }
    else {
        $(this).css("display", "none")
        // $(this).children().css("display","block")
      }
    })
  })
  // clients table searching end


  // Client new work adding begin 
  // $("#add_work_btn").click(function() {
  //   let work_name =  $("#work_name_input").val()
  //   let work_status = $("#work_status").val()
  //   if(work_name =="" && !work_status == "") {
  //     return;
  //   } else {
  //     $("#add_work_btn").attr("data-dismiss", "modal");
  //     // $("#add_work_btn").click();
  //     if(work_status == "success") {
  //       $("#work_table_body").append(
  //         "<tr>" +
  //         "<td>"+ work_name +"</td>" +
  //         "<td class='p-0 table-dropdown'>" +
  //         "<select class='form-control select_status'>" +
  //         "<option value='success'>" +"Uğurlu"+"</option>" +
  //         "<option value='danger'>Bağlı</option>" +
  //         "<option value='info'>Davam edir</option></select>"+
  //         "<td>Yeni sənəd</td>" +
  //         "<td>Yeni sənəd</td>" +
  //         "</td></tr>"      
  //       );
  //     } else if (work_status == "danger" ) {
  //       $("#work_table_body").append(
  //         "<tr>" +
  //         "<td>"+ work_name +"</td>" +
  //         "<td class='p-0 table-dropdown'>" +
  //         "<select class='form-control select_status'>" +
  //         "<option value='danger'>Bağlı</option>" +
  //         "<option value='success'>" +"Uğurlu"+"</option>" +
  //         "<option value='info'>Davam edir</option></select>"+
  //         "<td>Yeni sənəd</td>" +
  //         "<td>Yeni sənəd</td>" +
  //         "</td></tr>");  
        
  //     } else {
  //       $("#work_table_body").append(
  //         "<tr>" +
  //         "<td>"+ work_name +"</td>" +
  //         "<td class='p-0 table-dropdown'>" +
  //         "<select class='form-control select_status'>" +
  //         "<option value='info'>Davam edir</option>" +
  //         "<option value='success'>Uğurlu</option>" +
  //         "<option value='danger'>Bağlı</option></select>"+
  //         "<td>Yeni sənəd</td>" +
  //         "<td>Yeni sənəd</td>" +
          
  //         "</td></tr>");  
        
  //     }
  //     $.ajax({
  //       headers:{
  //         'X-CSRFToken':getCookie('csrftoken')
  //       },
  //       type:"POST",
  //       url:"/api/case/create/{{client_id}}",
  //       data:{
  //         'name':$('#work_name_input').val(),
  //         'status':$('#work_status').val()
  //       },
  //       success:function(data){
  //         console.log(data)
  //       },
  //       error:function(data){
  //         console.log(data)
  //       }
  //     })
  //     $("#work_name_input").val("")
  //     $("#work_status").val("success");
  //   }
    
    
  // })
  // Client new work adding end 

  // Searching in the works
  $("#search_work").keyup(function() {
    let value = $(this).val().toLowerCase()
    $(".main_tr").each(function(){
    if($(this).children("td.name").text().toLowerCase().includes(value)) {
        $(this).css("display", "table-row")
        $(this).children().css("display","table-cell")
      }
    else {
        $(this).css("display", "none")
        // $(this).children().css("display","block")
      }
    })
    
  })
  // Searching in the works
  $(function() {
    var INDEX = 0; 
    $("#chat-submit").click(function(e) {
      e.preventDefault();
      var msg = $("#chat-input").val(); 
      if(msg.trim() == ''){
        return false;
      }
      generate_message(msg, 'self');
      var buttons = [
          {
            name: 'Existing User',
            value: 'existing'
          },
          {
            name: 'New User',
            value: 'new'
          }
        ];
      // setTimeout(function() {      
      //   generate_message(msg, 'user');  
      // }, 1000)
      
    })
    // Chat in everywhere begin 
    function generate_message(msg, type) {
      INDEX++;
      var str="";
      str += "<div id='cm-msg-"+INDEX+"' class=\"chat-msg "+type+"\">";
      str += "          <span class=\"msg-avatar\">";
      str += "            <img src=\"https:\/\/image.crisp.im\/avatar\/operator\/196af8cc-f6ad-4ef7-afd1-c45d5231387c\/240\/?1483361727745\">";
      str += "          <\/span>";
      str += "          <div class=\"cm-msg-text\">";
      str += msg;
      str += "          <\/div>";
      str += "        <\/div>";
      $(".chat-logs").append(str);
      $("#cm-msg-"+INDEX).hide().fadeIn(300);
      if(type == 'self'){
       $("#chat-input").val(''); 
      }    
      $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight}, 1000);    
    }  
    
    function generate_button_message(msg, buttons){    
      INDEX++;
      var btn_obj = buttons.map(function(button) {
         return  "              <li class=\"button\"><a href=\"javascript:;\" class=\"btn btn-primary chat-btn\" chat-value=\""+button.value+"\">"+button.name+"<\/a><\/li>";
      }).join('');
      var str="";
      str += "<div id='cm-msg-"+INDEX+"' class=\"chat-msg user\">";
      str += "          <span class=\"msg-avatar\">";
      str += "            <img src=\"https:\/\/image.crisp.im\/avatar\/operator\/196af8cc-f6ad-4ef7-afd1-c45d5231387c\/240\/?1483361727745\">";
      str += "          <\/span>";
      str += "          <div class=\"cm-msg-text\">";
      str += msg;
      str += "          <\/div>";
      str += "          <div class=\"cm-msg-button\">";
      str += "            <ul>";   
      str += btn_obj;
      str += "            <\/ul>";
      str += "          <\/div>";
      str += "        <\/div>";
      $(".chat-logs").append(str);
      $("#cm-msg-"+INDEX).hide().fadeIn(300);   
      $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight}, 1000);
      $("#chat-input").attr("disabled", true);
    }
    
    $(document).delegate(".chat-btn", "click", function() {
      var value = $(this).attr("chat-value");
      var name = $(this).html();
      $("#chat-input").attr("disabled", false);
      generate_message(name, 'self');
    })
    
    $("#chat-circle").click(function() {    
      $("#chat-circle").toggle('scale');
      $(".chat-box").toggle('scale');
    })
    
    $(".chat-box-toggle").click(function() {
      $("#chat-circle").toggle('scale');
      $(".chat-box").toggle('scale');
    })
    
  });

  $("#all_clients .dropdown-menu .dropdown-item").click(function() {
    let id = $(this).attr("id");
    let name = $(this).text();
    let before_name = $(".all_clients_in_chat span.client_name").text();
    $(".all_clients_in_chat span.client_name").text(name);
    $(this).text(before_name);
    
  })



  // Chat in everywhere end
});
