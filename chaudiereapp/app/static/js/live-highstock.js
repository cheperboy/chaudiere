/*
flask-live-charts
*/
var chart;

function parseURL(url) {
	var separator = '/'
	var arrayOfStrings = url.split(separator);
	var param = arrayOfStrings[arrayOfStrings.length-1]
	return param
}

/**
 * Request data from the server, add it to the graph and set a timeout
 * to request again
 */
function requestLastWatt0(chart_name) {
	console.log('requestLastWatt0');
    $.ajax({
        url: JSbaseURL+'webapi/getlastwatt0',
        success: function(point) {
            var series = live_chart.series[0],
                shift = series.data.length > 50; // shift if the series is// longer than 20
			var papp = [point[0], point[1]]
            live_chart.series[0].addPoint(papp, true, shift);
			console.log(papp);
            // call it again after one second
            setTimeout(requestLastWatt0, 1000);
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
function requestData(sensor_type, sensor_id, hour_length){
	var url = JSbaseURL+'webapi/getserie/'+hour_length+'/'+sensor_type+'/'+sensor_id
	console.log(url);
	var datas = $.ajax({ 
		url: url, 
		async: false
	}).responseText;
	var datas = JSON.parse(datas);
	return datas;
}

$(document).ready(function() {
	// if document id exist then call chart constructor
	//eval(div_id)
	div_id = 'mylivechart-container'
	if(document.getElementById(div_id)){ 
		var conf = requestConf('liveconf');
		//console.log("conf "+ JSON.stringify(conf, null, 4));
		live_chart = new Highcharts.stockChart(div_id, conf);
	}
	div_id = 'staticcharttemp-container'
	if(document.getElementById(div_id)){
		var conf = requestConf('staticconf/temp');
		//conf.series[0].data = [datas[0], datas[1]]
		hour_length = parseURL(window.location.href)
		series_length = Object.keys(conf.series).length;
		for (i = 0; i < series_length; i++) {
			sensor_type = conf.series[i].sensor_type
			sensor_id = conf.series[i].sensor_id
			conf.series[i].data = requestData(sensor_type, sensor_id, hour_length)
		}
		static_chart = new Highcharts.stockChart(div_id, conf);
	}
});