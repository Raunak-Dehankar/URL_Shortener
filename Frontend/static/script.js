const API = "http://127.0.0.1:8000"

document.addEventListener("DOMContentLoaded", function(){

    const token = localStorage.getItem("token")

    // Only protect dashboard page
    if (window.location.pathname === "/dashboard" && !token) {
        window.location = "/"
        return
    }

    const urlList = document.getElementById("urlList")

    if (urlList) {
        loadUrls()
    }

})

async function register(){

let username = document.getElementById("reg_username").value
let email = document.getElementById("reg_email").value
let password = document.getElementById("reg_password").value

await fetch(API + "/register", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify({
username: username,
email: email,
password: password
})
})

alert("Registered successfully")
window.location = "/"
}


async function login(){

let username = document.getElementById("username").value
let password = document.getElementById("password").value

let res = await fetch(API + "/login",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
username:username,
password:password
})
})

if(res.status !== 200){
alert("Invalid username or password")
return
}

let data = await res.json()

localStorage.setItem("token", data.access_token)

if(data.role === "admin"){
window.location.href = "/admin"
}else{
window.location.href = "/dashboard"
}
}

async function shorten(){

let token = localStorage.getItem("token")

let url = document.getElementById("url").value
let alias = document.getElementById("alias").value

if(alias.trim() === ""){
    alias = null
}

let res = await fetch(API + "/shorten", {
method: "POST",
headers: {
"Content-Type": "application/json",
"Authorization": "Bearer " + token
},
body: JSON.stringify({
url: url,
alias: alias
})
})
if (!res.ok) {
    let err = await res.text()
    console.error("Shorten error:", err)
    alert("Error shortening URL")
    return
}

let data = await res.json()

document.getElementById("result").innerHTML =
data.short_url +
` <button onclick="copyToClipboard('${data.short_url}')">Copy</button>`

loadUrls()
}

async function deleteUrl(id){

let token = localStorage.getItem("token")

await fetch(API + "/delete/" + id,{
method:"DELETE",
headers:{
"Authorization":"Bearer " + token
}
})

loadUrls()
}

async function loadUrls(){

let token = localStorage.getItem("token")

let res = await fetch(API + "/myurls", {
headers:{
"Authorization":"Bearer " + token
}
})

if (!res.ok) {
    console.error("Failed to load URLs")
    return
}
let urls = await res.json()

let list = document.getElementById("urlList")

list.innerHTML = ""

urls.forEach(u => {

list.innerHTML += `

<div class="url-item">

<div class="url-title">
${u.short_url}
</div>

<div class="url-original">
${u.original_url}
</div>

<div class="url-clicks">
Clicks: ${u.clicks}
</div>

<div class="url-buttons">

<button class="copy-btn"
onclick="copyToClipboard('${u.short_url}')">
Copy
</button>

<button class="delete-btn"
onclick="deleteUrl(${u.id})">
Delete
</button>

<button class="qr-btn"
onclick="showQR('${u.short_url}')">
QR
</button>

</div>

</div>

`

})

}

function showQR(url){

let modal = document.getElementById("qrModal")
let canvasArea = document.getElementById("qrCanvas")

canvasArea.innerHTML = ""

QRCode.toCanvas(url, {width:200}, function (error, canvas){

if(error){
console.error(error)
return
}

canvasArea.appendChild(canvas)

})

modal.style.display = "flex"

}

function closeQR(){

document.getElementById("qrModal").style.display = "none"

}

function logout(){

localStorage.removeItem("token")

window.location="/"

}
