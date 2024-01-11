function Common() {
  const handleButtonPlay = function (event) {
    $(".btn-play").on("click", function() {
      const video = $(".video-upload")[0];
      const button = $(this);
      const icon = button.find("i");
      video.muted = false;
      if (video.paused) {
        video.play();
        icon.removeClass("fa-play").addClass("fa-pause");
      } else {
        video.pause();
        icon.removeClass("fa-pause").addClass("fa-play");
      }
    });
  }

  const handleButtonMute = function (event) {
    $(".btn-mute").on("click", function() {
      const video = $(".video-upload")[0];
      const button = $(this);
      const icon = button.find("i");
      if (video.muted) {
        video.muted = false;
        icon.removeClass("fa-volume-mute").addClass("fa-volume-up");
      } else {
        video.muted = true;
        icon.removeClass("a-volume-up").addClass("fa-volume-mute");
      }
    });
  }

  const handleDurationVideo = function () {
    const video = document.querySelector('.video-upload');
    const startInput = $('.start_time');
    const endInput = $('.end_time');
    const outputInput = $('.video-duration');
    const videoTimeTotal = $('.video-time-total');
    const videoTimeCurrent = $('.video-time-current');
    outputInput.text(formatTime(video.duration));
    videoTimeTotal.text(formatTime(video.duration));
    video.addEventListener('play', () => {
      startInput.val(formatTime(video.currentTime));
    });

    video.addEventListener('timeupdate', function() {
      videoTimeCurrent.text(formatTime(video.currentTime));
    });

    video.addEventListener('pause', () => {
      endInput.val(formatTime(video.currentTime));
    });

    video.addEventListener('loadedmetadata', function() {
      videoTimeTotal.text(formatTime(video.duration));
      outputInput.text(formatTime(video.duration));
    });
  }

  const handleButtonExport = function () {
    $('.btn-export').on('click', function (){
      let preview_video = $('#video-preview');
      let url = preview_video.find('source').attr('src');
      let id = $('#id').val();
      if (url) {
        let params = {
          'id': id,
          'url': url
        }
        $.ajax({
          url: '/export_video',
          type: 'POST',
          beforeSend: function() {
            $.LoadingOverlay("show");
          },
          headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
          data: params
        }).done(function(res) {
          if (res.success === 'true') {
            let anchor = $("<a>")
                .attr("href", url)
                .attr("download", "downloaded_video.mp4") // Change the downloaded file name here
                .appendTo("body");
            anchor[0].click();
            anchor.remove();
            $.LoadingOverlay("hide");
          }
        }).error(function (e) {
          console.log(e)
          $.LoadingOverlay("hide");
        });
      }else {
        alert('Please enter preview before export');
      }
    })
  }

  const formatTime = function (time) {
    const hours = Math.floor(time / 3600);
    const minutes = Math.floor((time % 3600) / 60);
    const seconds = Math.floor(time % 60);
    return `${padZero(hours)}:${padZero(minutes)}:${padZero(seconds)}`;
  }

  const padZero = function (number) {
    return number < 10 ? `0${number}` : number;
  }

  const back = function () {
    $('.btn-back').on('click', function () {
      window.history.back();
    });
  }

  const init = function () {
    handleButtonPlay();
    handleButtonMute();
    handleDurationVideo();
    handleButtonExport();
    back();
  }

  return {
    init
  }
}

$(function () {
  const common = new Common();
  common.init();
})