function table_toggler(input) {
  let input_table = document.getElementById("input_table");
  let display_table = document.getElementById("display_table");

  if (input == 1) {
    display_table.style.display = "none";
    input_table.style.display = "block";
  } else {
    display_table.style.display = "block";
    input_table.style.display = "none";
  }
}

pw_field = $("#password");
button = $("#submit");
pw_message = $("#pw_message")[0];
const pw_regex =
  "^(?=.*([A-Z]){1,})(?=.*[!@#$&*]{1,})(?=.*[0-9]{1,})(?=.*[a-z]{1,}).{8,30}$";
pw_field.on("keyup", (e) => {
  if (pw_field[0].value.length == 0) {
    button.prop("disabled", false);
    button.toggleClass("disabled", false);
    pw_message.innerHTML = "";
  } else if (pw_field[0].value.length < 8) {
    pw_message.style.color = "darkred";
    pw_message.innerHTML = "Passwort zu kurz";
    button.prop("disabled", true);
    button.toggleClass("disabled", true);
  } else if (pw_field[0].value.length > 30) {
    pw_message.style.color = "darkred";
    pw_message.innerHTML = "Passwort zu lang";
    button.prop("disabled", true);
    button.toggleClass("disabled", true);
  } else if (pw_field[0].value.match(pw_regex) === null) {
    pw_message.style.color = "darkred";
    pw_message.innerHTML =
      "Sonderzeichen (!@#$&*), Zahl, Groß- und Kleinbuchstaben benötigt";
    button.prop("disabled", true);
    button.toggleClass("disabled", true);
  } else {
    pw_message.style.color = "green";
    pw_message.innerHTML = "Valides Passwort";
    button.prop("disabled", false);
    button.toggleClass("disabled", false);
  }
});
