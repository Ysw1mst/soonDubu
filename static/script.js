function showFileName(input) {
    if (input.files && input.files[0]) {
        const fileName = input.files[0].name;
        const display = document.querySelector('.uploaded-file-name');
        display.textContent = fileName;
    }
}