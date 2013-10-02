var API_SAVE_STUDY_URL = "/study/save_study/";
var API_GET_STUDY_BWTEEN_URL = "/study/get_study_between";

var StudyAPI = (function() {
    /**
     * @param start_date "10/02/2013"
     * @param end_date "10/03/2013"
     */
    var get_study_between = function(start_date, end_date) {
        console.log('start_date: ', start_date);
        console.log('end_date: ', end_date);
        var promise = $.ajax({
            type: "GET",
            url: API_GET_STUDY_BWTEEN_URL,
            data: {
                start_date: start_date,
                end_date: end_date
            }
        });
        return promise;
    };

    /**
     * @param vocabularies "u0x8fd9 u0x90a3 u0x6765"
     */
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