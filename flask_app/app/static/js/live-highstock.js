/*
flask-live-charts
*/
var chart;
 
function requestConfHistory(begin_date, hour_length){
	var url = JSbaseURL+'charts/api_history/'+ begin_date +'/'+ hour_length
	console.log(url);
	var datas = $.ajax({ 
		url: url, 
		async: false
	}).responseText;
	var datas = JSON.parse(datas);
	return datas;
}

$(document).ready(function() {
	div_id = 'staticchart-container'
	if(document.getElementById(div_id)){
		// Note : parameters JS_begin_date and JShistory_hours is get from chart.py view and passed to javascript via index.html
		if(JS_begin_date){
			var conf = requestConfHistory(JS_begin_date, JShistory_hours)
		}
		static_chart = new Highcharts.stockChart(div_id, conf);
	}
});