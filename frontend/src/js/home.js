const registration_form = document.getElementById("registration_form");
const username = document.getElementById("username");
const email = document.getElementById("email");
const password = document.getElementById("password");
const confirm_password = document.getElementById("confirm_password");

async function log_data() {
    console.log(`username: ${username.value}\n` +
                `email: ${email.value}\n` +
                `password: ${password.value}\n` +
                `confirm_password: ${confirm_password.value}`);
};

async function send_data(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы
    
    await log_data();

    if (password.value !== confirm_password.value) {
        console.error("Пароли не совпадают!");

        const messageDiv = document.getElementById("message");
        messageDiv.textContent = "Пароли не совпадают";
        messageDiv.style.color = "red";
        return;
    }
    
    const data = {
        username: username.value,
        email: email.value, 
        password: password.value, 
    };
    
    try {
        const response = await fetch("/send_data", {  // Убрали полный URL
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // Успешная регистрация
            window.location.href = "/pages/registration_successful.html";
        } else {
            // Обработка ошибок сервера
            showMessage("Ошибка при регистрации", "red");
        }
    } catch (error) {
        console.error("Ошибка при отправке данных:", error);
        showMessage("Ошибка соединения с сервером", "red");
    }
};

registration_form.addEventListener("submit", send_data);