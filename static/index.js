// Configure a few settings and attach camera
Webcam.set({
    width: 320, height: 240, image_format: 'jpeg', jpeg_quality: 90
});

Webcam.attach('#my_camera');

// preload shutter audio clip
var shutter = new Audio();
shutter.autoplay = true;
shutter.src = navigator.userAgent.match(/Firefox/) ? 'shutter.ogg' : 'shutter.mp3';

function take_snapshot() {
    // play sound effect
    shutter.play();

    // take snapshot and get image data
    Webcam.snap(function (data_uri) {
        // display results in page
        document.getElementById('results').innerHTML = '<img src="' + data_uri + '"/>';

        Webcam.upload( data_uri, 'images', function(code, text) {
			// Upload complete!
			// 'code' will be the HTTP response code from the server, e.g. 200
			// 'text' will be the raw response content
		} );
    });
}
