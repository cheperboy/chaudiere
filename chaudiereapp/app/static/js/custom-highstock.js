/*
flask-live-charts
*/
var chart;
 
function requestConfHistory(begin_date, hour_length){
	var url = JS_base_URL +'charts/api_history/'+ begin_date +'/'+ hour_length
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
		// Note : parameters JS_begin_date and JS_hours_lenth is get from chart.py view and passed to javascript via index.html
		if(JS_begin_date){
			var conf = requestConfHistory(JS_begin_date, JS_hours_lenth)
		}
		static_chart = new Highcharts.stockChart(div_id, conf);
	}
});