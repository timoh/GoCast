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
			$.getJSON('api/userstats/1', function(data){
				all_data = data;


				/* GENERATE DATE RANGE (x-axis)*/
				date_range = generateDateRange(all_data);

				/* GENERATE ARRAYS FOR DIFFERENT DATASETS FOR A SPECIFIC DATE RANGE */
				console.log('------ BUILDING START ------');

				var exists1 = new Date;
				var exists2 = new Date;
				exists1.setTime(1338768000000);
				exists2.setTime(1339027200000);

				console.log('Should find value -150 for in expenses for '+formatDateForHighCharts(exists1));
				console.log('Should find value -135 for in expenses for '+formatDateForHighCharts(exists2));

				expenses = buildDataForHighCharts(all_data.daily_expenses, date_range, 'expenses');
				income = buildDataForHighCharts(all_data.daily_incomes, date_range, 'income');
				balance = buildDataForHighCharts(all_data.daily_balances, date_range, 'balance');

				/* needs actual forecast data!!! */
				forecast = buildDataForHighCharts(all_data.daily_balances, date_range, 'forecast');

				console.log('------ BUILDING COMPLETE !!!! ------');

				/* FINALLY, CALL THE HIGHCHARTS DRAW FUNCTION */
				drawChart();
			});

			var generateDateRange = function(dateObject){

				/* PRODUCES A DATE RANGE */
				iterateDates(dateObject.daily_expenses, 'expenses');
				iterateDates(dateObject.daily_incomes, 'incomes');
				iterateDates(dateObject.daily_balances, 'balances');

				if(date_range.length == 0){
					date_range.push(smallest_day);
					console.log('date_range initialized with smallest_day, value now');
					console.log(date_range);
				}

				while (date_range[date_range.length-1] < biggest_day) {
					//console.log('Date range length is: '+date_range.length);

					var previous_day = date_range[date_range.length-1];

					/* CHECK THAT EACH DAY IS VALID DATE OBJECT*/
					if ( isNaN( previous_day.getTime() ) ) {  // d.valueOf() could also work
    				console.warn('Previous day '+previous_day+' is not a valid Date object!');
  				} 
					var created_day = new Date();
					created_day.setTime(previous_day.getTime() + (24 * 60 * 60 * 1000));

					date_range.push(created_day);



				}
				console.log('DATE RANGE:');
				console.log(date_range);

				/* FORMAT DATE OBJECTS INTO STRINGS FOR HIGHCHARTS */
				for (date in date_range) {
					date_range_string[date] = formatDateForHighCharts(date_range[date]);
				}

				console.log('Date range string:');
				console.log(date_range_string);

				return date_range_string;

			}

			var formatDateForHighCharts = function(dateObject){
				return dateObject.getFullYear()+'-'+dateObject.getMonth()+'-'+dateObject.getDate();
			}

			var buildDataForHighCharts = function(arrayOfValues, dateRange, nameOfDataSet){
				console.log('START BUILDING ***'+nameOfDataSet+'*** !!!! ------')
				var array_to_return = new Array; //array with zeros in place

				for (iterator in dateRange) {
					/* LOOP THROUGH DATES */
					var found = false; //reset for each date
					console.log('Checking if data for '+dateRange[iterator]+' is found');

						for(i in arrayOfValues){
							/* LOOP THROGH VALUES FOR EACH DATE */
							var temp_date = new Date();
							temp_date.setTime(arrayOfValues[i][0].$date); //create comparable date

							if(formatDateForHighCharts(temp_date) === dateRange[iterator]){
								/* IF A MATCHING DATE IS FOUND, MEANS THAT THERE IS DATA FOR THIS DAY */
								console.log('Value for '+dateRange[iterator]+' in dataset'+nameOfDataSet+' is '+arrayOfValues[i][1]);
								found = true; //make sure no zeros are put in wrong places
								array_to_return.push(arrayOfValues[i][1]); //add value to array
							} 
						}

						if (found == false) {
							//console.log('No data for '+dateRange[iterator]+' in dataset'+nameOfDataSet+'  was found! Adding zero.');
							/* NO DATA FOR THIS DAY WAS FOUND */
							array_to_return.push(0); //insert zero because no data is found
						}
				}

				/* DONE & DONE! */
				console.log('Building ***'+nameOfDataSet+'*** complete!');
				console.log(array_to_return);
				return array_to_return /* ARRAY OF VALUES */
			}

			var iterateDates = function(expenseCategory, categoryName){
				console.log('Now iterating over '+categoryName);
				var date_range_array = new Array;

				for (day in expenseCategory) {
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
						//console.log('New smallest day found!');
						//console.log(smallest_day);
					} else if (new_day > biggest_day) { /* BIGGER THAN CURRENTLY BIGGEST? */
						biggest_day = new_day;
						//console.log('New biggest day found!');
						//console.log(biggest_day);
					} else {
						//console.log('Same old, same old!');
					}

					console.log('Completed iterating over '+categoryName+'. Date range is:');
					console.log(date_range_array);
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