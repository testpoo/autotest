// 步骤
function getElements() {
  var xstep = document.getElementsByName("choice")[0].value;
  var old = document.getElementById("steps").value;
  document.getElementsByName("choice")[0].value = '';
  if (old == '') {
    document.getElementById("steps").value = xstep;
  }
  else {
    document.getElementById("steps").value = old + "\n" + xstep;
  }
}
// 前置事件
function getPres() {
  var xstep = document.getElementById("pre-choice").value;
  var old = document.getElementById("pre-steps").value;
  document.getElementsByName("pre-choice")[0].value = '';
  if (old == '') {
    document.getElementById("pre-steps").value = xstep;
  }
  else {
    document.getElementById("pre-steps").value = old + "\n" + xstep;
  }
}
// 后置事件
function getNexts() {
  var xstep = document.getElementById("next-choice").value;
  var old = document.getElementById("next-steps").value;
  document.getElementsByName("next-choice")[0].value = '';
  if (old == '') {
    document.getElementById("next-steps").value = xstep;
  }
  else {
    document.getElementById("next-steps").value = old + "\n" + xstep;
  }
}

function loading() {
  document.getElementById("loadDiv").style.display = "block";
}

// 公共案例去掉前置后置事件
function delPreNext() {
  if (document.getElementById("type").value == '公共用例'){
    for (var i=0;i<4;i++){
      document.getElementsByClassName("delPreNext")[i].style.display = "none";
    }
  }
  else {
    for (var i=0;i<4;i++){
      document.getElementsByClassName("delPreNext")[i].style.display = "block";
    }
  }
}

function test() {
  alert("test");
}


/*
function getModel() {
  var product = document.getElementsByName("product")[0].value;
  var model_all = document.getElementById("model_all");
  if (product="SiCAP") {
    var div = document.getElementById("model_sicap");
  }
  else if (product="OMA") {
    var div = document.getElementById("model_oma");
  }
  div.style.cssText="display:none;"
  div.style.cssText="display:block;"
}*/