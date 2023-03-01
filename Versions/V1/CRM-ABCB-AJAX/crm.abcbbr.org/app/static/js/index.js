const sideMenu = document.querySelector("aside")
const menuBtn = document.querySelector("#menu-btn")
const closeBtn = document.querySelector("#close-btn")
const themeToggler = document.querySelector(".theme-toggler")
const btnAlert = document.querySelector(".btn-alert")

// SHOW SIDEBAR
menuBtn.addEventListener("click", () => {
    sideMenu.style.display = "block";
})

// CLOSE SIDEBAR
closeBtn.addEventListener("click", () => {
    sideMenu.style.display = "none";
})

// MUDAR TEMA
themeToggler.addEventListener("click", () => {
    document.body.classList.toggle("dark-light-variables");

    themeToggler.querySelector("span:nth-child(1)").classList.toggle("active")
    themeToggler.querySelector("span:nth-child(2)").classList.toggle("active")
})

// ALERT UPLOAD
btnAlert.addEventListener("click", () => {
    document.getElementById('alert-upload').classList.remove('alert-upload')
})

// UPLOAD DE DOCUMENTOS
document.getElementById("submitBtn").addEventListener("click", function (event) {
    event.preventDefault();

    const formData = new FormData();
    const fileField = document.querySelector('input[type="file"]');

    formData.append('files', fileField.files[0]);

    fetch('https://localhost:5000/import/import-remessa', {
        method: 'POST',
        body: formData
    })
        .then((response) => response.json())
        .then((result) => {
            document.getElementById('alert-success').classList.remove('alert-success')
        })
        .catch((error) => {
            document.getElementById('alert-error').classList.remove('alert-error')
        });

    // The rest of your code goes here
    // Consider the Mozilla docs: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#uploading_a_file
    // Send your CSRF token via the X-CSRFToken header
});

// EXPANDIR LISTA
var expanded = False;
function showCheckboxes() {
    var checkboxes = document.getElementById("checkboxes");
    if (!expanded) {
        checkboxes.style.display = "block"
        expanded = true;
    } else {
        checkboxes.style.display = "none";
        expanded = false;
    }
}


// SUBMIT AJAX
document.getElementById("submitBtn").addEventListener("click", function (event) {
    event.preventDefault();
    // The rest of your code goes here
    // Consider the Mozilla docs: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#uploading_a_file
    // Send your CSRF token via the X-CSRFToken header
    const formData = new FormData();
    const fileField = document.querySelector('input[type="file"]');

    formData.append(fileField.files[0]);

    const csrfToken = getCookie('CSRF-TOKEN');

    const headers = new Headers({
        'Content-Type': 'multipart/form-data',
        'X-CSRF-TOKEN': csrfToken
    });

    fetch('http://localhost:8080/import/send', {
        method: 'POST',
        headers: headers,
        body: formData,
    })
        .then((response) => response.json())
        .then((result) => {
            console.log('Success:', result);
        })
        .catch((error) => {
            console.error('Error:', error);
        });

});