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
			*		forecast (areaspline)
			*
			*/
			$.getJSON('api/userstats/1', function(data){
				all_data = data;
				
				
				/* GENERATE DATE RANGE (x-axis)*/
				date_range = generateDateRange(all_data);
				
				
				/* FINALLY, CALL THE HIGHCHARTS DRAW FUNCTION */
				drawChart();
			});
			
			var generateDateRange = function(dateObject){
				
				/* SET UP THE DATE RANGE
				*		1. FIND THE SMALLEST VALUE
				*		2. FIND THE BIGGEST VALUE
				*		3. FILL IN EVERY DAY IN BETWEEN
				*		RESULT: ARRAY WITH THE DATE RANGE
				*/	
				
				console.log('DAILY EXPENSES:');
				iterateDates(dateObject.daily_expenses);
				console.log('---- END -----');
				
				
				console.log('DAILY INCOMES:');
				iterateDates(dateObject.daily_incomes);
				console.log('---- END -----');
				
				console.log('DAILY BALANCES:');
				iterateDates(dateObject.daily_balances);
				console.log('---- END -----');
				
				/* BUILD ARRAY OF DATES BASED ON BIGGEST AND SMALLEST DAYS */
				console.log('PRINTING DATE RANGE');
				
				console.log('SMALLEST');
				console.log(smallest_day);
				
				console.log('BIGGEST');
				console.log(biggest_day);
				
				console.log('---- END -----');
				
				console.log('date_range definition:');
				console.log(date_range);
				
				if(date_range.length == 0){
					date_range.push(smallest_day);
					console.log('date_range initialized with smallest_day, value now');
					console.log(date_range);
				}
				
				while (date_range[date_range.length-1] < biggest_day) {
					console.log('Date range length is: '+date_range.length);
					
					var previous_day = date_range[date_range.length-1];
					
					/* CHECK THAT EACH DAY IS VALID DATE OBJECT*/
					if ( isNaN( previous_day.getTime() ) ) {  // d.valueOf() could also work
    				console.warn('Previous day '+previous_day+' is not a valid Date object!');
  				} 
					var created_day = new Date();
					created_day.setTime(previous_day.getTime() + (24 * 60 * 60 * 1000));
					
					date_range.push(created_day);
					
					console.log('ADDED NEW ELEMENT TO DATE RANGE:');
					console.log(date_range[date_range.length-1]);
				}
				
				/* FORMAT DATE OBJECTS INTO STRINGS FOR HIGHCHARTS */
				for (date in date_range) {
					date_range_string[date] = formatDateForHighCharts(date_range[date]);
				}
				
				console.log('Date range string:');
				console.log(date_range_string);
				
			}
			
			var formatDateForHighCharts = function(dateObject){
				return dateObject.getFullYear()+'-'+dateObject.getMonth()+'-'+dateObject.getDate();
			}
			
			var iterateDates = function(expenseCategory){
				
				var date_range_array = new Array;
				
				for (day in expenseCategory) {
					console.log('Now on iteration #'+day)
					var new_day = new Date();
					
					new_day.setTime(expenseCategory[day][0].$date);
					
					/* MAKE SURE SMALLEST AND BIGGEST DAYS ARE DEFINED */
					if (smallest_day == undefined) {
						smallest_day = new_day;
					}
					
					if (biggest_day == undefined) {
						biggest_day = new_day;
					}

					
					if (new_day < smallest_day) { /* SMALLER THAN CURRENTLY SMALLEST? */
						smallest_day = new_day;
						console.log('New smallest day found!');
						console.log(smallest_day);
					} else if (new_day > biggest_day) { /* BIGGER THAN CURRENTLY BIGGEST? */
						biggest_day = new_day;
						console.log('New biggest day found!');
						console.log(biggest_day);
					} else {
						console.log('Same old, same old!');
					}
					
					return date_range_array;
					
				}
				
			}
	
	
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
                categories: date_range
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