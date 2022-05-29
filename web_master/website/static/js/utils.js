function update_url(param, value) {
  // update url with new parameters
  let params = get_html_parameter_list(location.search);
  if (!params) {
    params = {};
  }
  params[param] = value;
  let new_params = "?";
  for (const [p, v] of Object.entries(params)) {
    new_params += p + "=" + v + "&";
  }
  window.history.replaceState(null, null, new_params.slice(0, -1));
}

function go_to_map() {
  window.location.href = "/home";
  window.dispatchEvent(new Event("resize"));
}

function get_html_parameter_list(querystring) {
  // returns dictionary of all html parameters
  if (querystring == "") return;
  var params = querystring.slice(1);
  var pairs = params.split("&");
  var pair, name, value;
  params = {};
  for (var i = 0; i < pairs.length; i++) {
    pair = pairs[i].split("=");
    console.log(pair);
    name = pair[0];
    if (name == "next") {
      continue;
    }
    value = pair[1];
    name = unescape(name).replace("+", " ");
    value = unescape(value).replace("+", " ");
    params[name] = value;
  }
  return params;
}

function overlay_off() {
  $("#entry_overlay").removeClass("fade_in");
  setTimeout(function () {
    $("#entry_overlay").hide();
  }, 200); // give it time to fade out
}

function deleteTarget(id) {
  fetch("/delete-entry", {
    method: "POST",
    body: JSON.stringify({ id: id }),
  }).then((_res) => {
    document.getElementById("entry_" + id.toString()).remove();
  });
}
