function onLoad() {
  $('a#calculate').bind('click', getCalculation);
  $('button.trigger').bind('click', getBudgetData);
  $('input.expAddSubmit').bind('click', addExp);
  $('input.expRemoveSubmit').bind('click', removeExp);
  $('input.expModSubmit').bind('click', modExp);
  $('input.expModSubmit').bind('click', modExp);
  $('input.termModSubmit').bind('click', modTerm);
  $('button.loadTermData').bind('click', loadTermData);
}

function loadTermData(event) {
  var termId = event.target.id
  $.getJSON(
    $SCRIPT_ROOT + '/api/term/' + termId, {}, function(jqXHR) { displayTermData(jqXHR); }
  ).fail(
    function(jqXHR) { displayTermData(jqXHR); }
  )
}

function displayTermData(term) {
  $('.termDataDisplay').text(JSON.stringify(term));
  termDataPoints = ['title', 'leftover', 'plannedLeftover', 'spendings', 'plannedSpendings']
  $.each(termDataPoints, function(index, dataPoint) {
    $('.termData#' + dataPoint).text(term[dataPoint]);
  })

  if (term.linked) {
    $('.termData#linked').text(term['linkedTerm']['title'])
    linkedDataPoints = ['leftover', 'plannedLeftover']
    $.each(linkedDataPoints, function(index, linkedDataPoint) {
      $('.termDataTable tbody #linked_' + linkedDataPoint).text(term['linkedTerm'][linkedDataPoint])
    });
  }

  $.each(term['budgets'], function(index, budget) {
      if ( $('.budget#' + budget.id).length ) {
        $('.budget#' + budget.id + ' .budgettitle').text('wow');
        $('.budget#' + budget.id + ' .budgetbudget').text('uwu');
      } else {
        var table = '<table><thead><tr>' +
          '<th>title</th><th>Budget</th>' +
          '</tr></thead><tbody><tr>' +
          '<td class="budgettitle">'+ budget.title +'</td><td class="budgetbudget">'+ budget.budget +'</td>' +
          '</tr></tbody></table>';
        $('.budgetlist').append('<div class="budget" id="'+ budget.id +'"><div class="budgethead">' + table + '</div><ul></ul></div>');
        $.each(budget.expenditures, function(index, exp) {
            $('.budget#' + budget.id +' ul').append('<li>'+ exp.title +'</li>');
        });
      }
  });
}

function modTerm(event) {
  var tId = event.target.id

  var term = {
    title: $("#" + tId + ".termModTitle").val(),
    income: $("#" + tId + ".termModIncome").val(),
    termid: tId
  }

  $.getJSON(
    $SCRIPT_ROOT + '/_modTerm', term, function(jqXHR) { displayAddExpReturn(jqXHR, tId); }
  ).fail(
    function(jqXHR) { displayAddExpReturn(jqXHR, tId); }
  )
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

function modExp(event) {
  var eId = event.target.id
  var bId = event.target.dataset.budgetid

  var exp = {
    title: $("#" + eId + ".expModTitle").val(),
    price: $("#" + eId + ".expModPrice").val(),
    payed: $("#" + eId + ".expModPayed").is(':checked'),
    expenditureid: eId
  }

  $.getJSON(
    $SCRIPT_ROOT + '/_modExp', exp, function(jqXHR) { displayAddExpReturn(jqXHR, bId); }
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
