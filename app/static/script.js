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

document.getElementById("result").innerText = data.short_url
}

function logout(){

localStorage.removeItem("token")

window.location="/"

}