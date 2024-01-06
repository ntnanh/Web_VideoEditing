function Upload(){

    const handleUploadCutVideo = function () {
        $('#upload-file').on('change', function () {
            $('#formUpload').submit();
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