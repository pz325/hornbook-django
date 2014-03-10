var Util = (function() {
    var notifyError = function(msg) {
        $.jGrowl(msg);
    };

    var notifySuccess = function(msg) {
        $.jGrowl(msg);
    };

    var getLastWeek = function() {
        var today = new Date();
        var lastWeek = new Date(today.getTime()-1000*60*60*24*7);
        return lastWeek ;
    };

    var getLastMonth = function() {
        var today = new Date();
        var lastMonth = new Date(today.getTime()-1000*60*60*24*30);
        return lastMonth ;
    };

    return {
        notifySuccess: notifySuccess,
        notifyError: notifyError,
        getLastMonth: getLastMonth,
        getLastWeek: getLastWeek
    };
})();
