const ol_users_list = document.getElementById("ol_users_list");

async function get_data() {
    const response = await fetch ("/get_data", {
            method: "GET",
        });
    
    const answer = await response.json()

    return answer;
}

async function show_data() {
    users_list = await get_data();
    console.log(users_list);

    for (let i = 0; i < users_list["users"].length; i++) {
        const username = users_list["users"][i]["username"]
        const email = users_list["users"][i]["email"]
        console.log(username)

        const li_element = document.createElement("li");
        li_element.textContent = `${username} ${email}`;
        ol_users_list.appendChild(li_element);
    }
}

document.addEventListener("DOMContentLoaded", show_data);