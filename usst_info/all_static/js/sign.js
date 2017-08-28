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

//入学年份
function addGrade() {
  var thisyear = new Date().getFullYear();
  for(var i = thisyear - 6; i <= thisyear; i++) {
    var addyear = "<option value='" + i + "'>" + i + "</option>";
    $("#signup_grade").append(addyear);
  }
}
addGrade();

//根据学院更改专业
$("#signup_college").change(function() {
  var department = $("#signup_major");
  var college = $("#signup_college").val();
  switch(college) {
    case "1": {
      department.empty();
      department.append("<option value='0'>未分专业</option>");
      department.append("<option value='1'>过程装备与控制工程</option>");
      department.append("<option value='2'>新能源科学与工程</option>");
      department.append("<option value='3'>能源与动力工程</option>");
    } break;
    case "2": {
      department.empty();
      department.append("<option value='0'>未分专业</option>");
      department.append("<option value='1'>测控技术与仪器</option>");
      department.append("<option value='2'>电子信息工程</option>");
      department.append("<option value='3'>通信工程</option>");
      department.append("<option value='4'>电子科学与技术</option>");
      department.append("<option value='5'>智能科学与技术</option>");
      department.append("<option value='6'>计算机科学与技术</option>");
      department.append("<option value='7'>网络工程</option>");
      department.append("<option value='8'>电气工程及其自动化</option>");
      department.append("<option value='9'>自动化</option>");
      department.append("<option value='10'>光电信息科学与工程</option>");
      department.append("<option value='11'>光电信息科学与工程(中德合作)</option>");
    } break;
    case "3": {
      department.empty();
      department.append("<option value='0'>未分专业</option>");
      department.append("<option value='1'>国际金融与贸易</option>");
      department.append("<option value='2'>金融学</option>");
      department.append("<option value='3'>管理科学</option>");
      department.append("<option value='4'>信息管理与信息系统</option>");
      department.append("<option value='5'>工业工程</option>");
      department.append("<option value='6'>工商管理(中美合作)</option>");
      department.append("<option value='7'>会计学</option>");
      department.append("<option value='8'>公共事业管理</option>");
      department.append("<option value='9'>公共事业管理(体育)</option>");
      department.append("<option value='10'>税收学</option>");
    } break;
    case "4": {
      department.empty();
      department.append("<option value='0'>未分专业</option>");
      department.append("<option value='1'>机械设计制造及其自动化</option>");
      department.append("<option value='2'>车辆工程</option>");
      department.append("<option value='3'>机械设计制造及其自动化(国际工程)(中德合作)</option>");
    } break;
    case "5": {
      department.empty();
      department.append("<option value='0'>未分专业</option>");
      department.append("<option value='1'>英语</option>");
      department.append("<option value='2'>德语</option>");
      department.append("<option value='3'>日语</option>");
      department.append("<option value='4'>英语(中美合作)</option>");
    } break;
    case "6": {
      department.empty();
      department.append("<option value='0'>未分专业</option>");
      department.append("<option value='1'>土木工程</option>");
      department.append("<option value='2'>环境工程</option>");
      department.append("<option value='3'>建筑环境与能源应用工程</option>");
    } break;
    case "7": {
      department.empty();
      department.append("<option value='0'>未分专业</option>");
      department.append("<option value='1'>生物医学工程</option>");
      department.append("<option value='2'>食品科学与工程</option>");
      department.append("<option value='3'>食品质量与安全</option>");
      department.append("<option value='4'>医学影像技术</option>");
      department.append("<option value='5'>医学信息工程</option>");
      department.append("<option value='6'>制药工程</option>");
      department.append("<option value='7'>假肢矫形工程</option>");
    } break;
    case "8": {
      department.empty();
      department.append("<option value='0'>未分专业</option>");
      department.append("<option value='1'>广告学</option>");
      department.append("<option value='2'>编辑出版学</option>");
      department.append("<option value='3'>传播学</option>");
      department.append("<option value='4'>包装工程</option>");
      department.append("<option value='5'>工业设计</option>");
      department.append("<option value='6'>动画</option>");
      department.append("<option value='7'>视觉传达设计</option>");
      department.append("<option value='8'>产品设计</option>");
      department.append("<option value='9'>环境设计</option>");
      department.append("<option value='10'>印刷工程(卓越班)</option>");
    } break;
    case "9": {
      department.empty();
      department.append("<option value='0'>未分专业</option>");
      department.append("<option value='1'>数学与应用数学</option>");
      department.append("<option value='2'>应用物理学</option>");
      department.append("<option value='3'>应用化学</option>");
    } break;
    case "10": {
      department.empty();
      department.append("<option value='0'>未分专业</option>");
      department.append("<option value='1'>电气工程及其自动化(中德合作)</option>");
    } break;
    case "11": {
      department.empty();
      department.append("<option value='0'>未分专业</option>");
      department.append("<option value='1'>电子信息科学与技术</option>");
      department.append("<option value='2'>机械设计及其自动化(中英合作)</option>");
      department.append("<option value='3'>会展经济与管理(中英合作)</option>");
      department.append("<option value='4'>工商管理</option>");
    } break;
    case "12": {
      department.empty();
      department.append("<option value='0'>未分专业</option>");
      department.append("<option value='1'>材料科学与工程</option>");
      department.append("<option value='2'>材料科学与工程(卓越班)</option>");
      department.append("<option value='3'>材料成型及控制工程</option>");
    }
  }
});
