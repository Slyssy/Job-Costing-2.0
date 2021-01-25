// Search Table
$("#dashboard_search").on("keyup", function () {
  let value = $(this).val();
  console.log("Value:", value);
  let data = searchTable(value, project_list);
  buildTable(data);
});

function searchTable(value, data) {
  let filteredData = [];

  for (const item in data) {
    value = value.toLowerCase();
    let name = data[item].project_name.toLowerCase();

    if (name.includes(value)) {
      filteredData.push(data[item]);
    }
  }

  return filteredData;
}


let projectArray = Object.keys(project_list).map((i) => project_list[i]);
// console.log(projectArray);

projectArray.sort((a, b) => a.project_name !== b.project_name ? a.project_name < b.project_name ? -1 : 1 : 0);

// // Future column sort features code
// $('th').on('click', function(){
//   let column = $(this).data('column')
//   let order = $(this).data('order')
//   console.log('Column was clicked', column, order)

//   if(order == 'desc'){
//     $(this).data('order', "asc")
//   projectArray = projectArray.sort((a,b) => a[column] > b[column] ? 1 : -1)
// }
//   else{
//   $(this).data('order', "desc")
//   projectArray = projectArray.sort((a,b) => a[column] < b[column] ? 1 : -1)
// }
//   buildTable(projectArray)
// })
function formatMoney(number) {
  return number.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
}

buildTable(projectArray)

function buildTable(data){
  let table = document.getElementById('dashboardTable')
  table.innerHTML = ''
  for (let i = 0; i < data.length; i++){
    let hours_over = false
    let labor_over = false
    let material_over = false
    let misc_over = false
    let subcontractor_over = false
    
    let flag = '';
    if (data[i].fin_est_labor_hours - data[i].fin_act_labor_hours < 0 ) {
      hours_over = true;
      flag = 'flag';
    }
    
    if (parseFloat(data[i].fin_est_labor_expense.replace(/,/g, '')) - parseFloat(data[i].fin_act_labor_expense.replace(/,/g, '')) < 0 ) {
      labor_over = true;
      flag = 'flag';
    }
    if (parseFloat(data[i].fin_est_material_expense.replace(/,/g, '')) - parseFloat(data[i].fin_act_material_expense.replace(/,/g, '')) < 0 ) {
      material_over = true;
      flag = 'flag';
    }
    if (parseFloat(data[i].fin_est_miscellaneous_expense.replace(/,/g, '')) - parseFloat(data[i].fin_act_miscellaneous_expense.replace(/,/g, '')) < 0 ) {
      misc_over = true;
      flag = 'flag';
    }
    if (parseFloat(data[i].fin_est_subcontractor_expense.replace(/,/g, '')) - parseFloat(data[i].fin_act_subcontractor_expense.replace(/,/g, '')) < 0 ) {
      subcontractor_over = true;
      flag = 'flag';
    }
    
    let  row = `<tr>
                             <td><a href="/search?project_id=${data[i].id}">${data[i].project_name}</a></td>
                              <td class="revenue">$${data[i].fin_act_revenue}</td>
                              <td class="labor-hours border-secondary border-left">${data[i].fin_est_labor_hours}</td>
                              <td class="labor-hours ${hours_over}">${data[i].fin_act_labor_hours}</td>
                              <td class="labor border-secondary border-left">$${data[i].fin_est_labor_expense} </td>
                              <td class="labor ${labor_over}">$${data[i].fin_act_labor_expense}</td>
                              <td class="material border-secondary border-left">$${data[i].fin_est_material_expense}</td>
                              <td class="material ${material_over}">$${data[i].act_material_expense}</td>
                              <td class="misc border-secondary border-left">$${data[i].fin_est_miscellaneous_expense}</td>
                              <td class="misc ${misc_over}">$${data[i].fin_act_miscellaneous_expense}</td>
                              <td class="overhead border-secondary border-left">$${data[i].fin_est_overhead_expense}</td>
                              <td class="overhead">$${data[i].fin_act_overhead_expense}</td>
                              <td class="subcontractor border-secondary border-left">$${data[i].fin_est_subcontractor_expense}</td>
                              <td class="subcontractor ${subcontractor_over}">$${data[i].fin_act_subcontractor_expense}</td>
                              <td class="start-date">${data[i].act_start_date}</td>
                          </tr>`
       table.innerHTML += row   
  }
}