$(document).ready(function () {
/****************************************************/
    /* js for image.html */
    $('#hidden-div').hide();
    var image_result = document.getElementById("result");
    image_result.onload = function (e) {
        $('#hidden-div').show();
        document.getElementById("loading-badge").innerHTML = "Reconstructing..."
    };
});