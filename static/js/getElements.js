// 用例步骤
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

// 滚动条的显示
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

// 获取模块
function getModel(model_oma,model_sicap) {
  model_oma = model_oma.split(",");
  model_sicap = model_sicap.split(",");
  if (document.getElementById("product").value == 'SiCAP') {
    parent = document.getElementById("models");
    parent.innerHTML = "";
    for (var i=0;i<model_sicap.length;i++) {
      var option=document.createElement('option');
      option.value=model_sicap[i];
      parent.appendChild(option);
    }
  }
  else {
    parent = document.getElementById("models");
    parent.innerHTML = "";
    for (var i=0;i<model_oma.length;i++) {
      var option=document.createElement('option');
      option.value=model_oma[i];
      parent.appendChild(option);
    }
  }
}

// 执行模式
function getExecMode() {
  if (document.getElementById("exec-mode").value == '按用例'){
    document.getElementById("select-issue-mode").style.display = "block";
    document.getElementById("select-model-mode").style.display = "none";
    document.getElementById("select-version-mode").style.display = "none";
    document.getElementById("steps").value = '';
  }
  else if (document.getElementById("exec-mode").value == '按模块') {
    document.getElementById("select-issue-mode").style.display = "none";
    document.getElementById("select-model-mode").style.display = "block";
    document.getElementById("select-version-mode").style.display = "none";
    document.getElementById("steps").value = '';
  }
  else if (document.getElementById("exec-mode").value == '按版本') {
    document.getElementById("select-issue-mode").style.display = "none";
    document.getElementById("select-model-mode").style.display = "none";
    document.getElementById("select-version-mode").style.display = "block";
    document.getElementById("steps").value = '';
  }
}

// 用例集
function getIssueModes() {
  var xstep = document.getElementById("select-issue").value;
  var old = document.getElementById("steps").value;
  document.getElementById("select-issue").value = '';
  if (old == '') {
    document.getElementById("steps").value = xstep;
  }
  else {
    document.getElementById("steps").value = old + "\n" + xstep;
  }
}

function getModelModes() {
  var xstep = document.getElementById("select-model").value;
  var old = document.getElementById("steps").value;
  document.getElementById("select-model").value = '';
  if (old == '') {
    document.getElementById("steps").value = xstep;
  }
  else {
    document.getElementById("steps").value = old + "\n" + xstep;
  }
}

function getVersionModes() {
  var xstep = document.getElementById("select-version").value;
  var old = document.getElementById("steps").value;
  document.getElementById("select-version").value = '';
  if (old == '') {
    document.getElementById("steps").value = xstep;
  }
  else {
    document.getElementById("steps").value = old + "\n" + xstep;
  }
}

// 隐藏表格步骤过长的部分
function more(id) {
  document.getElementById('pack_'+id).style.display = "none";
  document.getElementById('more_'+id).style.display = "block";
  document.getElementById("expand_more_"+id).style.display = "none";
  document.getElementById("expand_pack_"+id).style.display = "block";
}

function pack(id) {
  document.getElementById('more_'+id).style.display = "none";
  document.getElementById('pack_'+id).style.display = "block";
  document.getElementById("expand_more_"+id).style.display = "block";
  document.getElementById("expand_pack_"+id).style.display = "none";
}