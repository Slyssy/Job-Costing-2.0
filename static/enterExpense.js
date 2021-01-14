var expenseType = exp_dropdown_dict.expense_list.map((d) => d.expense);
var expEle = document.getElementById("expense");
for (let i = 0; i < expenseType.length; i++) {
  var opt = expenseType[i];

  var el = document.createElement("option");
  el.text = opt;
  el.value = opt;

  expEle.add(expEl);
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