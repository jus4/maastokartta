function showNotice(notice) {
  const noticeContainer = document.getElementById("notice-container")
  const noticeText= document.getElementById("notice-text")
  noticeText.innerText = notice
  noticeContainer.classList.remove("hidden")
  setTimeout(function(){
    noticeContainer.classList.add("hidden")
  }, 3000)
}

// DOM loaded
window.addEventListener('load', function () {

  document.body.addEventListener('htmx:responseError', function(event) {
    const errorBox = document.getElementById('error-notice');
    errorBox.classList.remove('hidden')
    const errorTextContent = errorBox.querySelector('.error-text')

    // Try to extract error message from response body (if provided)
    const response = event.detail.xhr;
    errorTextContent.textContent = response.responseText || "Failed to parse location";
    setTimeout(function(){
      errorBox.classList.add("hidden")
    }, 5000)
  });

  // Map link generation
  const mapLinkButton = document.getElementById("copy-map-link")
  const openMapLink = document.getElementById("open-map-link")
  if ( mapLinkButton ) {
    mapLinkButton.addEventListener("click", function(){
      const mapLink = document.getElementById("result-input")
      navigator.clipboard.writeText(mapLink.value);
      showNotice("Maastokartta link copied to clipboard")
    })
  }

  if (openMapLink) {
    openMapLink.addEventListener("click", function() {
      const mapLink = document.getElementById("result-input")
      window.open(mapLink.value)
    })
  }

  // Toggle google short url | lat long
  const showGLShortUrl = document.querySelector('input[name="use-google-short-url"]')
  const glLink = document.getElementById("gmap-short-url")
  const coordinatesLatLong = document.getElementById("coordinates-latitude-longitude")
  if ( showGLShortUrl && glLink && coordinatesLatLong ) {
    showGLShortUrl.addEventListener("input", function() {
      if ( this.checked ) {
        coordinatesLatLong.classList.add("hidden")
        glLink.classList.remove("hidden")
      } else {
        coordinatesLatLong.classList.remove("hidden")
        glLink.classList.add("hidden")
      }
    })
  }

})

