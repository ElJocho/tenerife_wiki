$("#header").hover(
  () => {
    $(".anim-menu").toggleClass("special");
    $(".profile-div").toggleClass("special");
  },
  function () {
    // on mouseout, reset the background colour
    $(".anim-menu").toggleClass("special");
    $(".profile-div").toggleClass("special");
  }
);

function profile(id) {
  update_url("u_id", id);
  window.location.href = "/profile?" + new URLSearchParams(location.search);
}
