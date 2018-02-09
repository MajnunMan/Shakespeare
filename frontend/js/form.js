var json = JSON.parse(localStorage.getItem("content"));

$( document ).ready(function() {
  if (json) {
    $("#category-js").val(json.data.category);
    $("#camp-text-js").val(json.data.text);
  }
});

$("#form-js").submit(function(event){
    localStorage.setItem("content", null);
    let category = $("#category-js").val();
    let text = $("#camp-text-js").val();
    console.log("category: " + category);
    console.log("text: " + text);
    data = {
      category: category,
      text: text
    }
    if(text){
      $("#loading").css('display', 'block');
      $.ajax({
       type: "GET",
       url: "http://localhost:4000",
       data: data,
       success: function (result) {
           localStorage.setItem("content", JSON.stringify({data: data, result: JSON.parse(result)}));
           document.location.href = "../html-main/result.html";
      	},
        error: function (xhr, ajaxOptions, thrownErro) {
          $("#loading").css('display', 'none');
        },
        complete: function () {
          $("#loading").css('display', 'none');
        }
      });
    }
    event.preventDefault();
});

$("#continue-to-text-js").click(function(event){
  $("#step2").css('opacity', '1');
  $("#step1").css('opacity', '.3');
  $(".text-css-js").css('opacity', '1');
  $(".category-css-js").css('opacity', '.3');
  $("#camp-text-js").removeAttr("disabled");
  $("#analyze-js").removeAttr("disabled");
  $("#category-js").attr("disabled", "true");
  $("#continue-to-text-js").attr("disabled", "true");
  event.preventDefault();
});
