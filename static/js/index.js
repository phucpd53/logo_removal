$(document).ready(function () {
    /* js for index.html */
    /****************************************************/
    // Init
    $('.img-preview').hide();
    $('#btn-run').hide();
    
    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.img-preview').show();
        $('#btn-run').show();
        readURL(this);
    });
    
});