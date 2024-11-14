document.addEventListener("DOMContentLoaded", function() {
    // HTML 요소가 로드된 후에 실행되는 코드
    const uploadButton = document.querySelector(".upload-button");
    const fileInput = document.querySelector("#fileInput");
    const downloadButton = document.querySelector(".download-button");

    if (uploadButton) {
        uploadButton.addEventListener("click", function() {
            console.log("Upload button clicked");
            // 파일 선택이 완료되면 폼을 제출하도록 자동으로 처리
            fileInput.click(); // file input을 강제로 클릭
        });
    }

    if (fileInput) {
        fileInput.addEventListener("change", function() {
            console.log("File selected:", fileInput.files[0].name);
            // 파일 선택 후 자동으로 폼을 제출
            document.getElementById("uploadForm").submit();
        });
    }

    if (downloadButton) {
        downloadButton.addEventListener("click", function() {
            console.log("Download button clicked");
            // 다운로드 버튼 클릭 시 서버에서 파일을 받아서 다운로드하는 로직을 추가할 수 있습니다.
        });
    }
});