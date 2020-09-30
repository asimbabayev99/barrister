$(document).ready(function () {
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
  fetch("https://jsonplaceholder.typicode.com/users")
    .then((response) => response.json())
    .then((json) =>{
        json.forEach(element => {
            $("#mailContent").append('<li class="list-group-item d-flex align-items-center"><div class="d-flex h-100 w-100 align-items-center justify-content-between"><span class="d-flex align-items-center"><input type="checkbox" name="" id="mailCheckboxes"><span class="emailNameTitle">' + element.username +'</span><span class="emailSubject">' + element.name +'</span><span class="emailContentShort">' + element.company.catchPhrase +'</span></span><span>' + element.id + '</span></li>'   )
        });
    });
  fetch("emails/")
  .then((response) => response.json())
  .then((json) => {
      console.log(json)
  });
  $("#checkboxMain").click(function() {
      if($("#mailCheckboxes").is(":checked")) {
        $(this).attr("checked",false);
      } else {
        $(this).attr("checked",true)
      }
  })
  
});
