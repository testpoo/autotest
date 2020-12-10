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
  if (document.getElementById("type").value == '公共用例' || document.getElementById("type").value == '后置用例') {
    for (var i = 0; i < 4; i++) {
      document.getElementsByClassName("delPreNext")[i].style.display = "none";
    }
  }
  else {
    for (var i = 0; i < 4; i++) {
      document.getElementsByClassName("delPreNext")[i].style.display = "block";
    }
  }
}

// 获取模块
function getModel(model_oma, model_sicap) {
  model_oma = model_oma.split(",");
  model_sicap = model_sicap.split(",");
  if (document.getElementById("product").value == 'SiCAP') {
    parent = document.getElementById("models");
    parent.innerHTML = "";
    for (var i = 0; i < model_sicap.length; i++) {
      var option = document.createElement('option');
      option.value = model_sicap[i];
      parent.appendChild(option);
    }
  }
  else {
    parent = document.getElementById("models");
    parent.innerHTML = "";
    for (var i = 0; i < model_oma.length; i++) {
      var option = document.createElement('option');
      option.value = model_oma[i];
      parent.appendChild(option);
    }
  }
}

// 执行模式
function getExecMode() {
  if (document.getElementById("exec-mode").value == '按用例') {
    document.getElementById("select-issue-mode").style.display = "block";
    document.getElementById("select-username-mode").style.display = "none";
    document.getElementById("select-model-mode").style.display = "none";
    document.getElementById("select-version-mode").style.display = "none";
    document.getElementById("steps").value = '';
  }
  else if (document.getElementById("exec-mode").value == '按用户') {
    document.getElementById("select-issue-mode").style.display = "none";
    document.getElementById("select-username-mode").style.display = "block";
    document.getElementById("select-model-mode").style.display = "none";
    document.getElementById("select-version-mode").style.display = "none";
    document.getElementById("steps").value = '';
  }
  else if (document.getElementById("exec-mode").value == '按模块') {
    document.getElementById("select-issue-mode").style.display = "none";
    document.getElementById("select-username-mode").style.display = "none";
    document.getElementById("select-model-mode").style.display = "block";
    document.getElementById("select-version-mode").style.display = "none";
    document.getElementById("steps").value = '';
  }
  else if (document.getElementById("exec-mode").value == '按版本') {
    document.getElementById("select-issue-mode").style.display = "none";
    document.getElementById("select-username-mode").style.display = "none";
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

function getUserModes() {
  var xstep = document.getElementById("select-user").value;
  var old = document.getElementById("steps").value;
  document.getElementById("select-user").value = '';
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

// 使用用户查询案例时，显示用户列表
function getUsernames() {
  if (document.getElementById("select-model").value == '按名称') {
    document.getElementById("div-usernames").style.display = "none";
    document.getElementById("div-names").style.display = "block";
    document.getElementById("div-models").style.display = "none";
    document.getElementById("div-versions").style.display = "none";
  }
  else if (document.getElementById("select-model").value == '按用户') {
    document.getElementById("div-usernames").style.display = "block";
    document.getElementById("div-names").style.display = "none";
    document.getElementById("div-models").style.display = "none";
    document.getElementById("div-versions").style.display = "none";
  }
  else if (document.getElementById("select-model").value == '按版本') {
    document.getElementById("div-usernames").style.display = "none";
    document.getElementById("div-names").style.display = "none";
    document.getElementById("div-models").style.display = "none";
    document.getElementById("div-versions").style.display = "block";
  }
  else if (document.getElementById("select-model").value == '按模块') {
    document.getElementById("div-usernames").style.display = "none";
    document.getElementById("div-names").style.display = "none";
    document.getElementById("div-models").style.display = "block";
    document.getElementById("div-versions").style.display = "none";
  }
}

// 隐藏表格步骤过长的部分
function more(id) {
  document.getElementById('pack_' + id).style.display = "none";
  document.getElementById('more_' + id).style.display = "block";
  document.getElementById("expand_more_" + id).style.display = "none";
  document.getElementById("expand_pack_" + id).style.display = "block";
}

function pack(id) {
  document.getElementById('more_' + id).style.display = "none";
  document.getElementById('pack_' + id).style.display = "block";
  document.getElementById("expand_more_" + id).style.display = "block";
  document.getElementById("expand_pack_" + id).style.display = "none";
}

// 弹出缺陷工具
function makeIssue() {
  document.getElementById("make_issue").style.display = "block";
  document.getElementById("hidebg").style.display = "block";
  document.getElementById("hidebg").style.height = document.body.clientHeight + "px";
  document.getElementById("content").style.height = document.body.clientHeight + "px";
  document.getElementById("content").style.overflow = "hidden";
  getSteps()
}

// select取值
function getSelectValue() {
  var selectValue = document.getElementById('getSelectValue').innerHTML;
  return selectValue;
}
// 添加表格第一行
function addElementTdone() {
  var parent = document.getElementById('make_issue_tbody');
  var son = document.createElement("tr")
  son.setAttribute('class', 'make_issue_tr');
  var selectValue = getSelectValue();
  son.innerHTML = '<td contenteditable="true">' + selectValue + '</td><td contenteditable="plaintext-only" class="make_issue_td"></td><td contenteditable="plaintext-only" class="make_issue_td"></td><td contenteditable="plaintext-only" class="make_issue_td"></td><td contenteditable="plaintext-only" class="make_issue_td"></td><td contenteditable="plaintext-only" class="make_issue_td"></td><td><a href="#" onclick="addElementTd()" class="addElementTd">➕</a> <a href="#" onclick="minusElementTd()" class="minusElementTd">➖</a></td>'
  parent.insertBefore(son, parent.childNodes[0]);
}
// 添加表格
function addElementTd() {
  var e = e || window.event;
  var target = e.target || e.srcElement;
  if (target.parentNode.tagName.toLowerCase() == "td") {
    rowIndex = target.parentNode.parentNode.rowIndex;
  }
  var parent = document.getElementById('make_issue_tbody');
  var son = document.createElement("tr")
  son.setAttribute('class', 'make_issue_tr');
  var selectValue = getSelectValue();
  son.innerHTML = '<td contenteditable="true">' + selectValue + '</td><td contenteditable="plaintext-only" class="make_issue_td"></td><td contenteditable="plaintext-only" class="make_issue_td"></td><td contenteditable="plaintext-only" class="make_issue_td"></td><td contenteditable="plaintext-only" class="make_issue_td"></td><td contenteditable="plaintext-only" class="make_issue_td"></td><td><a href="#" onclick="addElementTd()" class="addElementTd">➕</a> <a href="#" onclick="minusElementTd()" class="minusElementTd">➖</a></td>'
  //if (typeof rowIndex!="undefined") {
  parent.insertBefore(son, parent.childNodes[rowIndex]);
}

// 删除表格
function minusElementTd() {
  var e = e || window.event;
  var target = e.target || e.srcElement;
  if (target.parentNode.tagName.toLowerCase() == "td") {
    rowIndex = target.parentNode.parentNode.rowIndex;
  }
  var box = document.getElementsByClassName("make_issue_tr")[rowIndex - 1];
  box.parentNode.removeChild(box);
  box.remove();
}

//function doNotDelete() {
//  alert("第一行不能删，留着肯定有用~！")
//}

// 关闭工具
function closeTable() {
  document.getElementById("make_issue").style.display = "none";
  document.getElementById("hidebg").style.display = "none";
  document.getElementById("content").style.overflow = "scroll";
}

// 补齐UiSet
function getUiset(uis) {
  var uisets = document.getElementById('getUisets-input').value;
  var uisets_dict = uisets.replace(/^\"|\'|\"|\[|\]|\:|\ |$/g, '').replace(/keyword/g, '').split('},{');
  uisets_dict[0] = uisets_dict[0].slice(1);
  uisets_dict[uisets_dict.length - 1] = uisets_dict[uisets_dict.length - 1].substr(0, uisets_dict[uisets_dict.length - 1].length - 1);
  for (j = 0; j < uisets_dict.length; j++) {
    if (uis == uisets_dict[j].split('|')[0]) {
      return uisets_dict[j];
    }
  }
}

// 二次编辑时获取数据
function getSteps() {
  var steps = document.getElementById('steps').value;
  var stepText = [];
  var setpUiSet = [];
  steps = steps.split('\n');
  var steps = steps.filter(function (el) {
    return el !== '';
  });
  num = steps.length;
  for (i = 0; i < num; i++) {
    words = steps[i].indexOf('|');
    //words = steps[i].split('|');
    word_x = steps[i].slice(0,words);
    //word_y = steps[i].slice(words+1).replace(/^\"|\'|\"$/g, '').replace(/^\(/gi, '').replace(/\)$/gi, '').split(',');
    word_y = eval(steps[i].slice(words+1).replace(/^\(/gi, '[').replace(/\)$/gi, ']'))
    //word_y = words[1].replace(/^\"|\'|\(|\)|\"$/g, '').split(',');
    setpUiSet.push(word_x);
    stepText.push(word_y);
  }
  stepTexts = eval(stepText);
  var parent = document.getElementById('make_issue_tbody');
  parent.innerHTML = '';
  for (i = 0; i < num; i++) {
    var son = document.createElement("tr")
    son.setAttribute('class', 'make_issue_tr');
    var selectValue = getSelectValue();
    son.innerHTML = '<td contenteditable="true">' + selectValue + '</td><td contenteditable="plaintext-only" class="make_issue_td"></td><td contenteditable="plaintext-only" class="make_issue_td"></td><td contenteditable="plaintext-only" class="make_issue_td"></td><td contenteditable="plaintext-only" class="make_issue_td"></td><td contenteditable="plaintext-only" class="make_issue_td"></td><td><a href="#" onclick="addElementTd()" class="addElementTd">➕</a> <a href="#" onclick="minusElementTd()" class="minusElementTd">➖</a></td>'
    parent.appendChild(son);
  }
  for (i = 0; i < stepTexts.length; i++) {
    for (j = 0; j < 5; j++) {
      if (stepTexts[i][j] == undefined) {
        document.getElementsByClassName("make_issue_td")[5 * i + j].innerHTML = '';
      }
      else {
        document.getElementsByClassName("make_issue_td")[5 * i + j].innerHTML = stepTexts[i][j];
      }
    }
  }
  for (i = 0; i < num; i++) {
    var uiset = getUiset(setpUiSet[i]);
    document.getElementsByClassName("issue_names_list")[i + 1].value = uiset;
  }
}

// 保存数据
function saveTable() {
  var stepText = []
  var list = document.getElementsByClassName("make_issue_td");
  for (var i = 0; i < list.length; i++) {
    stepText.push(list[i].innerHTML);
  }
  stepText = chunk(stepText, 5)
  var stepUiSet = []
  var listUiSet = document.getElementsByClassName("issue_names_list");
  for (var i = 0; i < listUiSet.length; i++) {
    stepUiSet.push(listUiSet[i].value);
  }
  stepUiSet = stepUiSet.slice(1);
  arr_x = [];
  last_words = '';
  for (i = 0; i < stepUiSet.length; i++) {
    arr_x = stepUiSet[i].split('|');
    word_x = arr_x[0];
    if (word_x == '') {
      alert('不能有空行~！')
    }
    word_y = arr_x[1];
    word_y_len = word_y.replace(/^\"|\"$/g, '').split(',').length;
    last_word = '';
    for (j = 0; j < word_y_len; j++) {
      if (stepText[i][j] == '') {
        last_word += ",";
      }
      else {
        last_word += "'" + stepText[i][j] + "',";
      }
    }
    last_word = last_word.substr(0, last_word.length - 1);
    if (word_x == '等待' || word_x == '隐式等待') {
      last_word = last_word.replace(/\'/g, '');
      last_words += word_x + "|(" + last_word + ")\r\n";
    }
    else {
      last_words += word_x + "|(" + last_word + ")\r\n";
    }
  }
  document.getElementById("steps").value = '';
  last_words = last_words.substr(0, last_words.length - 2);
  document.getElementById("steps").value = last_words;
  document.getElementById("make_issue").style.display = "none";
  document.getElementById("hidebg").style.display = "none";
  document.getElementById("content").style.overflow = "scroll";
}
// 数组平均分割
function chunk(array, size) {
  //获取数组的长度，如果你传入的不是数组，那么获取到的就是undefined
  const length = array.length
  //判断不是数组，或者size没有设置，size小于1，就返回空数组
  if (!length || !size || size < 1) {
    return []
  }
  //核心部分
  let index = 0 //用来表示切割元素的范围start
  let resIndex = 0 //用来递增表示输出数组的下标

  //根据length和size算出输出数组的长度，并且创建它。
  let result = new Array(Math.ceil(length / size))
  //进行循环
  while (index < length) {
    //循环过程中设置result[0]和result[1]的值。该值根据array.slice切割得到。
    result[resIndex++] = array.slice(index, (index += size))
  }
  //输出新数组
  return result
}