$(function () {
		var days = new Array; /* ['05-31', '06-01', '06-02', '06-03', '06-04', '06-05'];*/
		var income = new Array; /* = [100, 100, 0, 5, 0, 0];*/
		var expenses = new Array; /* = [-50, -10, -20, 0, -5, -10];*/
		var balance = new Array; /* = [150, 90, 70, 75, 70, 60];*/
		var forecast = new Array;
		
    var chart;
    $(document).ready(function() {
	
			
			var all_data;
		
			/* GET TRANSACTIONS FROM DB WITH getJSON() */
			$.getJSON('/api/transactions', function(data){
				all_data = data;
				
				/* ITERATE THROUGH THE TRANSACTIONS TO FORMULATE CHART DATA */
				var i;
				for (i = 0; i < all_data.length; i += 1) {
					var previous_balance = 0;
					var current_balance = 0;
					
					/* PROVIDE X-AXIS STRINGS */
					days[i] = i.toString();
					if (i == 13) {
						days[i] == 'TODAY';
					}
					
					/*FORMULATE INCOME & EXPENSE DATA FROM DUMMYDATA */
					income[i] = all_data[i].amount;
					expenses[i] = all_data[i].amount*Math.random()*-2;
					
					/* MAKE SURE WE GET A REASONABLE NUMBER */ 
					if (balance[(i-1)] > 0){
						previous_balance = balance[i-1];
					} else {
						previous_balance = 0;
					}
					
					/* CALCULATE BALANCE */
					current_balance = parseFloat(previous_balance)+parseFloat(income[i])+parseFloat(expenses[i]);
					balance[i] = current_balance;
					
					forecast[i] = current_balance+all_data[i].amount*Math.random()*0.5-1;
					
					/* SHOW THE RESULT OF THE CALCULATION FOR THE DAY */
					console.log('Balance for day #'+days[i]+' is '+balance[i]);
				}
				
				
				/* DRAW THE MOTHERF***ER */
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