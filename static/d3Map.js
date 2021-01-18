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
const cityG = zoomG.append('g');
const projectG = zoomG.append('g');

let inputValue = null;
const month = ["January","February","March","April","May","June","July","August","September","October","November","December"];
const year= ["2020", "2021", "2022", "2023", "2024"] 
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
// Load in Cities Data
d3.tsv('static/uscities.tsv')
    .then(data => {
        // console.log(data)
        cityG.selectAll('circle').raise()
            .data(data)
            .enter().append('circle')
            .attr('class', "cities")
            .attr('r',  '1')
            .attr('cx', d => {
                return projection([d.lng, d.lat])[0];
            })
            .attr('cy', d => {
                return projection([d.lng, d.lat])[1];
            })
     
// Adding names to cities
            cityG.selectAll("text")
                .data(data)
                .enter()
                .append("text") // append text
                .attr('class', 'cityName')
                 .attr("x", function(d) {
                 return projection([d.lng, d.lat])[0];
                })
                .attr("y", function(d) {
                return projection([d.lng, d.lat])[1];
                })
                .attr("dy", 6) // set y position of bottom of text
                .attr("text-anchor", "end") // set anchor y justification
                .text(function(d) {return d.city;}); // define the text to display                         
})
// console.log(projectArray)

//Parsing and formatting data to be used for map points
const mapData = projectArray.map(({project_name, project_address, act_start_date, fin_act_revenue, fin_act_gross_profit, lat, lng,}) => (
    {project_name, project_address, act_start_date, fin_act_revenue: parseFloat((fin_act_revenue).replace(/,/g, '')), fin_act_gross_profit: parseFloat((fin_act_gross_profit).replace(/,/g, '')), lat: lat.toString(), lng: lng.toString()}));
    // console.log(mapData)

const mapper1 = single => {
    let d = single.act_start_date.split('-');
    let gp = Number(single.fin_act_gross_profit);
    let rev = Number(single.fin_act_revenue);
    let lt = single.lat;
    let lg = single.lng;
    let pn = single.project_name;
    let pa = single.project_address
    return { project_name: pn, project_address: pa, year: d[0], month: d[1], day: d[2], fin_act_gross_profit: gp , fin_act_revenue: rev, lat: lt, lng: lg};
}

const mapData0 = mapData.map(mapper1)

const mapData1 = mapData0.map(
    o => ({...o, month: month[o.month - 1]})
    );   
    console.log(mapData1)

// Grabbing years and pulling unique years to create a variable that will be used to populate the dropdown selector.
const mapYears = mapData1.map(a => a.year);
const selectYears = mapYears.filter((value, index, self) => self.indexOf(value) === index)
selectYears.sort(function(a, b){return b - a});
console.log(selectYears)

// Load in map point data
function map(mapData) {

//Map slider update function
d3.select("#timeslide").on("input", function() {
    update(+this.value);
    // console.log(+this.value);
});

// update the fill of each circle of class "projects" with value
function update(value) {
    document.getElementById("range").innerHTML=month[value];
    inputValue = month[value];
    d3.selectAll(".projects")
        .attr("fill", dateMatch);
}

// Date Match function used to determine the color of the circles based on whether or not selector selection
// matches month in actual start date
function dateMatch(mapData1, value) {
    let m = mapData1.month;

    if (inputValue == m) {
        this.parentElement.appendChild(this);
        return "#eb2828";
    } else {
        return "#636769";
    };
}

// Establish initial date view on map. Set for January.
function initialDate(mapData1, i){
    let m = mapData1.month;
  
    if (m == "January") {
        this.parentElement.appendChild(this);
        return "#eb2828";
    } else {
        return "#636769";
    };
}

//Appending option to html id-mapYear and adding selectYears to the dropdown
const mapOptions = d3.select("#mapYear").selectAll("option")
          .data(selectYears)
      .enter().append("option")
          .text(d => d)


mapUpdate(d3.select("#mapYear").property("value"), 0)
    
function mapUpdate(year, speed) {    
    var dataf1 = mapData1.filter(f => f.year == year)
    console.log(dataf1)

    projectG.selectAll('.projects').transition().duration(speed)
    // .call(project_circles)

    var projects = projectG.selectAll(".projects")
    // .data(dataf1, d => d.lng, d.lat)
    
    //Function to plot points
        projectG.selectAll('.projects').remove();
        console.log(mapData1)
        projectG.selectAll('circle').raise()
        .data(dataf1)
        .enter().append('circle')
        .attr('class', "projects")
        .attr('fill', initialDate)
        // .attr('fill', '#eb2828')
        .attr('r',  d => {
            return Math.sqrt(d.fin_act_revenue/ widthMap *0.1);
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
        d3.select("#startDate").text(" " + d.month + " " + d.day + ", " + d.year)

        //Position the tooltip <div> and set its content
        let x = d3.event.pageX;
        let y = d3.event.pageY - 40;
        
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
    map.update = mapUpdate
}
    map(mapData1)

var mapSelect = d3.select("#mapYear")
// .style("border-radius", "5px")
.on("change", function() {
map.update(this.value, 750)
})


