/*
flask-live-charts
*/
var chart;

function parseURL(url) {
	var separator = '/'
	var arrayOfStrings = url.split(separator);
	var param = arrayOfStrings[arrayOfStrings.length-1]
	console.log(param)
	var x = parseFloat(param);
	//if is param is integer
	if (!isNaN(param) && (x | 0) === x) {
		console.log('param is integer')
		return param;
	}
	console.log('param is not integer')
	return 1;
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

function requestConfPlotbands(date, hour_length){
	var url = JSbaseURL+'charts/staticminutehistoryconf/'+date+'/'+hour_length
	console.log(url);
	var datas = $.ajax({ 
		url: url, 
		async: false
	}).responseText;
	var datas = JSON.parse(datas);
	return datas;
}

/*
	Call webapi to request data
	serie: method to call : getchaudiere or getminute
	hour_length : Int
	db_field : temp0, temp1, watt0, ..
*/
function requestData(serie, db_field, hour_length){
	var url = JSbaseURL+'webapi/'+serie+'/'+hour_length+'/'+db_field
	console.log(url);
	var datas = $.ajax({ 
		url: url, 
		async: false
	}).responseText;
	var datas = JSON.parse(datas);
	return datas;
}

/*
	Call webapi to request data by (end) date and hours (begin = end_date - hours)
	serie: method to call : getchaudierehistory or getminutehistory
	date : 
	hour_length : Int
	db_field : temp0, temp1, watt0, ..
*/
function requestDataHistory(serie, date, db_field, hour_length){
	var url = JSbaseURL+'webapi/'+serie+'/'+date+'/'+hour_length+'/'+db_field
	console.log(url);
	var datas = $.ajax({ 
		url: url, 
		async: false
	}).responseText;
	var datas = JSON.parse(datas);
	return datas;
}


$(document).ready(function() {
	div_id = 'staticchartraw-container'
	if(document.getElementById(div_id)){
		
		var conf = requestConf('staticconf/raw');
		hour_length = parseURL(window.location.href)
		series_length = Object.keys(conf.series).length;
		for (i = 0; i < series_length; i++) {
			db_field = conf.series[i].db
			conf.series[i].data = requestData('getchaudiere', db_field, hour_length)
		}
		static_chart = new Highcharts.stockChart(div_id, conf);
	}

	div_id = 'staticchartminute-container'
	if(document.getElementById(div_id)){
		// if JShistory_date is set then we are in history mode and call getchaudierehistory
		// Note : parameters JShistory_date and JShistory_hours is get from chart.py view and passed to javascript via index.html
		if(JShistory_date){
			console.log(JShistory_date)
			var conf = requestConfPlotbands(JShistory_date, JShistory_hours)
			/*
			series_length = Object.keys(conf.series).length;
			for (i = 0; i < series_length; i++) {
				db_field = conf.series[i].db
				conf.series[i].data = requestDataHistory('getminutehistory', JShistory_date, db_field, JShistory_hours)
			}
			*/
		}
		// if JShistory_date is NOT set then we are in normal mode and call getchaudiere
		// Note : parameters hour_length is parsed from url by javascript
		else{
			var conf = requestConf('staticconf/minute');
			hour_length = parseURL(window.location.href)
			series_length = Object.keys(conf.series).length;
			for (i = 0; i < series_length; i++) {
				db_field = conf.series[i].db
				conf.series[i].data = requestData('getminute', db_field, hour_length)
			}
		}
		
		
		static_chart = new Highcharts.stockChart(div_id, conf);
	}
});