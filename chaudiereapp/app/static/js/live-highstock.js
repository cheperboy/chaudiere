/*
flask-live-charts
*/
var chart;

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestLastPapp(chart_name) {
	console.log('requestLastPapp');
    $.ajax({
        url: JSbaseURL+'webapi/getlastpapp',
        success: function(point) {
            var series = live_chart.series[0],
                shift = series.data.length > 50; // shift if the series is// longer than 20
			var papp = [point[0], point[1]]
            live_chart.series[0].addPoint(papp, true, shift);
			console.log(papp);
            // call it again after one second
            setTimeout(requestLastPapp, 1000);
        },
        cache: false
    });
}

function requestData2() {
	console.log('requestData2');
    $.ajax({
        url: JSbaseURL+'charts/livedatas',
        success: function(point) {
            var series = chart.series[0],
                shift = series.data.length > 20; // shift if the series is// longer than 20
			var temp = [point[0], point[1]]
			var puiss = [point[0], point[2]]
            chart.series[0].addPoint(temp, true, false);
            chart.series[1].addPoint(puiss, true, shift);
			console.log(puiss);
            // call it again after one second
            setTimeout(requestData2, 1000);
        },
        cache: false
    });
}

function requestConf(url_part){
	var url = JSbaseURL+ 'charts/'+url_part
	var myoptions= $.ajax({ 
		url: url, 
		async: false
	}).responseText;
	var myoptions = JSON.parse(myoptions);
	//update myoptions.chart.events.load if this property exists
	if(myoptions.chart.events){
		myoptions.chart.events.load = eval(myoptions.chart.events.load);
	}
	return myoptions;
}
function requestData(){
//	var url = JSbaseURL+'webapi/conso_by_date/2018/03/19'
	var url = JSbaseURL+'webapi/getpapp/12'
	console.log(url);
	var datas = $.ajax({ 
		url: url, 
		async: false
	}).responseText;
	var datas = JSON.parse(datas);
	console.log("DATAS "+ JSON.stringify(datas, null, 4));
	return datas;
}

$(document).ready(function() {
	// if document id exist then call chart constructor
	//eval(div_id)
	div_id = 'mylivechart-container'
	if(document.getElementById(div_id)){
		var conf = requestConf('liveconf');
		console.log("opt after "+ JSON.stringify(conf, null, 4));
		live_chart = new Highcharts.stockChart(div_id, conf);
	}
	div_id = 'mystaticchart-container'
	if(document.getElementById(div_id)){
		var conf = requestConf('staticconf');
		conf.series[0].data = requestData()
		console.log("opt after "+ JSON.stringify(conf, null, 4));
		static_chart = new Highcharts.stockChart(div_id, conf);
	}
});