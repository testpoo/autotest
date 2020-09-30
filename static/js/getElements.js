function getElements() {
  var xstep = document.getElementsByName("choice")[0].value;
  var old = document.getElementById("steps").value;
  document.getElementsByName("choice")[0].value = '';
  if (old == '') {
    document.getElementById("steps").value = (old + ";" + xstep).substr(1);
  }
  else {
    document.getElementById("steps").value = old + ";" + xstep;
  }
}

function loading() {
  document.getElementById("loadDiv").style.display = "block";
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