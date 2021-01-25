console.log(project_list);
// load the data
projectArray = Object.keys(project_list).map((i) => project_list[i]);
console.log(projectArray);

// Filtering data to be used for plot
const chartData = projectArray.map(
  ({
    act_start_date,
    fin_est_labor_expense,
    fin_act_labor_expense,
    fin_act_revenue,
    fin_est_material_expense,
    act_material_expense,
    fin_est_miscellaneous_expense,
    act_miscellaneous_expense,
    fin_est_subcontractor_expense,
    act_subcontractor_expense,
  }) => ({
    act_start_date,
    fin_est_labor_expense: parseFloat(fin_est_labor_expense.replace(/,/g, "")),
    fin_act_labor_expense: parseFloat(fin_act_labor_expense.replace(/,/g, "")),
    fin_act_revenue: parseFloat(fin_act_revenue.replace(/,/g, "")),
    fin_est_material_expense: parseFloat(
      fin_est_material_expense.replace(/,/g, "")
    ),
    act_material_expense: parseFloat(act_material_expense.replace(/,/g, "")),
    fin_est_miscellaneous_expense: parseFloat(
      fin_est_miscellaneous_expense.replace(/,/g, "")
    ),
    act_miscellaneous_expense: parseFloat(act_miscellaneous_expense),
    fin_est_subcontractor_expense: parseFloat(
      fin_est_subcontractor_expense.replace(/,/g, "")
    ),
    act_subcontractor_expense: parseFloat(act_subcontractor_expense),
  })
);
// console.log(chartData)

// Grouping dates into months and summing estimated and actual labor expense by month
const mapper = (single) => {
  let d = single.act_start_date.split("-");
  let e = Number(single.fin_est_labor_expense);
  let a = Number(single.fin_act_labor_expense);
  let r = Number(single.fin_act_revenue);
  let m = Number(single.act_material_expense);
  let q = Number(single.act_miscellaneous_expense);
  let s = Number(single.act_subcontractor_expense);
  let em = Number(single.fin_est_material_expense);
  let eq = Number(single.fin_est_miscellaneous_expense);
  let es = Number(single.fin_est_subcontractor_expense);

  return {
    year: d[0],
    month: d[1],
    fin_est_labor_expense: e,
    fin_act_labor_expense: a,
    fin_act_revenue: r,
    act_material_expense: m,
    act_miscellaneous_expense: q,
    act_subcontractor_expense: s,
    fin_est_material_expense: em,
    fin_est_miscellaneous_expense: eq,
    fin_est_subcontractor_expense: es,
  };
};

const reducer = (group, current) => {
  let i = group.findIndex(
    (single) => single.year == current.year && single.month == current.month
  );
  if (i == -1) {
    return [...group, current];
  }
  group[i].fin_act_revenue += current.fin_act_revenue;
  group[i].fin_est_labor_expense += current.fin_est_labor_expense;
  group[i].fin_act_labor_expense += current.fin_act_labor_expense;
  group[i].act_material_expense += current.act_material_expense;
  group[i].act_miscellaneous_expense += current.act_miscellaneous_expense;
  group[i].act_subcontractor_expense += current.act_subcontractor_expense;
  group[i].fin_est_material_expense += current.fin_est_material_expense;
  group[i].fin_est_miscellaneous_expense +=
    current.fin_est_miscellaneous_expense;
  return group;
};

const sumPerMonth = chartData.map(mapper).reduce(reducer, []);
// console.log(sumPerMonth);

// Sorting data by month
const data0 = sumPerMonth.sort((a, b) => a.month - b.month);
// console.log(data0)

// Changing month number to month name
const months = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];

const data = data0.map((o) => ({ ...o, month: months[o.month - 1] }));
console.log(data);

function chart(data) {
  // Looping through data to pull the Unique years in the data set.
  const years = data
    .map((a) => a.year)
    .filter((value, index, self) => self.indexOf(value) === index);
  years.sort(function (a, b) {
    return a - b;
  });
  // console.log(years)

  const options = d3
    .select("#year")
    .selectAll("option")
    .data(years)
    .enter()
    .append("option")
    .text((d) => d);

  var svg = d3.select("#estimate-to-actual"),
    margin = { top: 70, right: -45, bottom: 0, left: 90 },
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;

  // Setting x Scale
  const x = d3
    .scaleBand()
    .range([margin.left, width - margin.right])
    .padding(0.1)
    .paddingOuter(0.2);

  var y = d3.scaleLinear().range([height - margin.bottom, margin.top]);

  var xAxis = (g) =>
    g
      .attr("transform", "translate(0," + (height - margin.bottom) + ")")
      .call(d3.axisBottom(x).tickSizeOuter(0));

  var yAxis = (g) =>
    g
      .attr("transform", "translate(" + margin.left + ",0)")
      .call(d3.axisLeft(y).tickSize(-width));

  svg.append("g").attr("class", "x-axis");

  svg
    .append("g")
    .attr("class", "y-axis")
    .append("text")
    .attr("class", "yAxis")
    .attr("y", -70)
    .attr("x", -195)
    .attr("transform", `rotate(-90)`)
    .attr("fill", "#635f5d")
    .style("font-size", "2.5em")
    .text("Labor Expense ($)");

  update(d3.select("#year").property("value"), 0);

  function update(year, speed) {
    var dataf = data.filter((f) => f.year == year);

    y.domain([0, d3.max(data, (d) => d.fin_est_labor_expense)]).nice();

    svg.selectAll(".y-axis").transition().duration(speed).call(yAxis);

    x.domain(data.map((d) => d.month));

    svg.selectAll(".x-axis").transition().duration(speed).call(xAxis);

    var bar = svg.selectAll(".bar").data(dataf, (d) => d.month);

    bar.exit().remove();

    var bar1 = bar
      .enter()
      .append("rect")
      .attr("class", "bar")
      .style("fill", (d) =>
        d.fin_act_labor_expense < d.fin_est_labor_expense
          ? "#1b71f2"
          : "#eb2828"
      )
      .attr("opacity", ".5")
      .attr("width", x.bandwidth());

    bar1
      .merge(bar)
      .transition()
      .duration(speed)
      .attr("x", (d) => x(d.month))
      .attr("y", (d) => y(d.fin_act_labor_expense))
      .attr("height", (d) => y(0) - y(d.fin_act_labor_expense));

    // Adding Tooltip Behavior
    bar1
      .on("mouseover", function (d) {
        d3.select(this).style("fill", "#a834eb");
        d3.select("#act_labor_exp").text(
          " $" + valueFormat(d.fin_act_labor_expense)
        );

        //Position the tooltip <div> and set its content
        let x = d3.event.pageX;
        let y = d3.event.pageY - 40;

        //Position tooltip and make it visible
        d3.select("#tooltip-bar")
          .style("left", x + "px")
          .style("top", y + "px")
          .style("opacity", 1);
      })

      .on("mouseout", function () {
        d3.select(this).style("fill", function (d) {
          return d.fin_act_labor_expense < d.fin_est_labor_expense
            ? "#1b71f2"
            : "#eb2828";
        });

        //Hide the tooltip
        d3.select("#tooltip-bar").style("opacity", "0");
      });

    // Defining limit lines for estimated labor expense
    var line = svg.selectAll(".line").data(dataf, (d) => d.month);

    line.exit().remove();

    var line1 = line
      .enter()
      .append("line")
      .attr("class", "line")
      .style("fill", "none")
      .attr("x1", (d) => x(d.month) + x.bandwidth() + 5)
      .attr("x2", (d) => x(d.month) - 5);

    line1
      .merge(line)
      .transition()
      .duration(speed)
      .attr("y1", (d) => y(+d.fin_est_labor_expense))
      .attr("y2", (d) => y(+d.fin_est_labor_expense))
      .style("stroke-dasharray", [6, 2])
      .style("stroke", "#eb2828")
      .style("stroke-width", 3);

    // Adding Tooltip Behavior
    line1
      .on("mouseover", function (d) {
        d3.select(this).style("stroke", "#a834eb");
        d3.select("#est_labor_exp").text(
          " $" + valueFormat(d.fin_est_labor_expense)
        );

        //Position the tooltip <div> and set its content
        let x = d3.event.pageX;
        let y = d3.event.pageY - 40;

        //Position tooltip and make it visible
        d3.select("#tooltip-line")
          .style("left", x + "px")
          .style("top", y + "px")
          .style("opacity", 1);
      })

      .on("mouseout", function () {
        d3.select(this).style("stroke", "#eb2828");

        //Hide the tooltip
        d3.select("#tooltip-line").style("opacity", "0");
      });
  }

  chart.update = update;
}
chart(data);

var select = d3
  .select("#year")
  .style("border-radius", "5px")
  .on("change", function () {
    chart.update(this.value, 750);
  });

function matChart(data) {
  // Looping through data to pull the Unique years in the data set.
  const matYears = data
    .map((a) => a.year)
    .filter((value, index, self) => self.indexOf(value) === index);
  matYears.sort(function (a, b) {
    return a - b;
  });
  // console.log(years)

  const options = d3
    .select("#matYear")
    .selectAll("option")
    .data(matYears)
    .enter()
    .append("option")
    .text((d) => d);

  var svg = d3.select("#estimate-to-actual-material"),
    margin = { top: 70, right: -45, bottom: 0, left: 90 },
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;

  // Setting x Scale
  const x = d3
    .scaleBand()
    .range([margin.left, width - margin.right])
    .padding(0.1)
    .paddingOuter(0.2);

  var y = d3.scaleLinear().range([height - margin.bottom, margin.top]);

  var xAxis = (g) =>
    g
      .attr("transform", "translate(0," + (height - margin.bottom) + ")")
      .call(d3.axisBottom(x).tickSizeOuter(0));

  var yAxis = (g) =>
    g
      .attr("transform", "translate(" + margin.left + ",0)")
      .call(d3.axisLeft(y).tickSize(-width));

  svg.append("g").attr("class", "x-axis");

  svg
    .append("g")
    .attr("class", "y-axis")
    .append("text")
    .attr("class", "yAxis")
    .attr("y", -70)
    .attr("x", -190)
    .attr("transform", `rotate(-90)`)
    .attr("fill", "#635f5d")
    .style("font-size", "2.5em")
    .text("Material Expense ($)");

  matUpdate(d3.select("#matYear").property("value"), 0);

  function matUpdate(year, speed) {
    var dataf = data.filter((f) => f.year == year);

    y.domain([0, d3.max(data, (d) => d.fin_est_material_expense)]).nice();

    svg.selectAll(".y-axis").transition().duration(speed).call(yAxis);

    x.domain(data.map((d) => d.month));

    svg.selectAll(".x-axis").transition().duration(speed).call(xAxis);

    var bar = svg.selectAll(".bar").data(dataf, (d) => d.month);

    bar.exit().remove();

    var bar1 = bar
      .enter()
      .append("rect")
      .attr("class", "bar")
      .style("fill", (d) =>
        d.act_material_expense < d.fin_est_material_expense
          ? "#1b71f2"
          : "#eb2828"
      )
      .attr("opacity", ".5")
      .attr("width", x.bandwidth());

    bar1
      .merge(bar)
      .transition()
      .duration(speed)
      .attr("x", (d) => x(d.month))
      .attr("y", (d) => y(d.act_material_expense))
      .attr("height", (d) => y(0) - y(d.act_material_expense));

    // Adding Tooltip Behavior
    bar1
      .on("mouseover", function (d) {
        d3.select(this).style("fill", "#a834eb");
        d3.select("#act_material_exp").text(
          " $" + valueFormat(d.act_material_expense)
        );

        //Position the tooltip <div> and set its content
        let x = d3.event.pageX;
        let y = d3.event.pageY - 40;

        //Position tooltip and make it visible
        d3.select("#tooltip-mat-bar")
          .style("left", x + "px")
          .style("top", y + "px")
          .style("opacity", 1);
      })

      .on("mouseout", function () {
        d3.select(this).style("fill", function (d) {
          return d.act_material_expense < d.fin_est_material_expense
            ? "#1b71f2"
            : "#eb2828";
        });

        //Hide the tooltip
        d3.select("#tooltip-mat-bar").style("opacity", "0");
      });

    // Defining limit lines for estimated labor expense
    var line = svg.selectAll(".line").data(dataf, (d) => d.month);

    line.exit().remove();

    var line1 = line
      .enter()
      .append("line")
      .attr("class", "line")
      .style("fill", "none")
      .attr("x1", (d) => x(d.month) + x.bandwidth() + 5)
      .attr("x2", (d) => x(d.month) - 5);

    line1
      .merge(line)
      .transition()
      .duration(speed)
      .attr("y1", (d) => y(+d.fin_est_material_expense))
      .attr("y2", (d) => y(+d.fin_est_material_expense))
      .style("stroke-dasharray", [6, 2])
      .style("stroke", "#eb2828")
      .style("stroke-width", 3);

    // Adding Tooltip Behavior
    line1
      .on("mouseover", function (d) {
        d3.select(this).style("stroke", "#a834eb");
        d3.select("#est_material_exp").text(
          " $" + valueFormat(d.fin_est_labor_expense)
        );

        //Position the tooltip <div> and set its content
        let x = d3.event.pageX;
        let y = d3.event.pageY - 40;

        //Position tooltip and make it visible
        d3.select("#tooltip-mat-line")
          .style("left", x + "px")
          .style("top", y + "px")
          .style("opacity", 1);
      })

      .on("mouseout", function () {
        d3.select(this).style("stroke", "#eb2828");

        //Hide the tooltip
        d3.select("#tooltip-mat-line").style("opacity", "0");
      });
  }

  matChart.update = matUpdate;
}
matChart(data);

var select = d3
  .select("#matYear")
  .style("border-radius", "5px")
  .on("change", function () {
    matChart.update(this.value, 750);
  });

function revChart(data) {
  // Looping through data to pull the Unique years in the data set.
  const revYears = data
    .map((a) => a.year)
    .filter((value, index, self) => self.indexOf(value) === index);
  revYears.sort(function (a, b) {
    return a - b;
  });
  // console.log(years)

  const options = d3
    .select("#rev-year")
    .selectAll("option")
    .data(revYears)
    .enter()
    .append("option")
    .text((d) => d);

  var svg = d3.select("#revenue_barchart"),
    margin = { top: 70, right: -55, bottom: 0, left: 110 },
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;

  // Setting x Scale
  const x = d3
    .scaleBand()
    .range([margin.left, width - margin.right])
    .padding(0.1)
    .paddingOuter(0.2);

  var y = d3.scaleLinear().range([height - margin.bottom, margin.top]);

  var xAxis = (g) =>
    g
      .attr("transform", "translate(0," + (height - margin.bottom) + ")")
      .call(d3.axisBottom(x).tickSizeOuter(0));

  var yAxis = (g) =>
    g
      .attr("transform", "translate(" + margin.left + ",0)")
      .call(d3.axisLeft(y).tickSize(-width));

  svg.append("g").attr("class", "x-axis");

  svg
    .append("g")
    .attr("class", "y-axis")
    .append("text")
    .attr("class", "yAxis")
    .attr("y", -70)
    .attr("x", -220)
    .attr("transform", `rotate(-90)`)
    .attr("fill", "#635f5d")
    .style("font-size", "2.5em")
    .text("Revenue ($)");

  revUpdate(d3.select("#rev-year").property("value"), 0);

  function revUpdate(year, speed) {
    var dataf = data.filter((f) => f.year == year);

    y.domain([0, d3.max(data, (d) => d.fin_act_revenue)]).nice();

    svg.selectAll(".y-axis").transition().duration(speed).call(yAxis);

    data.sort(
      d3.select("#sort").property("checked")
        ? (a, b) => b.fin_act_revenue - a.fin_act_revenue
        : (a, b) => months.indexOf(a.month) - months.indexOf(b.month)
    );

    x.domain(data.map((d) => d.month));

    svg.selectAll(".x-axis").transition().duration(speed).call(xAxis);

    var bar = svg.selectAll(".bar").data(dataf, (d) => d.month);

    bar.exit().remove();

    var bar1 = bar
      .enter()
      .append("rect")
      .attr("class", "bar")
      .style("fill", "#1b71f2")
      .attr("opacity", ".5")
      .attr("width", x.bandwidth())
      .merge(bar);

    bar1
      .transition()
      .duration(speed)
      .attr("x", (d) => x(d.month))
      .attr("y", (d) => y(d.fin_act_revenue))
      .attr("height", (d) => y(0) - y(d.fin_act_revenue));

    // Adding Tooltip Behavior
    bar1
      .on("mouseover", function (d) {
        d3.select(this).style("fill", "#a834eb");
        d3.select("#monthlyRevenue").text(
          " $" + valueFormat(d.fin_act_revenue)
        );

        //Position the tooltip <div> and set its content
        let x = d3.event.pageX;
        let y = d3.event.pageY - 40;

        //Position tooltip and make it visible
        d3.select("#tooltip-revenue-bar")
          .style("left", x + "px")
          .style("top", y + "px")
          .style("opacity", 1);
      })

      .on("mouseout", function () {
        d3.select(this).style("fill", "#1b71f2");

        //Hide the tooltip
        d3.select("#tooltip-revenue-bar").style("opacity", "0");
      });
  }
  revChart.update = revUpdate;
}
revChart(data);

var checkbox = d3
  .select("#sort")
  .style("margin-left", "45%")
  .on("click", function () {
    revChart.update(select.property("value"), 750);
  });

var select = d3
  .select("#rev-year")
  .style("border-radius", "5px")
  .on("change", function () {
    revChart.update(this.value, 750);
  });
