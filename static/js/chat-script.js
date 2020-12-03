$(document).ready(function () {
  // $(".fa-paperclip").click(function () {
  //   if (confirm("Are you sure")) {
  //     return 0;
  //   } else {
  //     return 0;
  //   }
  // });

  // var roomName = "{{ room_name }}";
  var current_user = $("#current_user_id").attr('user_id');
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
          message: "",
          type: "file",
          action: "progress",
          data: content,
        })
      );
    };
    reader.readAsBinaryString(this.file.slice(index, end));
  }.bind(this);

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

  $("#input_file").change(function () {
    file = $("#input_file").get(0).files[0];
    this.file = file;
    console.log(file);
    var formData = new FormData();
    formData.append("file", file);
    // const data_ = JSON.stringify(data)
    // formData.append('data', data);
    $("#modal_aside_top .modal-header span span").text(file.name)
    let kb = (file.size / 1024).toString().split(".")[0]
    let mb;
    if(kb > 1000) {
      mb = (kb / 1024).toString().split(".")[0] + " mb"
    } else {
      mb = kb + " kb"
    }
    $("#modal_aside_top .modal-body p span").text(mb)
    $("#modal_aside_top").modal("show");
    if(kb > 5000) {
      $("#send_confirm_btn").attr("disabled", true)
    } else {
      $("#send_confirm_btn").attr("disabled", false)
    }
    $("#send_confirm_btn").click(function(){
      $.ajax({
        type: "POST",
        url: "/chat/upload_file/{{receiver}}/",
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        contentType: false,
        processData: false,
        data: formData,
        xhr: function () {
          var xhr = new window.XMLHttpRequest();
          xhr.upload.addEventListener("progress", uploadProgressHandler, false);
          xhr.addEventListener("load", loadHandler, false);
          xhr.addEventListener("error", errorHandler, false);
          xhr.addEventListener("abort", abortHandler, false);
          return xhr;
        },
        success: function (data) {
          chatSocket.send(
            JSON.stringify({
              type: "file",
              action: "post",
              id: data.id,
              message: data.message,
              filename: data.filename,
              url: data.url,
              date: data.date,
            })
          );
        },
        error: function (jqXhr, textStatus, errorMessage) {
          alert(errorMessage);
        },
      });
    }) 
      
  });

  chatSocket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    console.log(data);
    if (data.type == "text" && data.action == "post") {
      

      if (data.sender == current_user) {
        $("#modal_aside_right .modal-body").animate(
          {
            scrollTop: $("#modal_aside_right .modal-body").prop("scrollHeight"),
          },
          1000
        );
        document.querySelector("#modal_aside_right .modal-body").innerHTML +=
          "<div class='outgoing_msg'>" +
          "<div class='sent_msg'>" +
          "<p>" +
          data.message +
          "</p>" +
          "<span class='time_date'>" +
          data.date +
          "</span>" +
          "</div>" +
          "</div>";
      } else {
        alert("you have e message")
        
        $("#modal_aside_right .modal-body").animate(
          {
            scrollTop: $("#modal_aside_right .modal-body").prop("scrollHeight"),
          },
          1000
        );
        document.querySelector("#modal_aside_right .modal-body").innerHTML +=
          "<div class='incoming_msg'>" +
          "<div class='incoming_msg_img'><img src='https://ptetutorials.com/images/user-profile.png' alt='sunil'></div>" +
          "<div class='received_msg'>" +
          "<div class='received_withd_msg'>" +
          "<p>" +
          data.message +
          "</p>" +
          "<span class='time_date'>" +
          data.date +
          "</span>" +
          "</div>" +
          "</div>" +
          "</div>";
         
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
          $("#modal_aside_right .modal-body").animate(
            {
              scrollTop: $("#modal_aside_right .modal-body").prop(
                "scrollHeight"
              ),
            },
            1000
          );
          document.querySelector("#modal_aside_right .modal-body").innerHTML +=
            "<div class='outgoing_msg'>" +
            "<div class='sent_msg'>" +
            "<p><a href='" +
            data.url +
            "'>" +
            data.filename +
            "</a></p>" +
            "<p>" +
            data.message +
            "</p>" +
            "<span class='time_date'>" +
            data.date +
            "</span>" +
            "</div>" +
            "</div>";
        } else {
          $("#modal_aside_right .modal-body").animate(
            {
              scrollTop: $("#modal_aside_right .modal-body").prop(
                "scrollHeight"
              ),
            },
            1000
          );
          document.querySelector("#modal_aside_right .modal-body").innerHTML +=
            "<div class='incoming_msg'>" +
            "<div class='incoming_msg_img'><img src='https://ptetutorials.com/images/user-profile.png' alt='sunil'></div>" +
            "<div class='received_msg'>" +
            "<div class='received_withd_msg'>" +
            "<p><a href='" +
            data.file_link +
            "'>" +
            data.filename +
            "</a></p>" +
            "<p>" +
            data.message +
            "</p>" +
            "<span class='time_date'>" +
            data.date +
            "</span>" +
            "</div>" +
            "</div>" +
            "</div>";
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

  document.querySelector("#chat-message-submit").onclick = function (e) {
    var messageInputDom = document.querySelector("#chat-message-input");

    var message = messageInputDom.value;
    chatSocket.send(
      JSON.stringify({
        message: message,
        type: "text",
        action: "post",
        receiver: $('.person-title').attr('chat_id') 
      })
    );
    $("textarea").css("height", "38px");
    messageInputDom.value = "";
  };
});

$(function () {
  $("textarea")
    .each(function () {
      this.setAttribute("style", "height:" + 38 + "px;");
    })
    .on("input", function () {
      this.style.height = "auto";
      this.style.height = this.scrollHeight + "px";
    });
});
