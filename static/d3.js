// load the data
projectArray = Object.keys(project_list).map((i) => project_list[i]);
// console.log(projectArray)

// Filtering data to be used for plot
const chartData = projectArray.map(({act_start_date, fin_est_labor_expense, fin_act_labor_expense}) => ({act_start_date, fin_est_labor_expense: parseFloat((fin_est_labor_expense).replace(/,/g, '')), fin_act_labor_expense: parseFloat((fin_act_labor_expense).replace(/,/g, ''))}));
// console.log(chartData)

// Grouping dates into months and summing estimated and actual labor expense by month
const mapper = single => {
  let d = single.act_start_date.split('-');
  let e = Number(single.fin_est_labor_expense);
  let a = Number(single.fin_act_labor_expense);
  return { year: d[0], month: d[1], fin_est_labor_expense: e , fin_act_labor_expense: a};
}
 
const reducer = (group, current) => {
  let i = group.findIndex(single => (single.year == current.year && single.month == current.month));
  if (i == -1) {
    return [ ...group, current ];
  }

  group[i].fin_est_labor_expense += current.fin_est_labor_expense;
  group[i].fin_act_labor_expense += current.fin_act_labor_expense
  return group;
};

const sumPerMonth = chartData.map(mapper).reduce(reducer, []);
// console.log(sumPerMonth);

// Sorting data by month
const data0 = sumPerMonth.sort((a,b) => a.month - b.month)
// console.log(data0)

// Changing month number to month name
const months = ["Jan", "Feb","Mar", "Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

const data = data0.map(
  o => ({...o, month: months[o.month - 1]})
);
console.log(data)

function chart(data) {
  // Looping through data to pull the Unique years in the data set.
const years = data.map(a => a.year)
.filter((value, index, self) => self.indexOf(value) === index)
years.sort(function(a, b){return b - a});
// console.log(years)

const options = d3.select("#year").selectAll("option")
          .data(years)
      .enter().append("option")
          .text(d => d)

var svg = d3.select("#estimate-to-actual"),
margin = {top: 70, right: 20, bottom: 70, left: 125},
width = +svg.attr("width") - margin.left - margin.right,
height = +svg.attr("height") - margin.top - margin.bottom;

// Setting x Scale
const x = d3.scaleBand()
.range([margin.left, width - margin.right])
.padding(0.1)
.paddingOuter(0.2);

var y = d3.scaleLinear()
.range([height - margin.bottom, margin.top])

var xAxis = g => g
.attr("transform", "translate(0," + (height - margin.bottom) + ")")
.call(d3.axisBottom(x).tickSizeOuter(0))

var yAxis = g => g
.attr("transform", "translate(" + margin.left + ",0)")
.call(d3.axisLeft(y).tickSize(-width))

svg.append("g")
.attr("class", "x-axis")

svg.append("g")
.attr("class", "y-axis")


update(d3.select("#year").property("value"), 0)

function update(year, speed) {

var dataf = data.filter(f => f.year == year)

y.domain([0, d3.max(data, d => d.fin_est_labor_expense)]).nice()

svg.selectAll(".y-axis").transition().duration(speed)
    .call(yAxis);

x.domain(data.map(d => d.month))

svg.selectAll(".x-axis").transition().duration(speed)
    .call(xAxis)

var bar = svg.selectAll(".bar")
    .data(dataf, d => d.month)

bar.exit().remove();

bar.enter().append("rect")
    .attr("class", "bar")
    .style("fill", d => d.fin_act_labor_expense < d.fin_est_labor_expense ? '#1b71f2': '#eb2828')
    .attr("opacity", ".5")
    .attr("width", x.bandwidth())
    .merge(bar)
.transition().duration(speed)
    .attr("x", d => x(d.month))
    .attr("y", d => y(d.fin_act_labor_expense))
    .attr("height", d => y(0) - y(d.fin_act_labor_expense))

  // Defining limit lines for estimated labor expense
  var line = svg.selectAll(".line")
    .data(dataf, d => d.month)

line.exit().remove();
 
    line.enter().append("line")
    .attr("class", "line")
      .style("fill", 'none')
  		.attr("x1", d => x(d.month) + x.bandwidth() +5)
      .attr("x2", d => x(d.month) -5)
   .attr("y1", d => y(+d.fin_est_labor_expense))
      .attr("y2", d => y(+d.fin_est_labor_expense))
  		.style("stroke-dasharray", [6,2])
  		.style("stroke", "#eb2828")
  .style("stroke-width", 3)

}

chart.update = update;
}
chart(data)


var select = d3.select("#year")
.style("border-radius", "5px")
.on("change", function() {
chart.update(this.value, 750)
})
