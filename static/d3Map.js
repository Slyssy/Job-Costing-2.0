// const { select } = require("d3");

const marginMap = {top: 0, right: 0, bottom: 0, left: 0};
const widthMap = 1135 - marginMap.left - marginMap.right;
const heightMap = 600 - marginMap.top - marginMap.bottom;

const valueFormat = d3.format(',');

const svgMap = d3.select('#project-map')
    .append('svg')
    .attr('height', heightMap + marginMap.top + marginMap.bottom)
    .attr('width', widthMap + marginMap.left + marginMap.right)
    .append('g')
    .attr("transform", "translate(" + marginMap.left + ", " + marginMap.top + ")");

const projection = d3.geoAlbersUsa();
const pathGenerator = d3.geoPath().projection(projection);

const g = svgMap.append('g');

g.call(d3.zoom().on("zoom", () => {
    g.attr("transform", d3.event.transform);
}))

// Load Multiple Datasets
// Promise.all([
    
d3.json("https://gist.githubusercontent.com/mbostock/4090846/raw/d534aba169207548a8a3d670c9c2cc719ff05c47/us.json")
    .then(data => {
           // const counties = topojson.feature(data, data.objects.counties)

        // svgMap.selectAll('path').data(counties.features)
        // .enter().append('path')
        // .attr('class', 'county')
        // .attr('d', pathGenerator)       
    
        const states = topojson.feature(data, data.objects.states);          
       
        g.selectAll('path').data(states.features)
        .enter().append('path')
        .attr('class', 'states')
        .attr('d', pathGenerator)
        .append('title')
        .text('State Name')      
});

// Load in Cities Data
d3.tsv('static/uscities.tsv')
    .then(data => {
        console.log(data)
        g.selectAll('path').data(data)
            .enter().append('circle')
            .attr('class', "cities")
            .attr('r',  d => {
                return Math.sqrt(+d.population/ widthMap *0.005);
            })
            .attr('cx', d => {
                return projection([d.lng, d.lat])[0];
            })
            .attr('cy', d => {
                return projection([d.lng, d.lat])[1];
            })
            

    .on('mouseover', d => {
        // d3.select(this)
        // .style('fill', 'yellow')

        //Position the tooltip <div> and set its content
        let x = d3.event.pageX;
        let y = d3.event.pageY - 40;

        //Populate name in tooltip
        d3.select('#tooltip .name')
            .text(d.city);

        //Populate population value into tooltip
        d3.select('#tooltip .value')
            .text("population:" + valueFormat(d.population));
        
        //Position tooltip and make it visible
        d3.select('#tooltip')
            .style('left', x +'px')
            .style('top', y + 'px')
            .style('opacity', 1)
    })
    .on('mouseout', function() {
        // d3.select(this)
        // .style('fill', '#ecb133');
        
        //Hide the tooltip
        d3.select('tooltip')
            .style('opacity', '#0');
    });
            
})


    

