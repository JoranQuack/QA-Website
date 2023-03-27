// SCROLL FUNCTIONS
document.documentElement.dataset.scroll_position = window.scrollY.toString();

document.addEventListener('scroll', () => {
    document.documentElement.dataset.scroll_position = window.scrollY.toString();
    if (window.scrollY > 200) {
        document.getElementById("header")?.classList.remove("header-spaced");
        document.getElementById("header")?.classList.add("header-condense");
    } else {
        document.getElementById("header")?.classList.remove("header-condense");
        document.getElementById("header")?.classList.add("header-spaced");
    }
});


// MOBILE MENU
function menuOnClick() {
    document.getElementById("menu-bar")?.classList.toggle("change");
    document.getElementById("nav")?.classList.toggle("change");
    document.getElementById("menu-bg")?.classList.toggle("change-bg");
}


// PERFECT SCROLLBAR
const container = document.querySelector('#main');
// const ps = new PerfectScrollbar(container);
// ps.update();


// MAP STUFF
function initMap() {
    // The location
    const location = { lat: -43.531259, lng: 172.570716 };
    // The map, centered
    // @ts-ignore
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: location,
        mapId: "377fce5ade22f0c6",
        disableDefaultUI: true,
    });
    // The marker, positioned
    // @ts-ignore
    const marker = new google.maps.Marker({
        position: location,
        map: map,
    });
}
window.initMap = initMap;