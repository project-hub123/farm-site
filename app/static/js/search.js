// Поиск по странице
document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("search-input");
    const searchButton = document.getElementById("search-button");

    if (!searchInput || !searchButton) return;

    searchButton.addEventListener("click", function () {
        const text = searchInput.value.trim().toLowerCase();

        if (text.length < 2) {
            alert("Введите минимум 2 символа");
            return;
        }

        // Убираем старую подсветку
        removeHighlights();

        // Подсвечиваем новые совпадения
        highlight(document.body, text);
    });

});


// Подсветка найденного текста
function highlight(element, text) {

    if (element.children.length > 0) {
        for (let i = 0; i < element.childNodes.length; i++) {
            highlight(element.childNodes[i], text);
        }
    }

    if (element.nodeType === 3) {
        const index = element.data.toLowerCase().indexOf(text);
        if (index >= 0) {
            const span = document.createElement("span");
            span.className = "highlight";
            const matched = element.splitText(index);
            matched.splitText(text.length);
            const clone = matched.cloneNode(true);
            span.appendChild(clone);
            matched.parentNode.replaceChild(span, matched);
        }
    }
}


// Удаление подсветки
function removeHighlights() {
    const marks = document.querySelectorAll(".highlight");
    marks.forEach(mark => {
        const parent = mark.parentNode;
        parent.replaceChild(document.createTextNode(mark.textContent), mark);
        parent.normalize();
    });
}
