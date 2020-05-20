
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


// phone mask begin
$(document).ready(function(){
  $("#telnum").mask("+ 994" +  " (xx) xxx-xx-xx");
  $("#input_baslama_vaxti").mask("xx/xx/xxxx");
  $("#input_bitme_vaxti").mask("xx/xx/xxxx");
     });   
// phone mask end


//Choose icon via jquery begin
$(document).ready(function() {
  $("#choose_icon_button").click(function() {
    $("#icon_secmek_ucun").slideToggle()    
  });
    for (let i = 1; i <21; i++) {
      $("#icon"+i).click(function() {
        $("#choose_icon_button").html($("#icon"+i).html());
        $("#icon_secmek_ucun").slideUp(200)
      });
      }
});
//Choose icon via jquery begin


//Vaxt secimi intervallar ile begin
$(document).ready(function() {
  $("#select_box_baslig").click(function() {
    $("#select_box_alt_hisse").slideToggle()
  })
})

$(document).ready(function() {
  $(".deqiqe_0").click(function() {
    $("#select_box_baslig").html($(".deqiqe_0").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".deqiqe_hec").click(function() {
    $("#select_box_baslig").html($(".deqiqe_hec").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".deqiqe_5").click(function() {
    $("#select_box_baslig").html($(".deqiqe_5").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
   
  $(".deqiqe_10").click(function() {
    $("#select_box_baslig").html($(".deqiqe_10").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".deqiqe_15").click(function() {
    $("#select_box_baslig").html($(".deqiqe_15").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".deqiqe_30").click(function() {
    $("#select_box_baslig").html($(".deqiqe_30").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".deqiqe_45").click(function() {
    $("#select_box_baslig").html($(".deqiqe_45").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".saat_1").click(function() {
    $("#select_box_baslig").html($(".saat_1").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".saat_3").click(function() {
    $("#select_box_baslig").html($(".saat_3").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".saat_6").click(function() {
    $("#select_box_baslig").html($(".saat_6").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".saat_12").click(function() {
    $("#select_box_baslig").html($(".saat_12").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".gun_1").click(function() {
    $("#select_box_baslig").html($(".gun_1").html());
    $("#select_box_alt_hisse").slideUp(200)
  });
  $(".hefte_1").click(function() {
    $("#select_box_baslig").html($(".hefte_1").html());
    $("#select_box_alt_hisse").slideUp(200)
  })
})
//Vaxt secimi intervallar ile begin


$(document).ready(function() {
  var pathname = window.location.pathname;
  if (pathname.indexOf("/calendar/")==0 ){ 
    $('body').css('overflow', 'hidden'); 
    $('body').css('margin-top', '20px'); 
  }  
  // scrool trigger for click begin
 // https://gist.github.com/shlomohass/22249c0da0f53157dfe9#file-jquery-mousewheel-direction-capture-js
$('#calendar-ms').on('mousewheel DOMMouseScroll', function(e){
  if(typeof e.originalEvent.detail == 'number' && e.originalEvent.detail !== 0) {
    if(e.originalEvent.detail > 0) {
      $( ".fc-next-button" ).trigger( "click" );     
    } else if(e.originalEvent.detail < 0){
      $( ".fc-prev-button" ).trigger( "click" );     
           
    }
  } else if (typeof e.originalEvent.wheelDelta == 'number') {
    if(e.originalEvent.wheelDelta < 0) {
      $( ".fc-next-button" ).trigger( "click" );     
    } else if(e.originalEvent.wheelDelta > 0) {
        $( ".fc-prev-button" ).trigger( "click" );
    }
  }
}); 
// scrool trigger for click end

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
    },{
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

})



/** 
 * Professionals skills begin
*/

function openForm() {
  document.getElementById("experienceForm").style.display = "block";
}

function closeForm() {
  document.getElementById("experienceForm").style.display = "none";
}

function openSkillForm(){
  document.getElementById("skillForm").style.display = "block";
}

function closeSkillForm() {
  document.getElementById("skillForm").style.display = "none";
}

function onChangeRange(value){
  $("#progress-span").text(value);
}


function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function addExperiece(data) {
  str = "<div class='p_raw'>";
  str += "<p>" + data.title + "</p>"
  str += "<hr>"
  str += "</div>"
    
  $("#experience-info").append(str)
}

$(document).ready(function () {

  // experience related function below

  // opens and closes popup
  $("#new-exp").on("click", function() {
    $("#experienceForm").find("#add-exp").show();
    $("#experienceForm").find("#save-exp").hide();
    openForm();
  })

  // add data to database
  $("#add-exp").on("click", function () {
    data = {
      'profile': $("#profile-input").attr("profile-id"),
      'title': $('#experience-title').val(),
      'start': $('#start-date').val(),
      'end': $('#end-date').val()
    }
    $.ajax({
      headers: {
        "X-CSRFToken": getCookie('csrftoken'),
      },
      type: 'POST',
      url: '/api/experiences/',
      data: data,
      success: function (data, status, xhr) {
        // handle success 
      }
    });
  });

  // delete data from database
  $(".delete-exp").on("click", function() {
    button = this
    id = $(this).attr("data-id");
    $.ajax({
      headers: {
        "X-CSRFToken": getCookie('csrftoken'),
      },
      type: 'DELETE',
      url: '/api/experiences/' + id,
      success: function (data, status, xhr) {
        $(button).parents('.p_raw').remove();
      }
    })
  });

  // fill data in popup 
  $(".edit-exp").on("click", function() {
    $("#experienceForm").find("#add-exp").hide();
    $("#experienceForm").find("#save-exp").show();

    div = $(this).parents('.p_raw');
    title = div.find('.experience-title').text();
    start = div.find('.start-date').text().toString().split("/").join("-");
    end = div.find('.end-date').text().toString().split("/").join("-");

    console.log(start + " " + end)

    $("#experienceForm").attr('data-id', $(this).attr('data-id'))
    $("#experienceForm").attr('profile-id', $("#profile-input").attr("profile-id"));      
    $("#experienceForm").find("#experience-title").val(title)
    $("#experienceForm").find("#start-date").val(start);
    $("#experienceForm").find("#end-date").val(end);  
    
    openForm();
  });

  // update data in database
  $("#save-exp").on("click", function() {
    div = $(this).parents('.p_raw')
    id = $("#experienceForm").attr("data-id");
    data = {
      "id": id,
      'profile': $("#experienceForm").attr('profile-id'),
      'title': $('#experience-title').val(),
      'start': $('#start-date').val(),
      'end': $('#end-date').val()
    }
    $.ajax({
      headers: {
        "X-CSRFToken": getCookie('csrftoken'),
      },
      type: 'PUT',
      data: data,
      url: '/api/experiences/' + id,
      success: function (data, status, xhr) {
        // hande success
      }
    })
  })


  // skills related function below

  $("#new-skill").on("click", function() {
    $("#skillForm").find("#add-skill").show();
    $("#skillForm").find("#save-skill").hide();
    openSkillForm();
  })

  $("#add-skill").on("click", function () {
    data = {
      'profile_id': $("#profile-input").attr("profile-id"),
      'name': $('#skill-name').val(),
      'progress': $('#skill-progress').val(),
    }
    $.ajax({
      headers: {
        "X-CSRFToken": getCookie('csrftoken'),
      },
      type: 'POST',
      url: '/api/skills/',
      data: data,
      success: function (data, status, xhr) {
        addExperiece(data);
      }
    });
  });

  $(".edit-skill").on("click", function() {
    $("#skillForm").find("#add-skill").hide();
    $("#skillForm").find("#save-skill").show();

    div = $(this).parents('.p_raw');
    name = div.find('.skill-name').text();
    progress = div.find('.skill-progress').text()

    console.log(name + " " + progress)

    $("#skillForm").attr('data-id', $(this).attr('data-id'))
    $("#skillForm").attr('profile-id', $("#profile-input").attr("profile-id"));      
    $("#skillForm").find("#skill-name").val(name)
    $("#skillForm").find("#skill-progress").val(parseInt(progress));
    $("#skillForm").find("#progress-span").text(parseInt(progress))
    
    openSkillForm();
  });

  $("#save-skill").on("click", function() {
    div = $(this).parents('.p_raw')
    id = $("#skillForm").attr("data-id");
    data = {
      "id": id,
      'profile_id': $("#skillForm").attr('profile-id'),
      'name': $('#skill-name').val(),
      'progress': $('#skill-progress').val()
    }
    $.ajax({
      headers: {
        "X-CSRFToken": getCookie('csrftoken'),
      },
      type: 'PUT',
      data: data,
      url: '/api/skills/' + id,
      success: function (data, status, xhr) {
        // handle success
      }
    })
  })


  $(".delete-skill").on("click", function() {
    button = this
    id = $(this).attr("data-id");
    $.ajax({
      headers: {
        "X-CSRFToken": getCookie('csrftoken'),
      },
      type: 'DELETE',
      url: '/api/skills/' + id,
      success: function (data, status, xhr) {
        $(button).parents('.p_raw').remove();
      }
    })
  });


});



/** 
 * Professionals skills end
*/