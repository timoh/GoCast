$(function () {
    var chart;
    $(document).ready(function() {
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'chart1'
            },
            title: {
                text: 'Cashflow'
            },
            xAxis: {
                categories: ['1-12', '2-12', '3-12', '4-12', '5-12']
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
                data: [3, 2, 1, 3, 4]
            },  {
                type: 'spline',
                name: 'Balance',
                data: [3, 2.67, 3, 6.33, 3.33]
            }, {
                center: [100, 80],
                size: 100,
                showInLegend: false,
                dataLabels: {
                    enabled: false
                }
            }]
        });
    });
});
