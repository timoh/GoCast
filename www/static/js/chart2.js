$(function () {
	
		
		var days = ['05-31', '06-01', '06-02', '06-03', '06-04', '06-05'];
		var income = [100, 100, 0, 5, 0, 0];
		var expenses = [-50, -10, -20, 0, -5, -10];
		var balance = [150, 90, 70, 75, 70, 60];
		var all_data;
		
		$.getJSON('/api/transactions', function(data){
			all_data = data;
			console.log(all_data);
		})
	
    var chart;
    $(document).ready(function() {
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'chart2'
            },
            title: {
                text: 'Your Cashflow Forecast'
            },
            xAxis: {
                categories: days
            },
            tooltip: {
                formatter: function() {
                    var s;
                    if (this.point.name) { // the pie chart
                        s = ''+
                            this.point.name +': '+ this.y +' fruits';
                    } else {
                        s = ''+
                            this.x  +': '+ this.y;
                    }
                    return s;
                }
            },
            series: [{
                type: 'column',
                name: 'Income',
                data: income
            }, {
                type: 'column',
                name: 'Expenses',
                data: expenses
            }, {
                type: 'spline',
                name: 'Balance',
                data: balance
            }]
        });
    });
});