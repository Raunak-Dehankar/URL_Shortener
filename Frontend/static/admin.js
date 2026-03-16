const API = "http://127.0.0.1:8000"

const token = localStorage.getItem("token")

async function logout(){
localStorage.removeItem("token")
window.location="/"
}

async function loadUsers(){

let res = await fetch(API + "/admin/users", {
headers:{
"Authorization":"Bearer " + token
}
})

let users = await res.json()

let container = document.getElementById("usersList")

container.innerHTML = ""

users.forEach(user => {

let urlsHtml = ""

if(user.urls && user.urls.length > 0){

user.urls.forEach(url => {

urlsHtml += `
<p><b>Short:</b> http://127.0.0.1:8000/${url.short}</p>
<p><b>Original:</b> ${url.original}</p>
<p><b>Clicks:</b> ${url.clicks}</p>
<hr>
`

})

}else{

urlsHtml = `<p>No URLs created</p>`

}

let disableButton = ""

if(user.role !== "admin"){

disableButton = `
<button class="delete-btn" onclick="disableUser(${user.id})">
Disable User
</button>
`

}

let div = document.createElement("div")

div.className = "user-card"

div.innerHTML = `
<h3>User: ${user.username}</h3>

<p><b>Role:</b> ${user.role}</p>
<p><b>Status:</b> ${user.is_active ? "Active" : "Disabled"}</p>
<p><b>URL Limit:</b> ${user.url_limit}</p>

<input id="limit-${user.id}" placeholder="Set new limit">

<div class="url-buttons">

<button onclick="setLimit(${user.id})">
Set Limit
</button>

${disableButton}

</div>

<h4>User URLs</h4>

${urlsHtml}
`

container.appendChild(div)

let line = document.createElement("hr")
line.className = "user-divider"

container.appendChild(line)

})

}

async function disableUser(id){

await fetch(API + "/admin/disable_user/" + id,{
method:"POST",
headers:{
"Authorization":"Bearer " + token
}
})

loadUsers()

}

async function setLimit(id){

let limit = document.getElementById("limit-"+id).value

await fetch(API + "/admin/set_limit/" + id + "?limit=" + limit,{
method:"POST",
headers:{
"Authorization":"Bearer " + token
}
})

loadUsers()

}

loadUsers()