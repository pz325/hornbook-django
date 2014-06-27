var API_NEW_STUDY_URL = "/study/save_new_study/";   // POST url with '/'' at the end
var API_UPDATE_URL = "/study/update/";
var API_GET_ALL_URL = "/study/get_all";
var API_GET_STUDY_INTELLIGENT_URL = "/study/get_study_intelligent";
var API_GET_STATISTICS_URL = "/study/get_statistics";
var API_GET_NEW_FROM_500_URL = "/study/get_new_from_500";

/**
 * wrapper of study api
 * all function return a promise object
 * callback function support parameter list: (data, textStatus, jqXHR)
 */
var StudyAPI = (function() {
    /*
     * @return $.ajax()
     */
    var getStudyIntelligent = function() {
        return $.ajax({
            type: "GET",
            url: API_GET_STUDY_INTELLIGENT_URL
        });
    };

    /*
     * @param recall_results 
     *          { 
     *              "grasped": [ux1111 u0x2222],
     *              "unknown": [ux1111 u0x2222]
     *          }
     * @return $.ajax()
     */
    var update = function(recall_results) {
        return $.ajax({
            type: "POST",
            url: API_UPDATE_URL,
            data: {
                recall_results: recall_results
            }
        });
    };

    /**
     * @param vocabularies "u0x8fd9 u0x90a3 u0x6765"
     * @return $.ajax()
     */
    var saveNewStudy = function(vocabularies) {
        return $.ajax({
            type: "POST",
            url: API_NEW_STUDY_URL,
            data: {
                hanzi:vocabularies
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

    /*
     * @return $.ajax()
     */
    var getStatistics = function() {
        return $.ajax({
            type: "GET",
            url: API_GET_STATISTICS_URL
        });
    };

    /**
     * @ return $.ajax()
     */
    var getNewFrom500 = function(num) {
        console.log("getNewFrom500");
        return $.ajax({
            type: "GET",
            url: API_GET_NEW_FROM_500_URL,
            data: {
                num: num
            }
        });
    }

    return {
        saveNewStudy: saveNewStudy,
        update: update,
        getAll: getAll,
        getStudyIntelligent: getStudyIntelligent,
        getStatistics: getStatistics,
        getNewFrom500: getNewFrom500
    };

})();
