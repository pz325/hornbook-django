var API_NEW_STUDY_URL = "/study/new_study/";   // POST url with '/'' at the end
var API_REVISE_STUDY_URL = "/study/revise_study/";   // POST url with '/'' at the end
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
     * @param start_date JS Date object
     * @param end_date JS Date object
     * @return $.ajax()
     */
    var getStudyBetween = function(start_date, end_date) {
        start_date = $.datepicker.formatDate('mm/dd/yy', start_date);
        end_date = $.datepicker.formatDate('mm/dd/yy', end_date);

        return $.ajax({
            type: "GET",
            url: API_GET_STUDY_BWTEEN_URL,
            data: {
                start_date: start_date,
                end_date: end_date
            }
        });
    };

    /*
     * @return $.ajax()
     */
    var getStudyIntelligent = function() {
        return $.ajax({
            type: "GET",
            url: API_GET_STUDY_INTELLIGENT_URL
        });
    };

    /**
     * @param vocabularies "u0x8fd9 u0x90a3 u0x6765"
     * @return $.ajax()
     */
    var newStudy = function(vocabularies) {
        return $.ajax({
            type: "POST",
            url: API_NEW_STUDY_URL,
            data: {
                vocabularies:vocabularies
            }
        });
    };

    /**
     * @param vocabularies "u0x8fd9 u0x90a3 u0x6765"
     * @return $.ajax()
     */
    var reviseStudy = function(vocabularies) {
        return $.ajax({
            type: "POST",
            url: API_REVISE_STUDY_URL,
            data: {
                vocabularies:vocabularies
            }
        });
    };

    /*
     * @return $.ajax()
     */
    var getAll = function() {
        return $.ajax({
            type: "GET",
            url: API_GET_ALL_URL
        });
    };

    return {
        getStudyBetween: getStudyBetween,
        newStudy: newStudy,
        reviseStudy: reviseStudy,
        getAll: getAll,
        getStudyIntelligent: getStudyIntelligent
    };

})();
