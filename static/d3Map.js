// const { select } = require("d3");

const marginMap = {top: 70, right: 20, bottom: 70, left: 125};

const widthMap = 1135 - marginMap.left - marginMap.right;
const heightMap = 600 - marginMap.top - marginMap.bottom;

const svgMap = d3.select('#project-map')
// let path = d3.geoPath();

// d3.select('#project-map').append('svg').attr({width:width, height:height});

// d3.json('us_map.json', function(json){
//     svg.selectAll('path')
//     .data(json.features)
//     .enter()
//     .append('path')
//     .attr('d', path)
//     .attr('fill', '#666666')
// });

// let url = "https://gist.githubusercontent.com/mbostock/4090846/raw/d534aba169207548a8a3d670c9c2cc719ff05c47/us.json"
const projection = d3.geoMercator();
const pathGenerator = d3.geoPath().projection(projection);

d3.json("https://gist.githubusercontent.com/mbostock/4090846/raw/d534aba169207548a8a3d670c9c2cc719ff05c47/us.json")
    .then(data => {
        const states = topojson.feature(data, data.objects.states);
        console.log(data);
        console.log(states)

        const paths = svgMap.selectAll('path')
            .data(states.geometries);
        paths.enter().append('path')
            .attr('d', d => pathGenerator(d));
    })