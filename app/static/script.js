const API = "http://127.0.0.1:8000"

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

let res = await fetch("/login",{
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

window.location="/dashboard"
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

let urls = await res.json()

let list = document.getElementById("urlList")

list.innerHTML = ""

urls.forEach(u => {

list.innerHTML += `
<div style="margin:10px;padding:10px;border:1px solid gray">

<p>
<strong>Short:</strong> ${u.short_url}
<button onclick="copyToClipboard('${u.short_url}')">Copy</button>
</p>

<p>
<strong>Original:</strong> ${u.original_url}
</p>

<p>
Clicks: ${u.clicks}
</p>

<button onclick="deleteUrl(${u.id})">Delete</button>

</div>
`

})

}

function logout(){

localStorage.removeItem("token")

window.location="/"

}

loadUrls()

