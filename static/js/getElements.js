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