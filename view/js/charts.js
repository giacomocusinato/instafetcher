// List of image coordinate
var coordinatesList;

// Load google Visualizazion API and the geochart package
google.load('visualization', '1', {'packages': ['geochart']});
// Set a callback to run whan Visualization API are loaded
google.setOnLoadCallback(fetchImages);

/**
 * Fetches the coordinate list from Google Endpoints API
 */
function fetchImages() {
    $.ajax({
        url: 'https://instafetcher.appspot.com/_ah/api/instafetcher/v1/coordinates',
        type: 'GET',
        dataType: 'JSON',
        contentType: 'application/json',
        success: function(data) {
            // Initialize the coordinateList var for future chart re-draws
            coordinatesList = data;

            generateMapGraph();
        },
        error: function(xhr, ajaxOptions, thrownError) {
            console.error("Call list error: " + xhr.status);
        }
    });
}

/**
 * Callback that creates a DataTable,
 * istantiates the GeoChart and
 * draws the chart with the provided data
 */
function generateMapGraph() {
    var gdata = new google.visualization.DataTable();
    gdata.addColumn('number', 'Latitude');
    gdata.addColumn('number', 'Longitude');

    coordinatesList.items.forEach(function(coordinate) {
        gdata.addRow([coordinate.lat, coordinate.lon]);
    });

    var options = {
        displayMode: 'markers',
        colorAxis: {colors: ['green']}
    };

    var chart = new google.visualization.
        GeoChart(document.getElementById('map-chart'));
    chart.draw(gdata, options);
}

/**
 * Callback for the window resize event.
 * Google charts needs to be re-draw in
 * order to adapt to the screen-size
 */
function resizeHandler() {
    //$('#map-container').css('height', '30px');
    generateMapGraph();
}
if (window.addEventListener) {
    window.addEventListener('resize', resizeHandler, false);
}
else if (window.attachEvent) {
    window.attachEvent('onresize', resizeHandler);
}