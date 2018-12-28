     // GET USER MEDIA CODE

          navigator.getUserMedia = ( navigator.getUserMedia ||
                             navigator.webkitGetUserMedia ||
                             navigator.mozGetUserMedia ||
                             navigator.msGetUserMedia);
      var video;
      var webcamStream;

      function startWebcam() {
        if (navigator.getUserMedia) {
           navigator.getUserMedia (
              // constraints
              {
                 video: true,
                 audio: false
              },

              // successCallback

              function(localMediaStream) {
                  video = document.querySelector('video');
                 video.src = window.URL.createObjectURL(localMediaStream);
                 webcamStream = localMediaStream;
              },

              // errorCallback

              function(err) {
                 console.log("The following error occured: " + err);
              }
           );
        } else {
           console.log("getUserMedia not supported");
        }
		document.getElementById("snap").disabled = false;
      }


      //---------------------

      // TAKE A SNAPSHOT CODE

      //---------------------

      var canvas, ctx, fullQuality;


      function init() {
        // Get the canvas and obtain a context for
        // drawing in it
        canvas = document.getElementById("myCanvas");
        ctx = canvas.getContext('2d');
        ctx.toDataURL('image/jpeg', 1.0);
      }


      function snapshot() {
         // Draws current image from the video element into the canvas

        ctx.drawImage(video, 0,0, canvas.width, canvas.height);
        image_data = canvas . toDataURL ( 'image/jpeg');
        document . getElementById ( 'mytext') . value = image_data;
        $button = document.getElementById('form_button');
        $button.hidden = false;
      }
