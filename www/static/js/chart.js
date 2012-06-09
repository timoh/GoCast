$(function () {
    var chart;
    $(document).ready(function() {

        function requestData() {
            $.ajax({
                url: '/data/demo',
                success: function(dt_point) {
                    var series = chart.series[0],
                        point = [dt_point["time"], dt_point["val"]],
                        shift = series.data.length > 20; // shift if the series is longer than 20

                    //add the point

                    chart.series[0].addPoint(point, true, shift);
                    
                    
                    // call it again after one second
                    //setTimeout(requestData, 1000);    
                },
                cache: false
            });
        }

    chart = new Highcharts.Chart({
            chart: {
                renderTo: 'chart1',
                defaultSeriesType: 'spline',
                events: {
                    load: requestData
                }
            },
            title: {
                text: ''
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150,
                maxZoom: 20 * 1000
            },
            yAxis: {
                minPadding: 0.2,
                maxPadding: 0.2,
                title: {
                    text: '',
                    margin: 0
                }
            },
            series: [{
                name: 'Forecast',
                data: []
            }]
        });        
});
});
