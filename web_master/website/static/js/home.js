function toggle_visibility(div) {
  input_table = document.getElementById(div);
  if (input_table.style.display == "none") {
    input_table.style.display = "flex";
  } else {
    input_table.style.display = "none";
  }
}

location_form = document.getElementById("location_form");
location_form.addEventListener("submit", (e) => {
  e.preventDefault();
  const urlParams = new URLSearchParams(window.location.search);

  var xhr = new XMLHttpRequest();
  xhr.open("POST", `/api/edit_location?l_id=${urlParams.get("l_id")}`);
  xhr.onload = function () {
    location.reload();
  };
  var formData = new FormData(location_form);
  xhr.send(formData);
});

entry_form = document.getElementById("entry_form");
entry_form.addEventListener("submit", (e) => {
  e.preventDefault();
  const urlParams = new URLSearchParams(window.location.search);

  var xhr = new XMLHttpRequest();
  xhr.open("POST", `/api/new_entry?l_id=${urlParams.get("l_id")}`);
  xhr.onload = function () {
    if (this.status == 200) {
      let data = JSON.parse(this.response);

      entry_elements_div.style.display = "flex";

      let li_string =
        `<li class="card_item" id="entry_${data.id}">` +
        '   <div class="img_container">' +
        `     <img src="data:image/${data.image_data_type};base64,${data.image}" class="card_img"></img>` +
        "   </div>" +
        `   <h2>${data.title}</h2>` +
        `   <p>${data.category}</p>` +
        "</li>";
      let li_template = document.createElement("template");
      li_template.innerHTML = li_string;
      var ul = document.getElementById("entries");
      let li = li_template.content.firstChild;

      ul.appendChild(li);

      li.addEventListener("click", (e) => {
        entry_overlay.innerHTML =
          "<div class='inner_overlay flex-column' style='justify-content: flex-start;'>" +
          "<h1 style='margin-top: 15px;'>" +
          data.title +
          "</h1>" +
          "<div class='flex-column' style='width: 90%;'>" +
          "<img src='data:image/" +
          data.image_data_type +
          ";base64," +
          data.image +
          "' class='preview_img'><p>" +
          data.text +
          "</p>" +
          "</div></div>";
        $("#entry_overlay").show();
        $("#entry_overlay").addClass("fade_in");
      });
    }
  };
  var formData = new FormData(entry_form);
  xhr.send(formData);
});
