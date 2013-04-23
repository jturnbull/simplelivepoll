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
    }
};

