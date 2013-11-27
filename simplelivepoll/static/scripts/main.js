var results = {
    init: function(args) {
        var url = args.next;
        if(url) {
            this.pollNext(url);
        }

        this.graph();
    },
    pollNext: function(url) {
        var self = this;
        // If the next question is not yet active a 404 is returned.
        // Provide an option to move on to the next question, do not
        // automatically move them on.

        // Polling interval in ms
        var interval = 1000;

        var request = function() {
            $.ajax({
                type: 'get',
                url: url
            }).always(function(data) {
                if(data.status == '404') {
                    window.setTimeout(request, interval);
                } else {
                    self.nextQuestion(url);
                }
            });
        };
        request();
    },
    nextQuestion: function(url) {
        var message = $('.next-question-message');
        message.find('a').attr('href', url);
        message.addClass('show');
    },
    loadResults: function() {
        var results;
        $.ajax({
            url: window.location,
            type: 'get',
            async: false,
            cache: false
        }).success(function(data) {
            results = data;
        });
        return results;
    },
    updateResults: function() {
        var results = this.loadResults();

        for(var i = 0; i < results.answers.length; i++) {
            this.chart.series[i].data[0].update(results.answers[i].data, false);
        }
        this.chart.redraw();
    },
    graph: function() {
        var self = this;
        var graph = $('.highcharts');

        var results = this.loadResults();

        this.chart = new Highcharts.Chart({
            chart: {
                renderTo: graph[0],
                type: 'column',
                marginTop: 20
            },
            colors: ['#00AEEF', '#00488f', '#c0d72e'],
            credits : {
                enabled : false
            },
            title: {
                text: ''
            },
            xAxis: {
                labels: {
                    enabled: false
                }
            },
            yAxis: {
                min: 0,
                max: 100,
                title: {
                    text: 'Proportion (%)',
                    style: {
                        color: '#252525'
                    }
                }
            },
            plotOptions: {
                column: {
                    pointPadding: 0.1,
                    borderWidth: 0
                },
                tooltip: '',
                series: {
                    dataLabels: {
                        enabled: true,
                        formatter: function() {
                            return this.y + '%';
                        }
                    }
                }
            },
            tooltip: {
                formatter: function() {
                    return false;
                }
            },
            legend: {
                borderWidth: 0,
                layout: 'vertical',
                itemMarginBottom: 10,
                itemStyle: {
                    width: 200
                }
            },
            series: results.answers
        });

        setInterval(function() {
            self.updateResults();
        }, 1000);
    }
};

