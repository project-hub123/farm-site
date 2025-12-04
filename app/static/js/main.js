// Переключение режима для слабовидящих
function toggleLowVision() {
    const current = localStorage.getItem("lowvision");

    if (current === "on") {
        localStorage.setItem("lowvision", "off");
    } else {
        localStorage.setItem("lowvision", "on");
    }

    location.reload();
}

// Устанавливаем режим при загрузке страницы
document.addEventListener("DOMContentLoaded", function () {
    if (localStorage.getItem("lowvision") === "on") {
        document.body.classList.add("lowvision");
    }
});

// Плавный скролл к секциям (если есть ссылки с href="#...")
document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener("click", function (e) {
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: "smooth" });
        }
    });
});

// Простая функция уведомления
function showMessage(text) {
    const block = document.createElement("div");
    block.className = "notify";
    block.innerText = text;

    document.body.appendChild(block);

    setTimeout(() => {
        block.style.opacity = "0";
    }, 2000);

    setTimeout(() => {
        block.remove();
    }, 3000);
}

// Пример вызова уведомления:
// showMessage("Сообщение отправлено!");
