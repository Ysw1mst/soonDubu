document.addEventListener("DOMContentLoaded", function() {
    // HTML 요소가 로드된 후에 실행되는 코드
    const uploadButton = document.querySelector(".upload-button");
    const downloadButton = document.querySelector(".download-button");

    if (uploadButton) {
        uploadButton.addEventListener("click", function() {
            console.log("Upload button clicked");
        });
    }

    if (downloadButton) {
        downloadButton.addEventListener("click", function() {
            console.log("Download button clicked");
            // 다운로드 버튼 클릭 시 서버에서 파일을 받아서 다운로드 하는 로직을 추가할 수 있습니다.
        });
    }
});