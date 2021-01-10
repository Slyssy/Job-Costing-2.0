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

const zoomG = svgMap.append('g');
const mapG = zoomG.append('g');
const circlesG = zoomG.append('g');
   
d3.json("https://gist.githubusercontent.com/mbostock/4090846/raw/d534aba169207548a8a3d670c9c2cc719ff05c47/us.json")
    .then(data => {
           // const counties = topojson.feature(data, data.objects.counties)

        // svgMap.selectAll('path').data(counties.features)
        // .enter().append('path')
        // .attr('class', 'county')
        // .attr('d', pathGenerator)       
    
        const states = topojson.feature(data, data.objects.states);          
       
        mapG.selectAll('path')
        .data(states.features)
        .enter().append('path')
        .attr('class', 'states')
        .attr('d', pathGenerator)
        // .append('title')
        // .text('State Name')      
});
// // Load in Cities Data
// d3.tsv('static/uscities.tsv')
//     .then(data => {
//         console.log(data)
//         circlesG.selectAll('circle').raise()
//             .data(data)
//             .enter().append('circle')
//             .attr('class', "cities")
//             .attr('r',  d => {
//                 return Math.sqrt(+d.population/ widthMap *0.005);
//             })
//             .attr('cx', d => {
//                 return projection([d.lng, d.lat])[0];
//             })
//             .attr('cy', d => {
//                 return projection([d.lng, d.lat])[1];
//             })
     
        
            
//     // Adding Tooltip Behavior

//     .on('mouseover', function(d)  {
//         d3.select(this).style('fill', '#a834eb')
//         d3.select("#name").text(" " + d.city)
//         d3.select("#population").text(valueFormat(" " + d.population))
//         d3.select("#latitude").text(" " + d.lat)
//         d3.select("#longitude").text(" " + d.lng)

//         //Position the tooltip <div> and set its content
//         let x = d3.event.pageX;
//         let y = d3.event.pageY - 40;

//         // //Populate city name in tooltip
//         // d3.select('#tooltip .name')
//         //     .text(d.city);

//         //Populate city population value into tooltip
//         // d3.select('#tooltip .value')
//         //     .text("population:" + valueFormat(d.population));
        
//         //Position tooltip and make it visible
//         d3.select('#tooltip')
//             .style('left', x +'px')
//             .style('top', y + 'px')
//             .style('opacity', 1)
//     })
//     .on('mouseout', function() {
//         d3.select(this).style('fill', '#eb2828');        
        
//         //Hide the tooltip
//         d3.select('#tooltip')
//             .style('opacity', '0');
//     });

//     //Creating pan and zoom feature
//     zoomG.call(d3.zoom().on("zoom", () => {
//         zoomG.attr("transform", d3.event.transform);
//     }))
            
// })

console.log(projectArray)
//Parsing and formatting data to be used for map points
const mapData = projectArray.map(({project_name, project_address, act_start_date, fin_act_revenue, fin_act_gross_profit, lat, lng}) => (
    {project_name, project_address, act_start_date, fin_act_revenue: parseFloat((fin_act_revenue).replace(/,/g, '')), fin_act_gross_profit: parseFloat((fin_act_gross_profit).replace(/,/g, '')), lat, lng}));


// Load in map point data
function map(mapData) {
    // d3.tsv('static/uscities.tsv')
    //     .then(data => {
            console.log(mapData)
            circlesG.selectAll('circle').raise()
                .data(mapData)
                .enter().append('circle')
                .attr('class', "cities")
                .attr('r',  d => {
                    return Math.sqrt(d.fin_act_revenue/ widthMap *0.05);
                })
                .attr('cx', d => {                   
                    return projection([d.lng, d.lat])[0];
                })
                .attr('cy', d => {
                    return projection([d.lng, d.lat])[1];
                })
         
            
                
        // Adding Tooltip Behavior
    
        .on('mouseover', function(d)  {
            d3.select(this).style('fill', '#a834eb')
            d3.select("#name").text(" " + d.project_name)
            d3.select("#address").text(" " + d.project_address)
            d3.select("#revenue").text( " $" + valueFormat(d.fin_act_revenue))
            d3.select("#grossProfit").text(" $" + valueFormat(d.fin_act_gross_profit))
    
            //Position the tooltip <div> and set its content
            let x = d3.event.pageX;
            let y = d3.event.pageY - 40;
    
            // //Populate city name in tooltip
            // d3.select('#tooltip .name')
            //     .text(d.city);
    
            //Populate city population value into tooltip
            // d3.select('#tooltip .value')
            //     .text("population:" + valueFormat(d.population));
            
            //Position tooltip and make it visible
            d3.select('#tooltip')
                .style('left', x +'px')
                .style('top', y + 'px')
                .style('opacity', 1)
        })
        .on('mouseout', function() {
            d3.select(this).style('fill', '#eb2828');        
            
            //Hide the tooltip
            d3.select('#tooltip')
                .style('opacity', '0');
        });
    
        //Creating pan and zoom feature
        zoomG.call(d3.zoom().on("zoom", () => {
            zoomG.attr("transform", d3.event.transform);
        }))
                
    }
    map(mapData)