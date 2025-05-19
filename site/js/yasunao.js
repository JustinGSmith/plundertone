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

// The API calls this function when the player's state changes.
// The function indicates that when playing a video (state=1),
// the player should play for six seconds and then stop.

function state_change(event, thunk) {
    console.log("state change")
    if (event.data == YT.PlayerState.PLAYING) {
      console.log("queueing thunk from state_change.state_watch")
      setTimeout(thunk, 1000);
    } else {
      console.log("waiting on state", event.data)
    }
}

function stopVideo() {
  player.stopVideo();
}

function stutter(step, limit, skip, skip_rate) {
  console.log("defining stutter_thunk")
  thunk = () => {
    console.log("running stutter_thunk")
    if(step < limit) {
      console.log("stutter", step, limit, skip, skip_rate)
      destination = (limit - step) * skip
      player.seekTo(destination)
    }
    setTimeout(() => stutter(step++, limit, skip, skip_rate), skip_rate)
  }
  if(player.getPlayerState() == YT.PlayerState.PLAYING) {
    console.log("invoking stutter_thunk")
    thunk()
    } else {
      console.log("queueing stutter_thunk")
      // TODO - try making onPlayerStateChange an object with a continue method
      // to call
      window.onPlayerStateChange = (event) => state_change(event, thunk);
      player.playVideo()
  }
}

function main() {
  ready = true
  window.onPlayerStateChange = (event) => {
    if (ready && event.data == YT.PlayerState.PLAYING) {
      ready = false
      state_change(event, (event) => stutter(0, 1000, 1000, 1000))
    }
  }
}

main()
