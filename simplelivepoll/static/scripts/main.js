var results = {
    init: function(args) {
        var self = this;

        var url = args.next;
        if(url) {
            self.pollNext(url);
        }
    },
    pollNext: function(url) {
        // If the next question is not yet active a 404 is returned. Easy-peasy.

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
                    alert('The next question is active!');
                }
            });
        };
        request();
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
                type: 'column'
            },
            title: {
                text: results.question
            },
            yAxis: {
                min: 0,
                max: 100,
                title: {
                    text: 'Percentage'
                }
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series: results.answers
        });

        setInterval(function() {
            self.updateResults();
        }, 1000);
    }
};

