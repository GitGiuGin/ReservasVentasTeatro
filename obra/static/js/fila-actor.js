function toggleRowHighlight(id) {
    // Obtener el checkbox y la fila correspondiente
    const checkbox = document.getElementById(`chkActor-${id}`);
    const row = document.getElementById(`fila-${id}`);
    
    // Si el checkbox está seleccionado, agregar la clase para resaltar la fila
    if (checkbox.checked) {
        row.classList.add("table-active");
    } else {
        // Si no está seleccionado, quitar la clase
        row.classList.remove("table-active");
    }
}