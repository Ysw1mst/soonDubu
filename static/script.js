document.querySelector('input[type="file"]').addEventListener('change', function(event) {
    let fileName = event.target.files[0].name;
    alert('Selected file: ' + fileName);
});