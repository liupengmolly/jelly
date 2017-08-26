//切换登录与注册
$("#signin-li").click(function() {
  $(".signin").css("display","inherit");
  $(".signup").css("display","none");
  $(".signup-li").css("background-color","#4a5dec");
  $(".signin-li").css("background-color","inherit");
});

$("#signup-li").click(function() {
  $(".signup").css("display","inherit");
  $(".signin").css("display","none");
  $(".signin-li").css("background-color","#4a5dec");
  $(".signup-li").css("background-color","inherit");
});

//登录输入验证


//注册输入验证
