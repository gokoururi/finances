function onLoad() {
  $('a#calculate').bind('click', getCalculation);
  $('button.trigger').bind('click', getBudgetData);
  $('input.expAddSubmit').bind('click', addExp);
  $('input.expRemoveSubmit').bind('click', removeExp);
}

function displayAddExpReturn(request, id) {
  $("#" + id + ".expAddResult").text(request.result);
  location.reload()
}

function removeExp(event) {
  var bId = event.target.id
  $.getJSON(
    $SCRIPT_ROOT + '/_removeExp/' + bId, function(jqXHR) { displayAddExpReturn(jqXHR, bId); }
  ).fail(
    function(jqXHR) { displayAddExpReturn(jqXHR, bId); }
  )
}

function addExp(event) {
  var bId = event.target.id

  var newExp = {
    title: $("#" + bId + ".expAddTitle").val(),
    price: $("#" + bId + ".expAddPrice").val(),
    payed: $("#" + bId + ".expAddPayed").is(':checked'),
    budgetid: bId
  }

  $.getJSON(
    $SCRIPT_ROOT + '/_addExp', newExp, function(jqXHR) { displayAddExpReturn(jqXHR, bId); }
  ).fail(
    function(jqXHR) { displayAddExpReturn(jqXHR, bId); }
  )

}

function displayBudgetData(data) {
  $("#" + data.id + ".targetTitle").text(data.title);
  $("#" + data.id + ".targetBudget").text(data.budget);
}

function getBudgetData(event) {
  $.getJSON($SCRIPT_ROOT + '/_budgetData', { id: event.target.id }, displayBudgetData)
}

function displayCalculation(data) {
  $("#result").text(data.result);
}

function getCalculation() {
  var calcdata = {
      a: $('input[name="a"]').val(),
      b: $('input[name="b"]').val()
  }
  $.getJSON($SCRIPT_ROOT + '/_add_numbers', calcdata, displayCalculation)
  return false;
}

$(onLoad);
