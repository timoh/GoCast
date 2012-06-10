$(function () {
		var date_range = new Array; //x-axis with Date objects
		var date_range_string = new Array; //x-axis with strings
		var income = new Array; /* = [100, 100, 0, 5, 0, 0];*/
		var expenses = new Array; /* = [-50, -10, -20, 0, -5, -10];*/
		var balance = new Array; /* = [150, 90, 70, 75, 70, 60];*/
		var forecast = new Array;
		var biggest_day;
		var smallest_day;

    var chart;
    $(document).ready(function() {

			var all_data;

			/* GET TRANSACTIONS FROM DB WITH getJSON() 
			*		NEED TO POPULATE FOLLOWING ARRAYS WITH 
			*		_SAME AMOUNT_ OF VALUES:
			*
			*		date_range (x-axis)
			*		income (bar chart, positive)
			*		expenses (bar chart, negative)
			*		balance (areaspline)
			*		forecast (areaspline) TODO TODO TODO !!!!!!!!!
			*
			*/
			$.getJSON('api/usermetrics/1', function(data){
				// data
				
						date_range_string = data.dates
						console.log(date_range_string);
						
						income = data.daily_incomes
						console.log(data.daily_incomes);
						
						expenses = data.daily_expenses
						console.log(data.daily_expenses);
						
						balance = data.daily_balances
						console.log(data.daily_balances);
						
						forecast = data.daily_balances
						console.log(data.daily_balances);
			
				drawChart();
			});

			/* DEFINE THE CHART DRAWING FUNCTION */
			var drawChart = function(){
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'chart2'
            },
            title: {
                text: 'Your Cashflow Forecast'
            },
            xAxis: {
                categories: date_range_string
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
                type: 'areaspline',
                name: 'Balance',
                data: balance
            }, {
                type: 'spline',
                name: 'Forecast',
                data: forecast
            }]
        });
			}


		});
});