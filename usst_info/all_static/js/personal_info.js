$("#aboutme").click(function() {
  $(".aboutme").css("display","inherit");
  $("#aboutme").addClass("active");
  $(".collection").css("display","none");
  $("#collection").removeClass("active");
});

$("#collection").click(function() {
  $(".collection").css("display","inherit");
  $("#collection").addClass("active");
  $(".aboutme").css("display","none");
  $("#aboutme").removeClass("active");
});

$("#change").click(function() {
  $("#username").attr("disabled",false);
  $("#email").attr("disabled",false);
  $("#change").css("display","none");
  $("#undo").css("display","inherit");
  $("#submit").attr("disabled",false);
});

$("#undo").click(function() {
  $("#username").attr("disabled",true);
  $("#email").attr("disabled",true);
  $("#undo").css("display","none");
  $("#change").css("display","inherit");
  $("#submit").attr("disabled",true);
});
