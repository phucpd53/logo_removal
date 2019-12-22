$(document).ready(function () {
/****************************************************/
    /* js for image.html */
    $('#hidden-div').hide();
    $('.loader').hide();
    var image_result = document.getElementById("result");
    image_result.onload = function (e) {
        $('#hidden-div').show();
        document.getElementById("loading-badge").innerHTML = "Reconstructing..."
    };
    $('#stop-button').click(function(){
        $('.loader').show()
        $.ajax({
            type: 'POST',
            url: '/force_stop',
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result 
                $('.loader').hide();
                document.getElementById('loading-badge').innerHTML = 'Stopped!' 
            },
        });
        document.getElementById('result').src = '';
        $('#hidden-div').hide();
        document.getElementById('loading-badge').innerHTML = 'Stopping' 
    });
});
