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

    //+ Jonas Raoni Soares Silva
    //@ http://jsfromhell.com/array/shuffle [v1.0]
    var shuffle = function(o){ //v1.0
        for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
        return o;
    };

    return {
        notifySuccess: notifySuccess,
        notifyError: notifyError,
        getLastMonth: getLastMonth,
        getLastWeek: getLastWeek,
        shuffle: shuffle
    };
})();
