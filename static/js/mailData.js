$(document).ready(function () {
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

  var isDataCame = false,
    
    deleteJson = {};
  if (isDataCame === false) {
    $("#mailContent").append(
      '<li id="preLoader" class="list-group-item align-items-center justify-content-center"><div class="spinner-grow float-left"  role="status"><span class="sr-only"> Loading...</span></div> <div class="float-left  h-100 d-flex align-items-center"> Loading...</div></li>'
    );
  }
  fetch("http://127.0.0.1:8000/api/emails/?ordering=-date", {
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => response.json())
    .then((json) => {
      if (Object.keys(json).length === 0) {
        isDataCame = true;
        $("#preLoader").css("display", "none");
        $("#mailContent").append(
          '<li id="preLoader" class="list-group-item align-items-center justify-content-center">Mail Yoxdur...</li>'
        );
      }
      json.forEach((element) => {
        if (element.folder === "Inbox") {
          var subjectLen = element.subject.length;
          var subjectString = "";
          if (subjectLen > 15) {
            for (let i = 0; i < 15; i++) {
              subjectString += element.subject[i];
            }
            subjectString += "...";
          } else {
            subjectString = element.subject;
          }
          $("#mailContent").append(
            "<li  num=" +
              element.num +
              ' id="' +
              element.id +
              '"class="list-group-item d-flex align-items-center mailListGroup"><div class="d-flex h-100 w-100 align-items-center' +
              ' justify-content-between"><span class="d-flex align-items-center"><input type="checkbox" class="checkBoxMails" name="' +
              element.folder +
              '" id="mailCheckboxes"><span class="emailNameTitle">' +
              element.sender +
              '</span><span class="emailSubject">' +
              subjectString +
              "</span></span>" +
              "</li>"
          );

          isDataCame = true;
          $("#preLoader").css("display", "none");
        }
      });

      // Click to the sidebar DRAFTS choice to look at only DRAFTS emails begin

      $(".drafts").click(function () {
        $("#mailContent").html("");
        json.forEach((element) => {
          if (element.folder === "Drafts") {
            $("#mailContent").append(
              "<li num=" +
                element.num +
                ' id="' +
                element.id +
                '" class="list-group-item d-flex align-items-center mailListGroup"><div class="d-flex h-100 w-100 align-items-center justify-content-between"><span class="d-flex align-items-center"><input type="checkbox" class="checkBoxMails" name="' +
                element.folder +
                '" id="mailCheckboxes"><span class="emailNameTitle">' +
                element.sender +
                '</span><span class="emailSubject">' +
                element.subject +
                "</span></span></li>"
            );
            $(".mailListGroup").click(function () {
              $(".defaultMail").show(200);
              $(".insteadMailImage").hide(100);
              $(".file_container .list-group").html("");
              $(".file_container .file_image").html("");
              var mail = $(this).attr("id");
              var num = $(this).attr("num");
              $(".mailListGroup").each((element) => {
                if ($(this).attr("num") == num) {
                  $(this).addClass("bg-primary text-light");
                }
              });
              $(".mailListGroup").each(function () {
                if ($(this)[0].id == mail) {
                  $(this).addClass("bg-primary text-light");
                } else {
                  $(this).removeClass("bg-primary text-light");
                }
              });
              json.forEach((element) => {
                if (element.id == mail) {
                  $(".mailSubject").text(element.sender);
                  $(".mailSubject").attr("id", mail);
                  $(".mailSender").text(element.sender);
                  let subjectLen = element.subject.length;

                  $(".mailSubjectExpand").text(element.subject);
                  let time = element.date.split("-");
                  let endTime = time[2].split("");
                  let wholeTime =
                    time[0] +
                    "-" +
                    time[1] +
                    "-" +
                    endTime[0] +
                    "" +
                    endTime[1];
                  $(".mailDate").text(wholeTime);
                  $(".mailMovzu").html(element.content);
                  let mailSender = element.sender.split("");
                  $(".emailImage").text(
                    mailSender[0].toUpperCase() +
                      "" +
                      mailSender[1].toUpperCase()
                  );
                  if (element.attachments.length > 0) {
                    /// If txt file do this begin
                    // console.log(element.attachments)
                    var attachment = [];
                    element.attachments.forEach((element) => {
                      if (element.view_url.endsWith(".txt")) {
                        $(".file_container .list-group").append(
                          "<li class='list-group-item d-flex align-items-center justify-content-between'><span>" +
                            element.name +
                            "</span><span><button class='mr-3 btn btn-sm btn-dark show_modal_email' url=" +
                            "" +
                            element.view_url +
                            " data-toggle='modal' data-target='#file_showing_modal'><i class='fas fa-eye'></i></button><a href=" +
                            element.download_url +
                            "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                        );
                        $(".show_modal_email").click(function () {
                          $(
                            "#file_showing_modal .modal-body iframe"
                          ).removeClass("d-none");
                          $(
                            "#file_showing_modal .modal-body .email_image"
                          ).addClass("d-none");
                          $("#file_showing_modal .modal-body iframe").attr(
                            "src",
                            $(this).attr("url")
                          );
                        });
                      } else if (
                        element.view_url.endsWith(".jpg") ||
                        element.view_url.endsWith(".png") ||
                        element.view_url.endsWith(".jpeg")
                      ) {
                        $(".file_container .file_image").append(
                          "" +
                            "<div class='col-md-6  col-lg-4 mb-3' style='height:150px;position:relative'>" +
                            "<img style='height : 100%;object-fit:cover;position:relative;' class='w-100 mail_image' src=" +
                            element.view_url +
                            ">" +
                            "<button data-toggle='modal' data-target='#file_showing_modal' url=" +
                            element.view_url +
                            " class='show_modal_email_image btn btn-sm btn-dark absolute_email_btn_2 mr-3'><i class='fas fa-eye'></i></button>" +
                            "<a href=" +
                            element.download_url +
                            "><button class='btn btn-sm btn-dark absolute_email_btn'><i class='fas fa-download'></i></button></a>" +
                            "</img>" +
                            "</div>" +
                            ""
                        );
                        $(".show_modal_email_image").click(function () {
                          $("#file_showing_modal .modal-body iframe").addClass(
                            "d-none"
                          );
                          $(
                            "#file_showing_modal .modal-body .email_image"
                          ).removeClass("d-none");
                          $(
                            "#file_showing_modal .modal-body .email_image"
                          ).html(
                            "" +
                              "<img style='width:100%; height:100%;object-fit:contain' src=" +
                              $(this).attr("url") +
                              "></img>" +
                              ""
                          );
                        });
                      } else if (
                        element.view_url.endsWith(".rar") ||
                        element.view_url.endsWith(".zip")
                      ) {
                        $(".file_container .list-group").append(
                          "<li class='list-group-item alert-warning d-flex align-items-center justify-content-between'><span>" +
                            element.name +
                            " <br><small>Bu faylı görmək mümkün deyil</small> </span><span><a href=" +
                            element.download_url +
                            "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                        );
                      } else if (
                        element.view_url.endsWith(".docx") ||
                        element.view_url.endsWith(".ppt") ||
                        element.view_url.endsWith(".xls")
                      ) {
                        $(".file_container .list-group").append(
                          "<li class='list-group-item d-flex align-items-center justify-content-between'><span>" +
                            element.name +
                            "</span><span><button class='mr-3 btn btn-sm btn-dark show_modal_email' url=" +
                            "" +
                            element.view_url +
                            " data-toggle='modal' data-target='#file_showing_modal'><i class='fas fa-eye'></i></button><a href=" +
                            element.download_url +
                            "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                        );
                      } else {
                        $(".file_container .list-group").append(
                          "<li class='list-group-item alert-warning d-flex align-items-center justify-content-between'><span>" +
                            element.name +
                            " <br><small>Bu faylı görmək mümkün deyil</small> </span><span><a href=" +
                            element.download_url +
                            "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                        );
                      }
                    });
                  }
                }
              });

              var deletingMessagesIds = [];
              var folder;
            });
          }
        });
        deletingMessagesIds = [];
        folder = "";
        $(".checkBoxMails").click(function () {
          folder = $(this).attr("name");
          let id = $(this).parent().parent().parent().attr("num");
          if ($(this).is(":checked")) {
            deletingMessagesIds.push(id);
          } else {
            let index = deletingMessagesIds.indexOf(id);
            deletingMessagesIds.splice(index, 1);
          }
          deleteJson = {
            uids: deletingMessagesIds,
            folder: folder,
          };
        });
      });

      // Click to the sidebar DRAFTS choice to look at only DRAFTS emails end

      //***********************  Sent mails begin  ********************** */
      $(".sendingMails").click(function () {
        $("#mailContent").html("");

        json.forEach((element) => {
          if (element.folder == "Sent") {
            $("#mailContent").append(
              "<li num=" +
                element.num +
                ' id="' +
                element.id +
                '" class="list-group-item d-flex align-items-center mailListGroup"><div class="d-flex h-100 w-100 align-items-center justify-content-between"><span class="d-flex align-items-center"><input type="checkbox" class="checkBoxMails" name="' +
                element.folder +
                '" id="mailCheckboxes"><span class="emailNameTitle">' +
                element.sender +
                '</span><span class="emailSubject">' +
                element.subject +
                "</span></span></li>"
            );
          }
          $(".mailListGroup").click(function () {
            $(".defaultMail").show(200);
            $(".insteadMailImage").hide(100);
            $(".file_container .list-group").html("");
            $(".file_container .file_image").html("");
            var mail = $(this).attr("id");
            var num = $(this).attr("num");
            $(".mailListGroup").each((element) => {
              if ($(this).attr("num") == num) {
                $(this).addClass("bg-primary text-light");
              }
            });
            $(".mailListGroup").each(function () {
              if ($(this)[0].id == mail) {
                $(this).addClass("bg-primary text-light");
              } else {
                $(this).removeClass("bg-primary text-light");
              }
            });
            json.forEach((element) => {
              if (element.id == mail) {
                $(".mailSubject").text(element.sender);
                $(".mailSubject").attr("id", mail);
                $(".mailSender").text(element.sender);
                let subjectLen = element.subject.length;

                $(".mailSubjectExpand").text(element.subject);
                let time = element.date.split("-");
                let endTime = time[2].split("");
                let wholeTime =
                  time[0] + "-" + time[1] + "-" + endTime[0] + "" + endTime[1];
                $(".mailDate").text(wholeTime);
                $(".mailMovzu").html(element.content);
                let mailSender = element.sender.split("");
                $(".emailImage").text(
                  mailSender[0].toUpperCase() + "" + mailSender[1].toUpperCase()
                );
                if (element.attachments.length > 0) {
                  /// If txt file do this begin
                  // console.log(element.attachments)
                  var attachment = [];
                  element.attachments.forEach((element) => {
                    if (element.view_url.endsWith(".txt")) {
                      $(".file_container .list-group").append(
                        "<li class='list-group-item d-flex align-items-center justify-content-between'><span>" +
                          element.name +
                          "</span><span><button class='mr-3 btn btn-sm btn-dark show_modal_email' url=" +
                          "" +
                          element.view_url +
                          " data-toggle='modal' data-target='#file_showing_modal'><i class='fas fa-eye'></i></button><a href=" +
                          element.download_url +
                          "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                      );
                      $(".show_modal_email").click(function () {
                        $("#file_showing_modal .modal-body iframe").removeClass(
                          "d-none"
                        );
                        $(
                          "#file_showing_modal .modal-body .email_image"
                        ).addClass("d-none");
                        $("#file_showing_modal .modal-body iframe").attr(
                          "src",
                          $(this).attr("url")
                        );
                      });
                    } else if (
                      element.view_url.endsWith(".jpg") ||
                      element.view_url.endsWith(".png") ||
                      element.view_url.endsWith(".jpeg")
                    ) {
                      $(".file_container .file_image").append(
                        "" +
                          "<div class='col-md-6  col-lg-4 mb-3' style='height:150px;position:relative'>" +
                          "<img style='height : 100%;object-fit:cover;position:relative;' class='w-100 mail_image' src=" +
                          element.view_url +
                          ">" +
                          "<button data-toggle='modal' data-target='#file_showing_modal' url=" +
                          element.view_url +
                          " class='show_modal_email_image btn btn-sm btn-dark absolute_email_btn_2 mr-3'><i class='fas fa-eye'></i></button>" +
                          "<a href=" +
                          element.download_url +
                          "><button class='btn btn-sm btn-dark absolute_email_btn'><i class='fas fa-download'></i></button></a>" +
                          "</img>" +
                          "</div>" +
                          ""
                      );
                      $(".show_modal_email_image").click(function () {
                        $("#file_showing_modal .modal-body iframe").addClass(
                          "d-none"
                        );
                        $(
                          "#file_showing_modal .modal-body .email_image"
                        ).removeClass("d-none");
                        $("#file_showing_modal .modal-body .email_image").html(
                          "" +
                            "<img style='width:100%; height:100%;object-fit:contain' src=" +
                            $(this).attr("url") +
                            "></img>" +
                            "" 
                        );
                      });
                    } else if (
                      element.view_url.endsWith(".rar") ||
                      element.view_url.endsWith(".zip")
                    ) {
                      $(".file_container .list-group").append(
                        "<li class='list-group-item alert-warning d-flex align-items-center justify-content-between'><span>" +
                          element.name +
                          " <br><small>Bu faylı görmək mümkün deyil</small> </span><span><a href=" +
                          element.download_url +
                          "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                      );
                    } else if (
                      element.view_url.endsWith(".docx") ||
                      element.view_url.endsWith(".ppt") ||
                      element.view_url.endsWith(".xls")
                    ) {
                      $(".file_container .list-group").append(
                        "<li class='list-group-item d-flex align-items-center justify-content-between'><span>" +
                          element.name +
                          "</span><span><button class='mr-3 btn btn-sm btn-dark show_modal_email' url=" +
                          "" +
                          element.view_url +
                          " data-toggle='modal' data-target='#file_showing_modal'><i class='fas fa-eye'></i></button><a href=" +
                          element.download_url +
                          "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                      );
                    } else {
                      $(".file_container .list-group").append(
                        "<li class='list-group-item alert-warning d-flex align-items-center justify-content-between'><span>" +
                          element.name +
                          " <br><small>Bu faylı görmək mümkün deyil</small> </span><span><a href=" +
                          element.download_url +
                          "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                      );
                    }
                  });
                }
              }
            });

            var deletingMessagesIds = [];
            var folder;
          });
        });
        deletingMessagesIds = [];
        folder = "";
        $(".checkBoxMails").click(function () {
          folder = $(this).attr("name");
          let id = $(this).parent().parent().parent().attr("num");
          if ($(this).is(":checked")) {
            deletingMessagesIds.push(id);
          } else {
            let index = deletingMessagesIds.indexOf(id);
            deletingMessagesIds.splice(index, 1);
          }
          deleteJson = {
            uids: deletingMessagesIds,
            folder: folder,
          };
          // console.log(deleteJson)
        });
      });

      //***********************  Sent mails end  ********************** */
      $(".spam_mails").click(function(){
        $("#mailContent").html("");
        var delete_mail
        fetch("/api/emails/?ordering=-date&folder=Spam")
        .then(response => response.json())
        .then(json => {
          console.log(json)
          delete_mail = json
          json.forEach((element) => {
              $("#mailContent").append(
                "<li num=" +
                  element.num +
                  ' id="' +
                  element.id +
                  '"class="list-group-item d-flex align-items-center mailListGroup"><div class="d-flex h-100 w-100 align-items-center justify-content-between"><span class="d-flex align-items-center"><input type="checkbox" class="checkBoxMails" name="' +
                  element.folder +
                  '" id="mailCheckboxes"><span class="emailNameTitle">' +
                  element.sender +
                  '</span><span class="emailSubject">' +
                  element.subject +
                  "</span></span></li>"
              );
              $(".mailListGroup").click(function () {
                $(".defaultMail").show(200);
                $(".insteadMailImage").hide(100);
                $(".file_container .list-group").html("");
                $(".file_container .file_image").html("");
                var mail = $(this).attr("id");
                var num = $(this).attr("num");
                $(".mailListGroup").each((element) => {
                  if ($(this).attr("num") == num) {
                    $(this).addClass("bg-primary text-light");
                  }
                });
                $(".mailListGroup").each(function () {
                  if ($(this)[0].id == mail) {
                    $(this).addClass("bg-primary text-light");
                  } else {
                    $(this).removeClass("bg-primary text-light");
                  }
                });
                json.forEach((element) => {
                  if (element.id == mail) {
                    $(".mailSubject").text(element.sender);
                    $(".mailSubject").attr("id", mail);
                    $(".mailSender").text(element.sender);
                    let subjectLen = element.subject.length;
                    $(".mailSubjectExpand").text(element.subject);
                    let time = element.date.split("-");
                    let endTime = time[2].split("");
                    let wholeTime =
                      time[0] +
                      "-" +
                      time[1] +
                      "-" +
                      endTime[0] +
                      "" +
                      endTime[1];
                    $(".mailDate").text(wholeTime);
                    $(".mailMovzu").html(element.content);
                    let mailSender = element.sender.split("");
                    $(".emailImage").text(
                      mailSender[0].toUpperCase() +
                        "" +
                        mailSender[1].toUpperCase()
                    );
                    if (element.attachments.length > 0) {
                      /// If txt file do this begin
                      // console.log(element.attachments)
                      var attachment = [];
                      element.attachments.forEach((element) => {
                        if (element.view_url.endsWith(".txt")) {
                          $(".file_container .list-group").append(
                            "<li class='list-group-item d-flex align-items-center justify-content-between'><span>" +
                              element.name +
                              "</span><span><button class='mr-3 btn btn-sm btn-dark show_modal_email' url=" +
                              "" +
                              element.view_url +
                              " data-toggle='modal' data-target='#file_showing_modal'><i class='fas fa-eye'></i></button><a href=" +
                              element.download_url +
                              "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                          );
                          $(".show_modal_email").click(function () {
                            $(
                              "#file_showing_modal .modal-body iframe"
                            ).removeClass("d-none");
                            $(
                              "#file_showing_modal .modal-body .email_image"
                            ).addClass("d-none");
                            $("#file_showing_modal .modal-body iframe").attr(
                              "src",
                              $(this).attr("url")
                            );
                          });
                        } else if (
                          element.view_url.endsWith(".jpg") ||
                          element.view_url.endsWith(".png") ||
                          element.view_url.endsWith(".jpeg")
                        ) {
                          $(".file_container .file_image").append(
                            "" +
                              "<div class='col-md-6  col-lg-4 mb-3' style='height:150px;position:relative'>" +
                              "<img style='height : 100%;object-fit:cover;position:relative;' class='w-100 mail_image' src=" +
                              element.view_url +
                              ">" +
                              "<button data-toggle='modal' data-target='#file_showing_modal' url=" +
                              element.view_url +
                              " class='show_modal_email_image btn btn-sm btn-dark absolute_email_btn_2 mr-3'><i class='fas fa-eye'></i></button>" +
                              "<a href=" +
                              element.download_url +
                              "><button class='btn btn-sm btn-dark absolute_email_btn'><i class='fas fa-download'></i></button></a>" +
                              "</img>" +
                              "</div>" +
                              ""
                          );
                          $(".show_modal_email_image").click(function () {
                            $("#file_showing_modal .modal-body iframe").addClass(
                              "d-none"
                            );
                            $(
                              "#file_showing_modal .modal-body .email_image"
                            ).removeClass("d-none");
                            $(
                              "#file_showing_modal .modal-body .email_image"
                            ).html(
                              "" +
                                "<img style='width:100%; height:100%;object-fit:contain' src=" +
                                $(this).attr("url") +
                                "></img>" +
                                ""
                            );
                          });
                        } else if (
                          element.view_url.endsWith(".rar") ||
                          element.view_url.endsWith(".zip")
                        ) {
                          $(".file_container .list-group").append(
                            "<li class='list-group-item alert-warning d-flex align-items-center justify-content-between'><span>" +
                              element.name +
                              " <br><small>Bu faylı görmək mümkün deyil</small> </span><span><a href=" +
                              element.download_url +
                              "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                          );
                        } else if (
                          element.view_url.endsWith(".docx") ||
                          element.view_url.endsWith(".ppt") ||
                          element.view_url.endsWith(".xls")
                        ) {
                          $(".file_container .list-group").append(
                            "<li class='list-group-item d-flex align-items-center justify-content-between'><span>" +
                              element.name +
                              "</span><span><button class='mr-3 btn btn-sm btn-dark show_modal_email' url=" +
                              "" +
                              element.view_url +
                              " data-toggle='modal' data-target='#file_showing_modal'><i class='fas fa-eye'></i></button><a href=" +
                              element.download_url +
                              "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                          );
                        } else {
                          $(".file_container .list-group").append(
                            "<li class='list-group-item alert-warning d-flex align-items-center justify-content-between'><span>" +
                              element.name +
                              " <br><small>Bu faylı görmək mümkün deyil</small> </span><span><a href=" +
                              element.download_url +
                              "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                          );
                        }
                      });
                    }
                  }
                });
  
                var deletingMessagesIds = [];
                var folder;
              });
            
          });
          deletingMessagesIds = [];
          folder = "";
        })
        
       
        $(".checkBoxMails").click(function () {
          folder = $(this).attr("name");
          let id = $(this).parent().parent().parent().attr("num");
          if ($(this).is(":checked")) {
            deletingMessagesIds.push(id);
          } else {
            let index = deletingMessagesIds.indexOf(id);
            deletingMessagesIds.splice(index, 1);
          }
          deleteJson = {
            uids: deletingMessagesIds,
            folder: folder,
          };
          // console.log(deleteJson)
        });
      })
      // Click in menu Trash to delete message begin

      $(".deleteMessage").click(function () {
        $("#mailContent").html("");
        var delete_mail
        fetch("/api/emails/trash/list")
        .then(response => response.json())
        .then(json => {
          console.log(json)
          delete_mail = json
          json.forEach((element) => {
              $("#mailContent").append(
                "<li num=" +
                  element.num +
                  ' id="' +
                  element.id +
                  '"class="list-group-item d-flex align-items-center mailListGroup"><div class="d-flex h-100 w-100 align-items-center justify-content-between"><span class="d-flex align-items-center"><input type="checkbox" class="checkBoxMails" name="' +
                  element.folder +
                  '" id="mailCheckboxes"><span class="emailNameTitle">' +
                  element.sender +
                  '</span><span class="emailSubject">' +
                  element.subject +
                  "</span></span></li>"
              );
              $(".mailListGroup").click(function () {
                $(".defaultMail").show(200);
                $(".insteadMailImage").hide(100);
                $(".file_container .list-group").html("");
                $(".file_container .file_image").html("");
                var mail = $(this).attr("id");
                var num = $(this).attr("num");
                $(".mailListGroup").each((element) => {
                  if ($(this).attr("num") == num) {
                    $(this).addClass("bg-primary text-light");
                  }
                });
                $(".mailListGroup").each(function () {
                  if ($(this)[0].id == mail) {
                    $(this).addClass("bg-primary text-light");
                  } else {
                    $(this).removeClass("bg-primary text-light");
                  }
                });
                json.forEach((element) => {
                  if (element.id == mail) {
                    $(".mailSubject").text(element.sender);
                    $(".mailSubject").attr("id", mail);
                    $(".mailSender").text(element.sender);
                    let subjectLen = element.subject.length;
                    $(".mailSubjectExpand").text(element.subject);
                    let time = element.date.split("-");
                    let endTime = time[2].split("");
                    let wholeTime =
                      time[0] +
                      "-" +
                      time[1] +
                      "-" +
                      endTime[0] +
                      "" +
                      endTime[1];
                    $(".mailDate").text(wholeTime);
                    $(".mailMovzu").html(element.content);
                    let mailSender = element.sender.split("");
                    $(".emailImage").text(
                      mailSender[0].toUpperCase() +
                        "" +
                        mailSender[1].toUpperCase()
                    );
                    if (element.attachments.length > 0) {
                      /// If txt file do this begin
                      // console.log(element.attachments)
                      var attachment = [];
                      element.attachments.forEach((element) => {
                        if (element.view_url.endsWith(".txt")) {
                          $(".file_container .list-group").append(
                            "<li class='list-group-item d-flex align-items-center justify-content-between'><span>" +
                              element.name +
                              "</span><span><button class='mr-3 btn btn-sm btn-dark show_modal_email' url=" +
                              "" +
                              element.view_url +
                              " data-toggle='modal' data-target='#file_showing_modal'><i class='fas fa-eye'></i></button><a href=" +
                              element.download_url +
                              "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                          );
                          $(".show_modal_email").click(function () {
                            $(
                              "#file_showing_modal .modal-body iframe"
                            ).removeClass("d-none");
                            $(
                              "#file_showing_modal .modal-body .email_image"
                            ).addClass("d-none");
                            $("#file_showing_modal .modal-body iframe").attr(
                              "src",
                              $(this).attr("url")
                            );
                          });
                        } else if (
                          element.view_url.endsWith(".jpg") ||
                          element.view_url.endsWith(".png") ||
                          element.view_url.endsWith(".jpeg")
                        ) {
                          $(".file_container .file_image").append(
                            "" +
                              "<div class='col-md-6  col-lg-4 mb-3' style='height:150px;position:relative'>" +
                              "<img style='height : 100%;object-fit:cover;position:relative;' class='w-100 mail_image' src=" +
                              element.view_url +
                              ">" +
                              "<button data-toggle='modal' data-target='#file_showing_modal' url=" +
                              element.view_url +
                              " class='show_modal_email_image btn btn-sm btn-dark absolute_email_btn_2 mr-3'><i class='fas fa-eye'></i></button>" +
                              "<a href=" +
                              element.download_url +
                              "><button class='btn btn-sm btn-dark absolute_email_btn'><i class='fas fa-download'></i></button></a>" +
                              "</img>" +
                              "</div>" +
                              ""
                          );
                          $(".show_modal_email_image").click(function () {
                            $("#file_showing_modal .modal-body iframe").addClass(
                              "d-none"
                            );
                            $(
                              "#file_showing_modal .modal-body .email_image"
                            ).removeClass("d-none");
                            $(
                              "#file_showing_modal .modal-body .email_image"
                            ).html(
                              "" +
                                "<img style='width:100%; height:100%;object-fit:contain' src=" +
                                $(this).attr("url") +
                                "></img>" +
                                ""
                            );
                          });
                        } else if (
                          element.view_url.endsWith(".rar") ||
                          element.view_url.endsWith(".zip")
                        ) {
                          $(".file_container .list-group").append(
                            "<li class='list-group-item alert-warning d-flex align-items-center justify-content-between'><span>" +
                              element.name +
                              " <br><small>Bu faylı görmək mümkün deyil</small> </span><span><a href=" +
                              element.download_url +
                              "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                          );
                        } else if (
                          element.view_url.endsWith(".docx") ||
                          element.view_url.endsWith(".ppt") ||
                          element.view_url.endsWith(".xls")
                        ) {
                          $(".file_container .list-group").append(
                            "<li class='list-group-item d-flex align-items-center justify-content-between'><span>" +
                              element.name +
                              "</span><span><button class='mr-3 btn btn-sm btn-dark show_modal_email' url=" +
                              "" +
                              element.view_url +
                              " data-toggle='modal' data-target='#file_showing_modal'><i class='fas fa-eye'></i></button><a href=" +
                              element.download_url +
                              "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                          );
                        } else {
                          $(".file_container .list-group").append(
                            "<li class='list-group-item alert-warning d-flex align-items-center justify-content-between'><span>" +
                              element.name +
                              " <br><small>Bu faylı görmək mümkün deyil</small> </span><span><a href=" +
                              element.download_url +
                              "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                          );
                        }
                      });
                    }
                  }
                });
  
                var deletingMessagesIds = [];
                var folder;
              });
            
          });
          deletingMessagesIds = [];
          folder = "";
        })
        
       
        $(".checkBoxMails").click(function () {
          folder = $(this).attr("name");
          let id = $(this).parent().parent().parent().attr("num");
          if ($(this).is(":checked")) {
            deletingMessagesIds.push(id);
          } else {
            let index = deletingMessagesIds.indexOf(id);
            deletingMessagesIds.splice(index, 1);
          }
          deleteJson = {
            uids: deletingMessagesIds,
            folder: folder,
          };
          // console.log(deleteJson)
        });
      });

      // Click in menu Trash to delete message end
      $(".mailListGroup").click(function () {
        $(".defaultMail").show(200);
        $(".insteadMailImage").hide(100);
        $(".file_container .list-group").html("");
        $(".file_container .file_image").html("");
        var mail = $(this).attr("id");
        var num = $(this).attr("num");
        $(".mailListGroup").each((element) => {
          if ($(this).attr("num") == num) {
            $(this).addClass("bg-primary text-light");
          }
        });
        $(".mailListGroup").each(function () {
          if ($(this)[0].id == mail) {
            $(this).addClass("bg-primary text-light");
          } else {
            $(this).removeClass("bg-primary text-light");
          }
        });
        json.forEach((element) => {
          if (element.id == mail) {
            $(".mailSubject").text(element.sender);
            $(".mailSubject").attr("id", mail);
            $(".mailSender").text(element.sender);
            let subjectLen = element.subject.length;

            $(".mailSubjectExpand").text(element.subject);
            let time = element.date.split("-");
            let endTime = time[2].split("");
            let wholeTime =
              time[0] + "-" + time[1] + "-" + endTime[0] + "" + endTime[1];
            $(".mailDate").text(wholeTime);
            $(".mailMovzu").html(element.content);
            let mailSender = element.sender.split("");
            $(".emailImage").text(
              mailSender[0].toUpperCase() + "" + mailSender[1].toUpperCase()
            );
            if (element.attachments.length > 0) {
              /// If txt file do this begin
              // console.log(element.attachments)
              var attachment = [];
              element.attachments.forEach((element) => {
                if (element.view_url.endsWith(".txt")) {
                  $(".file_container .list-group").append(
                    "<li class='list-group-item d-flex align-items-center justify-content-between'><span>" +
                      element.name +
                      "</span><span><button class='mr-3 btn btn-sm btn-dark show_modal_email' url=" +
                      "" +
                      element.view_url +
                      " data-toggle='modal' data-target='#file_showing_modal'><i class='fas fa-eye'></i></button><a href=" +
                      element.download_url +
                      "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                  );
                  $(".show_modal_email").click(function () {
                    $("#file_showing_modal .modal-body iframe").removeClass(
                      "d-none"
                    );
                    $("#file_showing_modal .modal-body .email_image").addClass(
                      "d-none"
                    );
                    $("#file_showing_modal .modal-body iframe").attr(
                      "src",
                      $(this).attr("url")
                    );
                  });
                } else if (
                  element.view_url.endsWith(".jpg") ||
                  element.view_url.endsWith(".png") ||
                  element.view_url.endsWith(".jpeg")
                ) {
                  $(".file_container .file_image").append(
                    "" +
                      "<div class='col-md-6  col-lg-4 mb-3' style='height:150px;position:relative'>" +
                      "<img style='height : 100%;object-fit:cover;position:relative;' class='w-100 mail_image' src=" +
                      element.view_url +
                      ">" +
                      "<button data-toggle='modal' data-target='#file_showing_modal' url=" +
                      element.view_url +
                      " class='show_modal_email_image btn btn-sm btn-dark absolute_email_btn_2 mr-3'><i class='fas fa-eye'></i></button>" +
                      "<a href=" +
                      element.download_url +
                      "><button class='btn btn-sm btn-dark absolute_email_btn'><i class='fas fa-download'></i></button></a>" +
                      "</img>" +
                      "</div>" +
                      ""
                  );
                  $(".show_modal_email_image").click(function () {
                    $("#file_showing_modal .modal-body iframe").addClass(
                      "d-none"
                    );
                    $(
                      "#file_showing_modal .modal-body .email_image"
                    ).removeClass("d-none");
                    $("#file_showing_modal .modal-body .email_image").html(
                      "" +
                        "<img style='width:100%; height:100%;object-fit:contain' src=" +
                        $(this).attr("url") +
                        "></img>" +
                        ""
                    );
                  });
                } else if (
                  element.view_url.endsWith(".rar") ||
                  element.view_url.endsWith(".zip")
                ) {
                  $(".file_container .list-group").append(
                    "<li class='list-group-item alert-warning d-flex align-items-center justify-content-between'><span>" +
                      element.name +
                      " <br><small>Bu faylı görmək mümkün deyil</small> </span><span><a href=" +
                      element.download_url +
                      "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                  );
                } else if (
                  element.view_url.endsWith(".docx") ||
                  element.view_url.endsWith(".ppt") ||
                  element.view_url.endsWith(".xls")
                ) {
                  $(".file_container .list-group").append(
                    "<li class='list-group-item d-flex align-items-center justify-content-between'><span>" +
                      element.name +
                      "</span><span><button class='mr-3 btn btn-sm btn-dark show_modal_email' url=" +
                      "" +
                      element.view_url +
                      " data-toggle='modal' data-target='#file_showing_modal'><i class='fas fa-eye'></i></button><a href=" +
                      element.download_url +
                      "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                  );
                } else {
                  $(".file_container .list-group").append(
                    "<li class='list-group-item alert-warning d-flex align-items-center justify-content-between'><span>" +
                      element.name +
                      " <br><small>Bu faylı görmək mümkün deyil</small> </span><span><a href=" +
                      element.download_url +
                      "><button class='btn btn-sm btn-dark'><i class='fas fa-download'></i></button></a></span></li>"
                  );
                }
              });
            }
          }
        });

        var deletingMessagesIds = [];
        var folder;
      });

      // Choose mails with checkbox to delete begin
      var deletingMessagesIds = [];
      var folder;

      $(".checkBoxMails").click(function () {
        folder = $(this).attr("name");
        let id = $(this).parent().parent().parent().attr("num");
        if ($(this).is(":checked")) {
          deletingMessagesIds.push(id);
        } else {
          let index = deletingMessagesIds.indexOf(id);
          deletingMessagesIds.splice(index, 1);
        }
        deleteJson = {

          "uids": deletingMessagesIds,
          "folder": folder,
          "flag" : "Deleted"

        };
      });

      // Choose mails with checkbox to delete end
    })
    .catch((err) => {
      console.log(err);
    });

  $("#checkboxMain").click(function () {
    if ($("#checkboxMain").is(":checked")) {
      $(".checkBoxMails").attr("checked", true);
      
    } else {
      $(".checkBoxMails").attr("checked", false);
    }
  });

  $(".noRounded1").click(function () {
    deleteJson.uids.forEach(element => {
      $(".mailListGroup").each(function() {
        if($(this).attr("num") === element ) {
          $(this).remove()
        }
      })
    })
    
    console.log(JSON.stringify(deleteJson));
    $.ajax({
      type: 'POST',
      url: '/api/email/change/flag',
      headers: { "X-CSRFToken": getCookie('csrftoken') },
      data : JSON.stringify(deleteJson),
      contentType: "application/json; charset=utf-8",

      success: function (data) {

        console.log(data)
      },

      error: function (data,jqXhr, textStatus, errorMessage) {
          console.log(data)
      }

    });
  });

  // When click spam button add mails to spam folder begin 

  $(".spam_button").click(function() {
    console.log(deleteJson.deletingMessagesIds)
    $.ajax({
      type: 'POST',
      url: "/api/email/move/folder/",
      headers: { "X-CSRFToken": getCookie('csrftoken') },
      data : JSON.stringify(deleteJson),
      contentType: "application/json; charset=utf-8",
      success: function (data) {
        console.log(data)
      },
      error: function (data,jqXhr, textStatus, errorMessage) {
          console.log(data)
      }
    });
  })


  // When click spam button add mails to spam folder begin 

});
