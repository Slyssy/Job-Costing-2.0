let margin = {top: 70, right: 20, bottom: 70, left: 125};

let width = 1135 - margin.left - margin.right;
let height = 600 - margin.top - margin.bottom;

let path = d3.geo.path();

let svg = d3.select('#project-map').append('svg').attr({width:width, height:height});

d3.json9('cb_2018_us_state_500k.geojson', function(json){
    svg.selectAll('path')
    .data(json.features)
    .enter()
    .append('path')
    .attr('d', path)
    .attr('fill', '#666666')
});