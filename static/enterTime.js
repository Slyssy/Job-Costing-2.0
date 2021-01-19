// function GetSortOrder(prop) {    
//   return function(a, b) {    
//       if (a[prop] > b[prop]) {    
//           return 1;    
//       } else if (a[prop] < b[prop]) {    
//           return -1;    
//       }    
//       return 0;    
//   }    
// }    

// Select Employee Name
var employees = dropdown_dict.employee_list.map((d) => d.name);
// employees.sort(GetSortOrder("name"));
// employees.sort(function(a,b){return b - a});
// var sorted = employees.sort(function(a,b){return b-a});
var ele = document.getElementById("name");
for (var i = 0; i < employees.length; i++) {
  var opt = employees[i];
// for (var i = 0; i < sorted.length; i++) {
//   var opt = sorted[i];

  var el = document.createElement("option");
  el.text = opt;
  el.value = opt;

  ele.add(el);
}

// Select Project Name
var projects = dropdown_dict.project_list.map((d) => d.name);
var ele = document.getElementById("proName");
for (var i = 0; i < projects.length; i++) {
  var opt = projects[i];
  var el = document.createElement("option");
  el.text = opt;
  el.value = opt;
  ele.add(el);
}
