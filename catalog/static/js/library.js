function hint(){
  let input = document.getElementById("textbox").value
  let xttp = new XMLHttpRequest()
  xttp.onload = function() {
    let text = document.getElementById("hint");
    text.innerHTML = this.responseText;
  }
  xttp.open('GET', 'testhint.py?q='+ input)
  xttp.send()
}
