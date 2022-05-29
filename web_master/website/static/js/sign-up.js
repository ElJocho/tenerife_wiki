pw_field = $("#password1");
pw_field_2 = $("#password2");
button = $(".hero-button");
button.prop("disabled", true);
unlock = false;
pw_message = $("#pw_message")[0];
const pw_regex =
  "^(?=.*([A-Z]){1,})(?=.*[!@#$&*]{1,})(?=.*[0-9]{1,})(?=.*[a-z]{1,}).{8,30}$";
pw_field.on("keyup", (e) => {
  if (pw_field[0].value.length < 8) {
    pw_message.style.color = "darkred";
    pw_message.innerHTML = "Passwort zu kurz";
    button.prop("disabled", true);
  } else if (pw_field[0].value.length > 30) {
    pw_message.style.color = "darkred";
    pw_message.innerHTML = "Passwort zu lang";
    button.prop("disabled", true);
  } else if (pw_field[0].value.match(pw_regex) === null) {
    pw_message.style.color = "darkred";
    pw_message.innerHTML =
      "Sonderzeichen, Zahl sowie Groß und Kleinbuchstaben benötigt";
    button.prop("disabled", true);
  } else {
    pw_message.style.color = "green";
    pw_message.innerHTML = "Valides Passwort";
    if (pw_field[0].value == pw_field_2[0].value) {
      button.prop("disabled", false);
    } else if (
      (pw_field[0].value != pw_field_2[0].value) &
      (pw_field_2[0].value.length > 0)
    )
      pw_message.style.color = "darkred";
    pw_message.innerHTML = "Passwörter stimmen nicht überein";
  }
});
pw_field_2.on("keyup", (e) => {
  if (pw_field[0].value == pw_field_2[0].value) {
    pw_message.style.color = "green";
    pw_message.innerHTML = "Passwörter stimmen überein";
    button.prop("disabled", false);
  } else {
    pw_message.style.color = "darkred";
    pw_message.innerHTML = "Passwörter stimmen nicht überein";
    button.prop("disabled", true);
  }
});
