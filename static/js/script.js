// SLEEP FUCNTION
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


// WAIT FOR ELEMENT TO EXIST
function waitForElm(selector) {
    return new Promise(resolve => {
        if (document.querySelector(selector)) {
            return resolve(document.querySelector(selector));
        }

        const observer = new MutationObserver(mutations => {
            if (document.querySelector(selector)) {
                resolve(document.querySelector(selector));
                observer.disconnect();
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    });
}


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
// const container = document.querySelector('#main');
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

// UPDATE NAV BAR WHEN SCROLLING
var scrolling = true;

window.onscroll = () => {
    if (scrolling) {
        var current = "";

        document.querySelectorAll("section").forEach((section) => {
            const sectionTop = section.offsetTop;
            if (scrollY >= sectionTop) {
                // @ts-ignore
                current = section.getAttribute("id");
            }
        });

        document.querySelectorAll(".nav a").forEach((a) => {
            a.classList.remove("active");
            if (a.classList.contains(current)) {
                a.classList.add("active");
            }
        });
    };
};


// UPDATE NAV BAR WHEN CLICKED
function navOnClick(_navId) {
    scrolling = false;
    var inactives = document.getElementsByClassName("link");
    for (let inactive of inactives) {
        inactive.classList.remove("active");
    };
    document.getElementsByClassName(_navId)[0].classList.add("active");
    document.getElementById(_navId)?.scrollIntoView({});
    sleep(1000).then(() => { scrolling = true });
}