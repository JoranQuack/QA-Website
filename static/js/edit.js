// @ts-nocheck
async function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

function previewImage(id) {
    console.log("banana")
    const file = document.getElementById(`image${id}`).files;
    if (file.length > 0) {
        const fileReader = new FileReader()
        fileReader.onload = function (event) {
            document.getElementById(`preview${id}`).setAttribute("src", event.target.result);
        };
        fileReader.readAsDataURL(file[0]);
    }
}

async function onFormFieldChange(e) {
    const btn = e.querySelector("#submit")
    await sleep(300)
    btn.classList.remove('submit-hidden')
    btn.classList.add('submit-shown')
}

// HIDE USERS ON DELETE
async function hideObject(object_name, ID, confirm_req) {
    let object = document.getElementById(`${object_name}_${ID}`);

    if (object_name === 'user_row') {
        let tds = document.getElementsByClassName(`user_td_${ID}`)
        for (var td of tds) {
            td.classList.add("animate-collapse_row")
        };
        object.classList.add("animate-collapse_row")
    }
    else {
        object.classList.add("animate-fade_out");
    };

    object.classList.add("hidden");
    if (confirm_req) {
        let remove_btn = document.getElementById(`${object_name}_remove_${ID}`)
        console.log(remove_btn)
        remove_btn.classList.remove("hidden");
        remove_btn.classList.add("flex");
        remove_btn.classList.add("animate-fade_in");
    };
};