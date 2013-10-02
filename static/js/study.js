var API_SAVE_STUDY_URL = "/study/save_study/";
var API_GET_STUDY_BWTEEN_URL = "/study/get_study_between";

var StudyAPI = (function() {
    var get_study_between = function(start_date, end_date) {

    };

    var save_study = function(vocabularies) {
        var promise = $.ajax({
            type: "POST",
            url: API_SAVE_STUDY_URL,
            data: {
                vocabularies:vocabularies
            }
        });
        return promise;
    };

    return {
        get_study_between: get_study_between,
        save_study: save_study
    };
})();