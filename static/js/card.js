document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll('.card');
    let maxHeight = 0;

    // Encuentra la altura máxima
    cards.forEach(card => {
        const cardHeight = card.offsetHeight;
        if (cardHeight > maxHeight) {
            maxHeight = cardHeight;
        }
    });

    // Ajusta todas las tarjetas a la altura máxima
    cards.forEach(card => {
        card.style.height = `${maxHeight}px`;
    });
});