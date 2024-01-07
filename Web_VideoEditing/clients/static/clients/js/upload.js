function Upload(){

    const handleUploadCutVideo = function () {
        $('#upload-file').on('change', function () {
            const fileInput = $('#upload-file');
            const selectedFile = fileInput[0].files[0];

            if (selectedFile) {
                if (selectedFile.type === 'video/mp4') {
                    $('#formUpload').submit();
                } else {
                    // Notify the user that the selected file is not an .mp4 file
                    alert('Please select a .mp4 file.');
                }
            } else {
                // Notify the user to select a file
                alert('Please select a file.');
            }
        })
    }

    const init = function () {
        handleUploadCutVideo();
    }
    return {
        init
    }
}
$(function () {
    const upload = new Upload
    upload.init()
})