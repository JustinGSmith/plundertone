// This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";

var firstScriptTag = document.getElementsByTagName('script')[0];

firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// This function creates an <iframe> (and YouTube player)
// after the API code downloads.
var player;
function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
    height: '390',
    width: '640',
    videoId: 'M7lc1UVf-VE',
    playerVars: {
      'playsinline': 1
    },
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
}

// The API will call this function when the video player is ready.
function onPlayerReady(event) {
  event.target.playVideo();
}

var stutter_points = [
  8000,
  8125,
  8250,
  8375,
  8500,
  8750,
  9000,
  9250,
  9500,
  9250,
  9500,
  10000
]

function stutter() {
  if(player.getPlayerState() == YT.PlayerState.PLAYING) {
    player.seekTo(stutter_points.peek())
    setTimeout(stutter, 1000)
  } else {
    window.onPlayerStateChange = stutter
    player.playVideo()
  }
}

function main() {
  ready = true
  window.onPlayerStateChange = (event) => {
    if (ready && event.data == YT.PlayerState.PLAYING) {
      ready = false
      stutter
    }
  }
}

main()
