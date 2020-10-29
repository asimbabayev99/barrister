$(document).ready(function () {
  var isDataCame = false,
    inbox = [],
    deleteJson = {};
  if (isDataCame === false) {
    $("#mailContent").append(
      '<li id="preLoader" class="list-group-item align-items-center justify-content-center"><div class="spinner-grow float-left"  role="status"><span class="sr-only"> Loading...</span></div> <div class="float-left  h-100 d-flex align-items-center"> Loading...</div></li>'
    );
  }
  fetch("http://127.0.0.1:8000/api/emails/?ordering=-date")
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
              element.subject +
              "</span></span>"+
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
              var mail = $(this).attr("id");
              json.forEach((element) => {
                if (element.id == mail) {
                  $(".mailSubject").text(element.sender);
                  $(".mailSubject").attr("id", element.id);
                  $(".mailSender").text(element.sender);
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
                  let color = [
                    "purple",
                    "blue",
                    "green",
                    "maroon",
                    "darkorange",
                  ];
                  $(".emailImage").text(
                    mailSender[0].toUpperCase() +
                      "" +
                      mailSender[1].toUpperCase()
                  );
                  let rNumber = Math.floor(Math.random() * 5);
                  $(".emailImage").css({
                    backgroundColor: color[rNumber],
                  });
                }
              });
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
          if(element.folder == "Sent") {
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
              var mail = $(this).attr("id");
              json.forEach((element) => {
                if (element.id == mail) {
                  $(".mailSubject").text(element.sender);
                  $(".mailSender").text(element.sender);
                  $(".mailSubjectExpand").text(element.subject);
                  let time = element.date.split("-");
                  let endTime = time[2].split("");
                  let wholeTime =
                  time[0] + "-" + time[1] + "-" + endTime[0] + "" + endTime[1];
                  $(".mailDate").text(wholeTime);
                  $(".mailMovzu").html(element.content);
                  let mailSender = element.sender.split("");
                  let color = ["purple", "blue", "green", "maroon", "darkorange"];
                  $(".emailImage").text(
                    mailSender[0].toUpperCase() + "" + mailSender[1].toUpperCase()
                    );
                    let rNumber = Math.floor(Math.random() * 5);
                    $(".emailImage").css({
                      backgroundColor: color[rNumber],
                    });
                  }
                });
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



      // Click in menu Trash to delete message begin

      $(".deleteMessage").click(function () {
        $("#mailContent").html("");
        json.forEach((element) => {
          if (element.folder === "Trash") {
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
              $(".mailSubject").html(
                '<div class="spinner-grow text-dark" role="status"><span class="sr-only">Loading...</span></div>'
              );
              $(".mailSender").html(
                '<div class="spinner-grow spinner-grow-sm text-dark" role="status"><span class="sr-only">Loading...</span></div>'
              );

              $(".mailSubjectExpand").html("");
              $(".mailDate").html("");
              $(".mailMovzu").html("");
              setTimeout(() => {
                $(".defaultMail").show(200);
                $(".insteadMailImage").hide(100);
                var mail = $(this).attr("id");
                json.forEach((element) => {
                  if (element.id == mail) {
                    $(".mailSubject").text(element.sender);
                    $(".mailSender").text(element.sender);
                    $(".mailSubjectExpand").text(element.subject);
                    $(".mailDate").text(wholeTime);
                    $(".mailMovzu").html(element.content);
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
                    let mailSender = element.sender.split("");
                    let color = [
                      "purple",
                      "blue",
                      "green",
                      "maroon",
                      "darkorange",
                    ];
                    $(".emailImage").html(
                      mailSender[0].toUpperCase() +
                        "" +
                        mailSender[1].toUpperCase()
                    );
                    let rNumber = Math.floor(Math.random() * 5);

                    $(".emailImage").css({
                      backgroundColor: color[rNumber],
                    });
                  }
                });
              }, 1000);
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
          // console.log(deleteJson)
        });
      });

      // Click in menu Trash to delete message end
      $(".mailListGroup").click(function () {
        $(".defaultMail").show(200);
        $(".insteadMailImage").hide(100);
        $(".file_container").html("")
        var mail = $(this).attr("id");

        json.forEach((element) => {
          if (element.id == mail) {
            $(".mailSubject").text(element.sender);
            $(".mailSubject").attr("id", mail);
            $(".mailSender").text(element.sender);
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
            if(element.attachments.length > 0) {

              $(".file_container").append("<a href='" + element.attachments[0].download_url+"'> File </a>")
            }
            
            // console.log(element.attachments[0].view_url)
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
          uids: deletingMessagesIds,
          folder: folder,
        };
        // console.log(deleteJson)
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
    console.log(deleteJson);
  });
});
