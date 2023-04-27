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


// HEADER SCROLL FUNCTIONS
document.documentElement.dataset.scroll_position = window.scrollY.toString();
var scrollValue = 50

document.addEventListener('scroll', () => {
    document.documentElement.dataset.scroll_position = window.scrollY.toString();
    if (window.scrollY > scrollValue) {
        document.getElementById("header")?.classList.remove("header-spaced");
        document.getElementById("header")?.classList.add("header-condense");
    } else {
        document.getElementById("header")?.classList.remove("header-condense");
        document.getElementById("header")?.classList.add("header-spaced");
    }
});


// FUNCTIONS ONLY APPLICABLE TO HOME PAGE
if (document.title == "Home") {
    var scrollValue = 120


    // MOBILE MENU
    function menuOnClick() {
        document.getElementById("menu-bar")?.classList.toggle("change");
        document.getElementById("nav")?.classList.toggle("change");
        document.getElementById("menu-bg")?.classList.toggle("change-bg");
    }


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
        sleep(1000).then(() => { scrolling = true });
    }
}

// FUNCTIONS ONLY APPLICABLE TO ALBUM PAGE
if (document.title == "Album") {


    // lightbox open
    function lightboxOpen(src) {
        let imgSrc = `/static/images/uploaded/${src}`
        document.getElementById('lightbox-img')?.setAttribute('src', imgSrc);

        document.getElementById('lightbox')?.classList.remove("lightbox-closed")
        document.getElementById('lightbox')?.classList.add("lightbox-opening")
        sleep(10).then(() => {
            document.getElementById('lightbox')?.classList.remove("lightbox-opening")
            document.getElementById('lightbox')?.classList.add("lightbox-opened")
        });
    }


    // lightbox close
    function lightboxClose() {
        document.getElementById('lightbox')?.classList.remove("lightbox-opened")
        document.getElementById('lightbox')?.classList.add("lightbox-closing")
        sleep(300).then(() => {
            document.getElementById('lightbox')?.classList.remove("lightbox-closing")
            document.getElementById('lightbox')?.classList.add("lightbox-closed")
        });
    }

    // closing the lightbox on pressing the Escape key.
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            lightboxClose();
        }
    });

}