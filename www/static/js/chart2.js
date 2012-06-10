$(function () {

    var chart;
    $(document).ready(function() {

			var days = new Array;/* ['05-31', '06-01', '06-02', '06-03', '06-04', '06-05'];*/
			var income = new Array;/* = [100, 100, 0, 5, 0, 0];*/
			var expenses = new Array;/* = [-50, -10, -20, 0, -5, -10];*/
			var balance = new Array; /* = [150, 90, 70, 75, 70, 60];*/
			var all_data;

			$.getJSON('/api/transactions', function(data){
				all_data = data;

				var i;
				for (i = 0; i < all_data.length; i += 1) {
					income[i] = all_data[i].amount;
					expenses[i] = all_data[i].amount;
					balance[i] = all_data[i].amount;
					days[i] = i.toString();
					console.log('Day '+days[i]+' has '+income[i]+' in income, '+expenses[i]+' in expenses and '+balance[i]+' in balance.');
				}

			});



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