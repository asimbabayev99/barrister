// sidebar js begin

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
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
  $("#search_client_input").keyup(function (e) {
    let value = $(this).val().toLowerCase();
    $(".main_tr").each(function () {
      if ($(this).children("td.name").text().toLowerCase().includes(value)) {
        $(this).css("display", "table-row");
        $(this).children().css("display", "table-cell");
      } else {
        $(this).css("display", "none");
        // $(this).children().css("display","block")
      }
    });
  });
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
  $("#search_work").keyup(function () {
    let value = $(this).val().toLowerCase();
    $(".main_tr").each(function () {
      if ($(this).children("td.name").text().toLowerCase().includes(value)) {
        $(this).css("display", "table-row");
        $(this).children().css("display", "table-cell");
      } else {
        $(this).css("display", "none");
        // $(this).children().css("display","block")
      }
    });
  });
  // Searching in the works
  $(function () {
    function userlistclick() {
      var message_data_main = "";
      $(".user-list-row").click(function () {
        $(".alternative-first_view").each(function () {
          $(this).remove();
        });
        let second_user;
        $(".user-list-row").each(function () {
          if ($(this).hasClass("active-user")) {
            second_user = $(this).attr("user-id");
          }
        });
        let current_id = $(this).attr("user-id");
        first_user = current_id;
        $(".user-list-row").each(function () {
          $(this).removeClass("active-user");
        });
        $(this).addClass("active-user");
        if (first_user !== second_user) {
          message_data_main = "";
          $(".chatting-client-name").text($(".user-list-row.active-user span").first().text())
          $(".chat-logs").html("");
          $(".chat-logs").html(
            "<div class='loading_chat'>Mesajlar yüklənir...</div>"
          );
        } else {
          return;
        }
        var is_loading = false;
        $.ajax({
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
          },
          type: "GET",
          url: "/api/messages/list/" + current_id + "/",
          success: function (data) {
            message_data_main = data.next;
            $(".chat-logs div.loading_chat").remove();
            let messages = data.results.reverse();
            for (let i = 0; i < messages.length; i++) {
              if (
                messages[i].sender ==
                $("p#user-id").attr("chat-current-user-id")
              ) {
                generate_message(messages[i].text, "self");
              } else {
                generate_message(messages[i].text, "user");
              }
            }
            is_loading = true;
          }
        });

        $(".chat-logs").on("scroll", function () {
          if(!is_loading) return;
          let id = $(".chat-logs").attr("current_user_id");
          if ($(this).scrollTop() == 0 ) {
            if ($(".chat-logs div.load_more_messages_loader").length == 1) {
              $(".chat-logs div.load_more_messages_loader").remove();
            }
            $(".chat-logs").prepend(
              "<div class='load_more_messages_loader'><span class='spinner-grow'></span> Yüklənir...</div>"
            );
            if (!message_data_main) {
              $(".chat-logs div.load_more_messages_loader").remove();
              return;
            }
            $.get(message_data_main, function (data) {
              if(message_data_main == data.next) return;
              message_data_main = data.next;
              next_message_url = data.next;
              
              let result = data.results.reverse();
              $(".chat-logs div.load_more_messages_loader").remove();
              for (let j = 0; j < result.length; j++) {
                if (
                  result[j].sender ==
                  $("p#user-id").attr("chat-current-user-id")
                ) {
                  load_message(result[j].text, "self");
                } else {
                  load_message(result[j].text, "user");
                }
              }
              $(".chat-logs").scrollTop(10);
            });
            
          }
        });
        $(".chat-logs").attr("current_user_id", current_id);
      });
    }

    var INDEX = 0;
    $("#chat-submit").click(function (e) {
      e.preventDefault();
      var messageInputDom = document.querySelector("#chat-input");
      var message = messageInputDom.value;
      chatSocket.send(
        JSON.stringify({
          message: message,
          type: "text",
          action: "post",
          receiver: $(".chat-logs").attr("current_user_id"),
        })
      );
      $("textarea").css("height", "38px");
      messageInputDom.value = "";
      var msg = $("#chat-input").val();
      if (msg.trim() == "") {
        return false;
      }
      // generate_message(msg, "self");
      var buttons = [
        {
          name: "Existing User",
          value: "existing",
        },
        {
          name: "New User",
          value: "new",
        },
      ];
      // setTimeout(function() {
      //   generate_message(msg, 'user');
      // }, 1000)
      
    });
    // Chat in everywhere begin
    function generate_message(msg, type) {
      INDEX++;
      var str = "";
      str += "<div id='cm-msg-" + INDEX + "' class=\"chat-msg " + type + '">';
      // str += '          <span class="msg-avatar">';
      // str +=
      //   '            <img src="">';
      // str += "          </span>";
      str += '          <div class="cm-msg-text">';
      str += msg;
      str += "          </div>";
      str += "        </div>";
      $(".chat-logs").append(str);
      $("#cm-msg-" + INDEX)
        .hide()
        .fadeIn(300);
      if (type == "self") {
        $("#chat-input").val("");
      }
      $(".chat-logs")
        .stop()
        .animate({ scrollTop: $(".chat-logs")[0].scrollHeight }, 1000);
    }
    function load_message(msg, type) {
      INDEX++;
      var str = "";
      str += "<div id='cm-msg-" + INDEX + "' class=\"chat-msg " + type + '">';
      // str += '          <span class="msg-avatar">';
      // str +=
      //   '            <img src="">';
      // str += "          </span>";
      str += '          <div class="cm-msg-text">';
      str += msg;
      str += "          </div>";
      str += "        </div>";
      $(".chat-logs").prepend(str);
      $("#cm-msg-" + INDEX)
        .hide()
        .fadeIn(300);
    }
    $(document).delegate(".chat-btn", "click", function () {
      var value = $(this).attr("chat-value");
      var name = $(this).html();
      $("#chat-input").attr("disabled", false);
      generate_message(name, "self");
    });

    $("#chat-circle").click(function () {
      $("#chat-circle").toggle("scale");
      $(".chat-box").toggle("scale");
    });

    $(".chat-box-toggle").click(function () {
      $("#chat-circle").toggle("scale");
      $(".chat-box").toggle("scale");
    });

    let is_users_came = false;
    if (!is_users_came) {
      $(".user-list").append(
        "<div class='loader col-12 d-flex justify-content-center mt-5'><span class='spinner spinner-border'></span></div>"
      );
    }

    var all_chat_users = [];
    $.get("/api/chat/users", function (data, status) {
      if (status == "success") {
        is_users_came = true;
        $(".user-list div.loader").remove();
      }
      all_chat_users = data;
      data.forEach((element) => {
        $(".user-list").append(
          '<div class="list-group-item rounded-0 user-list-row" user-id=' +
            element.id +
            ">" +
            '<div class="user-list-img"> ' +
            "</div>" +
            '<div class="user-list-name"> ' +
            "<span class='username-span'>" +
            element.first_name +
            " " +
            element.last_name +
            "</span><br>" +
            '<span class="client-chat-status">' +
            element.phone_number +
            "</span>" +
            '<div class="unread-message-number"></div>' +
            "</div>" +
            "</div>"
        );
      });
      var first_user;
      // filter in users in chat
      $(".user-list-row-main input").keyup(function () {
        filter_user($(this).val())

      })
      //   $(".user-list div.user-list-row").each(function () {
      //     // $(this).remove();
      //   });
      //   let value = $(this).val();
      //   if (!value) {
      //     all_chat_users.forEach((element) => {
      //       $(".user-list").append(
      //         '<div class="list-group-item rounded-0 user-list-row" user-id=' +
      //           element.id +
      //           ">" +
      //           '<div class="user-list-img"> ' +
      //           "</div>" +
      //           '<div class="user-list-name"> ' +
      //           "<span>" +
      //           element.first_name +
      //           " " +
      //           element.last_name +
      //           "</span><br>" +
      //           '<span class="client-chat-status">' +
      //           element.phone_number +
      //           "</span>" +
      //           '<div class="unread-message-number"></div>' +
      //           "</div>" +
      //           "</div>"
      //       );
      //     });
      //     userlistclick();
      //     return;
      //   }
      //   all_chat_users.forEach((element) => {
      //     if (element.first_name && element.last_name && element.phone_number) {
      //       if (
      //         element.first_name
      //           .toLowerCase()
      //           .includes(value.toLowerCase().trim()) ||
      //         element.last_name
      //           .toLowerCase()
      //           .includes(value.toLowerCase().trim()) ||
      //         (element.first_name + " " + element.last_name)
      //           .toLocaleLowerCase()
      //           .includes(value.toLowerCase().trim()) ||
      //         element.phone_number.toString().includes(value.trim())
      //       ) {
      //         $(".user-list").append(
      //           '<div class="list-group-item rounded-0 user-list-row" user-id=' +
      //             element.id +
      //             ">" +
      //             '<div class="user-list-img"> ' +
      //             "</div>" +
      //             '<div class="user-list-name"> ' +
      //             "<span>" +
      //             element.first_name +
      //             " " +
      //             element.last_name +
      //             "</span><br>" +
      //             '<span class="client-chat-status">' +
      //             element.phone_number +
      //             "</span>" +
      //             '<div class="unread-message-number"></div>' +
      //             "</div>" +
      //             "</div>"
      //         );
      //       }
      //     } else {
      //       return;
      //     }
      //     // userlistclick();
      //   });
      // });
      userlistclick();
    });
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    var current_user = $("p#user-id").attr("chat-current-user-id");
    var notification_number = parseInt($(".message_number").text());
    var chatSocket = new WebSocket(
      "ws://" + window.location.host + "/ws/chat/" + current_user + "/"
    );
    var load_data = function (index) {
      var end = index + 1000000;
      if (index >= this.file.size) return;
      if (end > this.file.size) end = this.file.size;

      var reader = new FileReader();
      reader.onload = function () {
        var content = reader.result;
        console.log(end / 1000000);
        content = btoa(content);
        chatSocket.send(
          JSON.stringify({
            message: message,
            type: "file",
            action: "progress",
            data: content,
          })
        );
      };
      reader.readAsBinaryString(this.file.slice(index, end));
    }.bind(this);

    function uploadProgressHandler(event) {
      var percent = (event.loaded / event.total) * 100;
      var progress = Math.round(percent);
      console.log(progress);
      // $("#loaded_n_total").html("Uploaded " + event.loaded + " bytes of " + event.total);
      // var percent = (event.loaded / event.total) * 100;
      // var progress = Math.round(percent);
      // $("#uploadProgressBar").html(progress + " percent na ang progress");
      // $("#uploadProgressBar").css("width", progress + "%");
      // $("#status").html(progress + "% uploaded... please wait");
    }

    function loadHandler(event) {
      // $("#status").html(event.target.responseText);
      // $("#uploadProgressBar").css("width", "0%");
    }

    function errorHandler(event) {
      // $("#status").html("Upload Failed");
    }

    function abortHandler(event) {
      // $("#status").html("Upload Aborted");
    }
  
  chatSocket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    console.log(data);
    if (data.type == "text" && data.action == "post") {
      if (data.sender == current_user) {
        generate_message(data.message, "self");
      } else {
        notification_number += 1;
        $(".message_number").text(notification_number);
        generate_message(data.message, "user");
      }
    } else if (data.type == "file") {
      // if (data.action == 'progress') {
      //   load_data(data.file_size);
      // }
      // else if (data.action == "complete") {
      //
      // }
      if (data.action == "post") {
        if (data.sender == current_user) {
          generate_message(data.url, "self");
        } else {
          generate_message(data.url, "user");
        }
      }
    }
  };
  chatSocket.onclose = function (e) {
    console.error("Chat socket closed unexpectedly");
  };

  document.querySelector("#chat-message-input").focus();
  document.querySelector("#chat-message-input").onkeyup = function (e) {
    // if (e.keyCode === 13) {
    //   // enter, return
    //   // document.querySelector("#chat-message-submit").click();
    // }
  };

  
});

  // users begin

  // users end

  // Chat in everywhere end
    
});


function filter_user(username) {
  value = username.toLowerCase();
  $(".user-list .user-list-row").each(function() {
    text = $(this).find(".user-list-name .username-span").text().toLowerCase();
    if(text.includes(value)) {
      $(this).css('display', 'flex')
    } else {
      $(this).css('display', 'none')
    }
  })
}