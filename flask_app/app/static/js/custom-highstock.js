/*
flask-live-charts
*/
var chart;

/*
Appel l'API charts/api_chart_data qui prend divers paramètres
- le nom du template JSON défini dans charts.py (eg 'static_conf_minute')
- la date de début
- la durée
L'API retourne un contenu JSON contenant la config chart + données
*/
function requestConfHistory(begin_date, hour_length, JS_chart_json_template){
	var url = JS_base_URL +'charts/api_chart_data/'+ JS_chart_json_template +'/'+ begin_date +'/'+ hour_length
	console.log(url);
	var datas = $.ajax({ 
		url: url, 
		async: false
	}).responseText;
	var datas = JSON.parse(datas);
	return datas;
}


/*
Au chargement de la page html, on vérifie que la variable JS_begin_date existe (c'est à dire qu'une chart est inclue dans la page).
Dans ce cas on récupère via l'api un contenu JSON (config chart + données)
on appel le constructeur Highcharts.stockChart avec en paramètre 
- l'id du <div> qui contient la chart et 
- les données JSON
*/
$(document).ready(function() {
	div_id = 'staticchart-container'
	if(document.getElementById(div_id)){
		// Note : parameters JS_begin_date and JS_hours_lenth is get from chart.py view and passed to javascript via index.html
		if(JS_begin_date){
			var conf = requestConfHistory(JS_begin_date, JS_hours_lenth, JS_chart_json_template)
		}
		static_chart = new Highcharts.stockChart(div_id, conf);
	}
});