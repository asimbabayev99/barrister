$(document).ready(function () {
  var isDataCame = false;
  if(isDataCame === false) {
    $("#mailContent").append('<li id="preLoader" class="list-group-item align-items-center justify-content-center"><div class="spinner-grow float-left"  role="status"><span class="sr-only"> Loading...</span></div> <div class="float-left  h-100 d-flex align-items-center"> Loading...</div></li>')
  }
  fetch("http://127.0.0.1:8000/api/emails")
    .then((response) => response.json())
    .then((json) => {
        if(Object.keys(json).length === 0 ) {
          isDataCame = true;
          $("#preLoader").css("display","none");
          $("#mailContent").append('<li id="preLoader" class="list-group-item align-items-center justify-content-center">Mail Yoxdur...</li>')
        }
        json.forEach(element => {

            if(element.folder === "Inbox")
            { 
              $("#mailContent").append('<li id="'+ element.id +'" class="list-group-item d-flex align-items-center mailListGroup"><div class="d-flex h-100 w-100 align-items-center justify-content-between"><span class="d-flex align-items-center"><input type="checkbox" class="checkBoxMails" name="" id="mailCheckboxes"><span class="emailNameTitle">' + element.sender +'</span><span class="emailSubject">' + element.subject +'</span></span></li>');
              isDataCame = true;
              $("#preLoader").css("display","none");
            } else {
              console.log(element.folder)
            }
            
        });
        $(".mailListGroup").click(function(){
          console.log($(this).attr("id"));
          var mail = $(this).attr("id");
          json.forEach(element => {
            if(element.id == mail) {
              // $("#" + mail).css("background","#007bff");
              $(".mailSubject").text(element.sender);
              $(".mailSender").text(element.sender);
              $(".mailSubjectExpand").text(element.subject)
              let time = element.date.split("-");
              let endTime = time[2].split("");
              let wholeTime = time[0] + "-" + time[1]+ "-" + endTime[0] + "" + endTime[1]
              $(".mailDate").text(wholeTime);
              $(".mailMovzu").html(element.content);
              let mailSender = element.sender.split('');
              let color = ["purple","blue","green","maroon","darkorange"];
              $(".emailImage").text(mailSender[0].toUpperCase() + '' + mailSender[1].toUpperCase());
              let rNumber = Math.floor(Math.random()*5);
              console.log(rNumber)
              $(".emailImage").css({
                backgroundColor : color[rNumber]
              })          
            }
          })
                   
        });
        
        
    });
  $("#checkboxMain").click(function() {
      
        if($("#checkboxMain").is(":checked")) {
          $(".checkBoxMails").attr("checked", true)
        } else {
          $(".checkBoxMails").attr("checked", false)
        }
      
  }) 
  
});


