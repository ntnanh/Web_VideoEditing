function Subtitle() {
  const handleChangeSubText = function () {
    const subText = $('.sub-text textarea');
    // Button click event to change the placeholder
    subText.on('click', function() {
      let originalPlaceholder = $(this).attr('placeholder');
      $(this).val(originalPlaceholder);
    });
    subText.on('change', function () {
      console.log($(this))
      let newSub = $(this).val();
      $(this).attr('placeholder', newSub)
    })
  }

  const handleChangeTime = function () {
    const subTime = $('.sub-time-start, .sub-time-end');
    // Button click event to change the placeholder
    subTime.on('click', function() {
      let originalPlaceholder = $(this).attr('placeholder');
      $(this).val(originalPlaceholder);
    });

    subTime.on('change', function () {
      let newSub = $(this).val();
      $(this).attr('placeholder', newSub)
    })
  }

  const getSubtitles = function () {
    let subtitles = [];
    $('.sidebar-subs').each(function (i) {
      subtitles.push({
        'start_time': $(this).find('.sub-time-start').attr('placeholder'),
        'end_time': $(this).find('.sub-time-end').attr('placeholder'),
        'text': $(this).find('.sub-text textarea').attr('placeholder'),
      })
    })

    return subtitles;
  }

  const activeButtonDeleteSub = function () {
    $(".sub-card").on({
      mouseenter: function () {
        $(this).find('.sub-buttons').removeClass('d-none')
      },
      mouseleave: function () {
        $(this).find('.sub-buttons').addClass('d-none')
      }
    });
  }

  const handleActiveSub = function () {
    $('.btn-add-section').on('click', function () {
      const subClone = $('.sidebar-subs:last').clone();
      subClone.find('.sub-time-start').attr('placeholder','00:00.00')
      subClone.find('.sub-time-end').attr('placeholder','00:00.00')
      subClone.find('.sub-text textarea').attr('placeholder','')
      $(this).before(subClone);
      handleChangeSubText();
      handleChangeTime();
      activeButtonDeleteSub();
      delSub();
    })
  }

  const delSub = function () {
    $(".sub-del").on('click', function () {
      $(this).closest('.sidebar-subs').remove();
    })
  };

  const init = function () {
    handleChangeSubText();
    handleChangeTime();
    handleActiveSub();
  }

  return {
    init,
    getSubtitles
  }
}

$(function() {
  const subtitle = new Subtitle();
  subtitle.init();
});