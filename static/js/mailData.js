$(document).ready(function () {
  var isDataCame = false;
  if(isDataCame === false) {
    $("#mailContent").append('<li id="preLoader" class="list-group-item align-items-center justify-content-center"><div class="spinner-grow float-left"  role="status"><span class="sr-only"> Loading...</span></div> <div class="float-left  h-100 d-flex align-items-center"> Loading...</div></li>')
  }
  fetch("http://127.0.0.1:8000/api/emails/")
    .then((response) => response.json())
    .then((json) => {
        if(Object.keys(json).length === 0 ) {
          isDataCame = true;
          $("#preLoader").css("display","none");
          $("#mailContent").append('<li id="preLoader" class="list-group-item align-items-center justify-content-center">Mail Yoxdur...</li>')
        }
        json.forEach(element => {
            $("#mailContent").append('<li id="'+ element.id +'" class="list-group-item d-flex align-items-center mailListGroup"><div class="asim d-flex h-100 w-100 align-items-center justify-content-between"><span class="d-flex align-items-center"><input type="checkbox" name="" id="mailCheckboxes"><span class="emailNameTitle">' + element.sender +'</span><span class="emailSubject">' + element.subject +'</span><span class="emailContentShort">' + element.num +'</span></span><span>' + element.folder + '</span></li>');
            isDataCame = true;
            $("#preLoader").css("display","none");
            
        });
        $(".mailListGroup").click(function(){
          console.log($(this).attr("id"));
          var mail = $(this).attr("id");
          json.forEach(element => {
            if(element.id == mail) {
              $(".mailSubject").text(element.sender);
              $(".mailSender").text(element.sender);
              $(".mailDate").text(element.date);
              $(".mailMovzu").text(element.content)

            }
          })


          
        });
        
    });
  $("#checkboxMain").click(function() {
      if($("#mailCheckboxes").is(":checked")) {
        $(this).attr("checked",false);
      } else {
        $(this).attr("checked",true)
      }
  }) 
  
});


