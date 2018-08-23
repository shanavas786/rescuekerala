const iDist = 1
const iLoc = 2
const iRequestee = 3
const iContact = 4
const iDate = 5
const iGps = 6
const iSummary = 7

$("input.search").keyup(search);
$(".show-details").click(showDetails);

function showDetails(evt) {
  var tds = $(evt.target).parent().siblings()
  var dist = tds.eq(iDist).text().toLowerCase()
  var loc = tds.eq(iLoc).text().toLowerCase()
  var requestee = tds.eq(iRequestee).text().toLowerCase()
  var phone = tds.eq(iContact).html()
  var date = tds.eq(iDate).text()
  var gps = tds.eq(iGps).html()
  var summary = tds.eq(iSummary).html()

  $("#req-dist").text(dist)
  $("#req-loc").text(loc)
  $("#req-requestee").text(requestee)
  $("#req-contact").html(phone)
  $("#req-date").text(date)
  $("#req-gps").html(gps)
  $("#req-summary").html(summary)

  $("#req-details").modal("show")
}

function search() {
  $("#req-table").find("tr").each(function(i,el) {
    // skip header row
    if (i == 0) return
    el = $(el)
    var tds = el.find("td")
    var loc = tds.eq(iLoc).text().toLowerCase()
    var requestee = tds.eq(iRequestee).text().toLowerCase()
    var phone = tds.eq(iContact).text()
    var locKey = $("#search-loc").val().toLowerCase()
    var reqKey = $("#search-requestee").val().toLowerCase()
    var phoneKey = $("#search-phone").val()

    if (loc.includes(locKey) &&
        requestee.includes(reqKey) &&
        phone.includes(phoneKey))
    {
      el.show()
    } else {
      el.hide()
    }
  })
}
