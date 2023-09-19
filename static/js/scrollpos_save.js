// @ts-nocheck
document.addEventListener("DOMContentLoaded", function (event) {
    const scrollpos = localStorage.getItem("scrollpos");
    if (scrollpos) window.scrollTo(0, scrollpos);
});

window.onscroll = function (e) {
    localStorage.setItem("scrollpos", window.scrollY);
};