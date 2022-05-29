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
