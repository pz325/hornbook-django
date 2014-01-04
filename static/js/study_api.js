var API_SAVE_STUDY_URL = "/study/save_study/";   // POST url with '/'' at the end
var API_GET_STUDY_BWTEEN_URL = "/study/get_study_between";
var API_GET_ALL_URL = "/study/get_all";
var API_GET_STUDY_INTELLIGENT_URL = "/study/get_study_intelligent";

/**
 * wrapper of study api
 * all function return a promise object
 * callback function support parameter list: (data, textStatus, jqXHR)
 */
var StudyAPI = (function() {
    /**
     * @param start_date "10/02/2013"
     * @param end_date "10/03/2013"
     * @return $.ajax
     */
    var getStudyBetween = function(start_date, end_date) {
        console.log('start_date: ', start_date);
        console.log('end_date: ', end_date);
        return $.ajax({
            type: "GET",
            url: API_GET_STUDY_BWTEEN_URL,
            data: {
                start_date: start_date,
                end_date: end_date
            }
        });
    };

    var getStudyIntelligent = function() {
        return $.ajax({
            type: "GET",
            url: API_GET_STUDY_INTELLIGENT_URL
        });
    };

    /**
     * @param vocabularies "u0x8fd9 u0x90a3 u0x6765"
     */
    var saveStudy = function(vocabularies) {
        return $.ajax({
            type: "POST",
            url: API_SAVE_STUDY_URL,
            data: {
                vocabularies:vocabularies
            }
        });
    };

    var getAll = function() {
        return $.ajax({
            type: "GET",
            url: API_GET_ALL_URL
        });
    };

    return {
        getStudyBetween: getStudyBetween,
        saveStudy: saveStudy,
        getAll: getAll,
        getStudyIntelligent: getStudyIntelligent
    };

})();
