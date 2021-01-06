// const { select } = require("d3");

const marginMap = {top: 0, right: 0, bottom: 0, left: 0};
const widthMap = 1135 - marginMap.left - marginMap.right;
const heightMap = 600 - marginMap.top - marginMap.bottom;

const svgMap = d3.select('#project-map')
    .append('svg')
    .attr('height', heightMap + marginMap.top + marginMap.bottom)
    .attr('width', widthMap + marginMap.left + marginMap.right)
    .append('g')
    .attr("transform", "translate(" + marginMap.left + ", " + marginMap.top + ")");

const projection = d3.geoAlbersUsa();
const pathGenerator = d3.geoPath().projection(projection);

const g = svgMap.append('g');

svgMap.call(d3.zoom().on("zoom", () => {
    g.attr("transform", d3.event.transform);
}))

d3.json("https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json")
    .then(data => {
        const states = topojson.feature(data, data.objects.states);
        // console.log(data);
        // console.log(states);
        g.selectAll('path').data(states.features)
        .enter().append('path')
        .attr('class', 'state')
        .attr('d', pathGenerator)
        .append('title')
        .text('State Name')

        // const paths = g.selectAll('path')
        //     .data(states.features);

        // paths.enter().append('path')
        //     .attr('class', 'state')
        //     .attr('d', d => pathGenerator(d))
        //     .append('title')
        //         .text('Hello');
            
    })

    

    

