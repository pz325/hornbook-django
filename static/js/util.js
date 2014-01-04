var Util = (function() {
    var notifyError = function(msg) {
        $.jGrowl(msg);
    };

    var notifySuccess = function(msg) {
        $.jGrowl(msg);
    };

    return {
        notifySuccess: notifySuccess,
        notifyError: notifyError
    };
})();