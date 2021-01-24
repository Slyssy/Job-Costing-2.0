// // Estimated Labor Expense vs. Actual Labor Expense
// let keys = Object.keys(project_dict);

// const filter = ["Labor Expense", "Labor_Hours"]

// let values = Object.values(project_dict);
// console.log(project_dict)
// console.log(values)
// console.log(keys)

// let trace1 = {
//   x: ["Bdg. Labor Exp."],
//   y: [values[7]],
//   name: "Budgeted Labor Expense",
//   type: "bar",
//   marker: {
//     color: "rgb(27, 113, 242)",
//     opacity: 0.5,
//   },
// };

// let trace2 = {
//   x: ["Act. Labor Exp."],
//   y: [values[13]],
//   name: "Actual Labor Expense",
//   type: "bar",
//   marker: {
//     color: "rgb(235, 40, 40)",
//     opacity: 0.5,
//   },
// };

// let expData = [trace1, trace2];

// let expLayout = {
//   title: "Estimated vs. Actual Labor Expense",
//   barmode: "group",
//   yaxis: {
//     title: "Labor Expense ($)",
//   },
// };

// Plotly.newPlot("eva_exp_bar", expData, expLayout);

// // Estimated Labor hours vs Actual Labor Hours
// let trace3 = {
//   x: ["Bdg. Labor Hours"],
//   y: [values[5]],
//   name: "Budgeted Labor Hours",
//   type: "bar",
//   marker: {
//     color: "rgb(27, 113, 242)",
//     opacity: 0.5,
//   },
// };

// let trace4 = {
//   x: ["Act. Labor Hours"],
//   y: [values[11]],
//   name: "Actual Labor Hours",
//   type: "bar",
//   marker: {
//     color: "rgb(235, 40, 40)",
//     opacity: 0.5,
//   },
// };

// let hourData = [trace3, trace4];

// let hourLayout = {
//   title: "Estimated vs. Actual Labor Hours",
//   barmode: "group",
//   yaxis: {
//     title: "Labor Hours",
//   },
// };

// Plotly.newPlot("eva_hr_bar", hourData, hourLayout);

// // Estimated Gross Profit vs. Actual Gross Profit
// let trace5 = {
//   x: ["Bdg. Gross Profit"],
//   y: [values[8]],
//   name: "Budgeted Gross Profit",
//   type: "bar",
//   marker: {
//     color: "rgb(27, 113, 242)",
//     opacity: 0.5,
//   },
// };

// let trace6 = {
//   x: ["Act. Gross Profit"],
//   y: [values[14]],
//   name: "Actual Gross Profit",
//   type: "bar",
//   marker: {
//     color: "rgb(235, 40, 40)",
//     opacity: 0.5,
//   },
// };

// let gpData = [trace5, trace6];

// let gpLayout = {
//   title: "Estimated vs. Actual Gross Profit",
//   barmode: "group",
//   yaxis: {
//     title: "Gross Profit",
//   },
// };

// Plotly.newPlot("eva_gp_bar", gpData, gpLayout);

console.log(project_dict)

// Function to grab data from object necessary to create plots and handle transitions
function dataGrab1({fin_est_labor_expense, fin_act_labor_expense}) {
  return {'Budgeted Expense' : +fin_est_labor_expense.replace(/,/g, ''), 'Actual Expense' : +fin_act_labor_expense.replace(/,/g, '')}
}

function dataGrab2({fin_est_labor_hours, fin_act_labor_hours}) {
  return {'Budgeted Hours': +fin_est_labor_hours, 'Actual Hours': +fin_act_labor_hours}
}

function dataGrab3({fin_est_material_expense, fin_act_material_expense}) {
  return {'Budgeted Material': +fin_est_material_expense.replace(/,/g, ''), 'Actual Material': +fin_act_material_expense.replace(/,/g, '')}
}

function dataGrab4({fin_est_miscellaneous_expense, fin_act_miscellaneous_expense}) {
  return {'Budgeted Miscellaneous': +fin_est_miscellaneous_expense.replace(/,/g, ''), 'Actual Miscellaneous': +fin_act_miscellaneous_expense.replace(/,/g, '')}
}

function dataGrab5({fin_est_subcontractor_expense, fin_act_subcontractor_expense}) {
  return {'Budgeted Subcontractor': +fin_est_subcontractor_expense.replace(/,/g, ''), 'Actual Subcontractor': +fin_act_subcontractor_expense.replace(/,/g, '')}
}

const grabbedData1 = dataGrab1(project_dict)
let data1 = Object.keys(grabbedData1).map(e => ({type: e, value: grabbedData1[e]}))
// console.log(data1)

const grabbedData2 = dataGrab2(project_dict)
let data2 = Object.keys(grabbedData2).map(e => ({type: e, value: grabbedData2[e]}))
// console.log(data2)

const grabbedData3 = dataGrab3(project_dict)
let data3 = Object.keys(grabbedData3).map(e => ({type: e, value: grabbedData3[e]}))
// console.log(data3)

const grabbedData4 = dataGrab4(project_dict)
let data4 = Object.keys(grabbedData4).map(e => ({type: e, value: grabbedData4[e]}))
// console.log(data4)

const grabbedData5 = dataGrab5(project_dict)
let data5 = Object.keys(grabbedData5).map(e => ({type: e, value: grabbedData5[e]}))
// console.log(data5)


// set the dimensions and margins of the graph
const margin = {top: 70, right: 30, bottom: 70, left: 120},
    width = 560 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
const svg = d3.select("#eva_exp_bar")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// Initialize the X axis
const x = d3.scaleBand()
  .range([ 0, width ])
  .padding(0.2);

const xAxis = svg.append("g")
  .attr("transform", "translate(0," + height + ")")

// Initialize the Y axis
const y = d3.scaleLinear()
  .range([ height, 0]);
const yAxis = svg.append("g")
  .attr("class", "myYaxis") 

  yAxis
  .append('text')
    .attr('class', 'yAxis')
    .attr('y', -60)
    .attr('x', -20)
    .attr('transform', `rotate(-90)`)
    .attr("fill", "#635f5d")
    .style('font-size', '1.5em')
    .text("Labor Expense ($) / Labor Hours")

   svg.append('text')
    .attr('y', -10)
    .attr('x', 80)
    .attr('class', 'title')
    .text("Estimate vs. Actual Labor")
    .attr("fill", "#635f5d")
    .style('font-size', '1.7em')


// A function that create / update the plot for a given variable:
function update(data) {

  // Update the X axis
  x.domain(data.map(d => d.type))
  xAxisG = xAxis.call(d3.axisBottom(x))

  xAxisG
  // .style("color", "#635f5d")
  // .style('font-size', '2.0em')

  // Update the Y axis
  y.domain([0, d3.max(data, d => d.value ) * 1.2 ]);
  yAxis.transition().duration(1000).call(d3.axisLeft(y));

  // Create the u variable
  const u = svg.selectAll("rect")
    .data(data)

    const colors = d3.scaleOrdinal()
    .domain(['Budget Expense', 'Actual Expense'])
    .range([ '#1b71f2', '#eb2828'])

  u
    .enter()
    .append("rect") // Add a new rect for each new elements
    .merge(u) // get the already existing elements as well
    .transition() // and apply changes to all of them
    .duration(1000)
      .attr("x", d => x(d.type))
      .attr("y", d => y(d.value))
      .attr("width", x.bandwidth())
      .attr("height", d => height - y(d.value))
      .attr("fill", function(d, i)  {return colors(d.type)})
      .style("opacity", "0.5")
      // "#1b71f2", "#eb2828"
  // If less group in the new dataset, I delete the ones not in use anymore
  u
    .exit()
    .remove()
}


// Initialize the plot with the first dataset
update(data1)

// Start Estmated Material, Misc and Subcontractor
// set the dimensions and margins of the graph

// append the svg object to the body of the page
const svg1 = d3.select("#eva_mat_misc_sub_bar")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// Initialize the X axis
const x1 = d3.scaleBand()
  .range([ 0, width ])
  .padding(0.2);

const xAxis1 = svg1.append("g")
  .attr("transform", "translate(0," + height + ")")

// Initialize the Y axis
const y1 = d3.scaleLinear()
  .range([ height, 0]);
const yAxis1 = svg1.append("g")
  .attr("class", "myOtherYaxis") 

  yAxis1
  .append('text')
    .attr('class', 'yAxis')
    .attr('y', -60)
    .attr('x', -60)
    .attr('transform', `rotate(-90)`)
    .attr("fill", "#635f5d")
    .style('font-size', '1.5em')
    .text("Expense Values ($)")

   svg1.append('text')
    .attr('y', -10)
    .attr('x', 20)
    .attr('class', 'title')
    .text("Estimate vs. Actual (Mat, Misc & Sub)")
    .attr("fill", "#635f5d")
    .style('font-size', '1.7em')


// A function that create / update the plot for a given variable:
function update1(data) {

  // Update the X axis
  x1.domain(data.map(d => d.type))
  xAxisG1 = xAxis1.call(d3.axisBottom(x1))

  xAxisG1
  // .style("color", "#635f5d")
  // .style('font-size', '2.0em')

  // Update the Y axis
  y1.domain([0, d3.max(data, d => d.value ) * 1.2 ]);
  yAxis1.transition().duration(1000).call(d3.axisLeft(y1));

  // Create the u variable
  const u1 = svg1.selectAll("rect")
    .data(data)

    const colors = d3.scaleOrdinal()
    .domain(['Budget Expense', 'Actual Expense'])
    .range([ '#1b71f2', '#eb2828'])

  u1
    .enter()
    .append("rect") // Add a new rect for each new elements
    .merge(u1) // get the already existing elements as well
    .transition() // and apply changes to all of them
    .duration(1000)
      .attr("x", d => x1(d.type))
      .attr("y", d => y1(d.value))
      .attr("width", x1.bandwidth())
      .attr("height", d => height - y1(d.value))
      .attr("fill", function(d, i)  {return colors(d.type)})
      .style("opacity", "0.5")
      // "#1b71f2", "#eb2828"
  // If less group in the new dataset, I delete the ones not in use anymore
  u1
    .exit()
    .remove()
}

update1(data3)