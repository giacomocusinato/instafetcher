/* API page counter */
var pageCounter = 0;

$(document).ready(function() {
    // Fetch the 'first-page' images
    // pageCounter is 0
    fetchImages(pageCounter);

    // Register to the "Load more" button event
    $('#load-more-btn').click(function() {
      fetchImages(pageCounter);
    });
})


/**
 * Fetches the images data from the Google Endpoints API.
 * @param api_page
 */
    function fetchImages(page) {
        $.ajax({
            url: 'https://instafetcher.appspot.com/_ah/api/instafetcher/v1/images/' + page,
            type: 'GET',
            dataType: 'JSON',
            contentType: 'application/json',
            success: function(data) {
                listImages(data);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.error("Call list error: " + xhr.status);
            }
        })
    }

/**
 * Parse the image list as JSON and programmatically add the data
 * retrieved to the html list.
 * @param data
 */
function listImages(data) {
    data.items.forEach(function(img) {
        var li = [
        '<li class="col-lg-3 col-sm-4 col-xs-12">',
        '  <a href="{0}" data-lightbox="image">',
        '    <div class="thumbnail">',
        '      <img class="img-responsive" src="{0}" />',
        '    </div>',
        '  </a>',
        '</li>'
        ].join('').format(img.url);

        $("#images").append(li);
    });
    pageCounter++;
}
