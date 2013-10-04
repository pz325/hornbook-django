var API_SAVE_STUDY_URL = "/study/save_study/";
var API_GET_STUDY_BWTEEN_URL = "/study/get_study_between";

var StudyAPI = (function() {
    /**
     * @param start_date "10/02/2013"
     * @param end_date "10/03/2013"
     */
    var getStudyBetween = function(start_date, end_date) {
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
    var saveStudy = function(vocabularies) {
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
        getStudyBetween: getStudyBetween,
        saveStudy: saveStudy
    };
})();

var StudyStrategy = (function() {
    var vocabularies_ = [];
    var index_;

    /**
     * do nothing
     */
    var init = function() {
        var deferred_obj = $.Deferred();
        deferred_obj.resolve();
        return deferred_obj.promise();
    };

    /**
     * @param vocabularies 
            [
                [{u_char: u0x1234}, {u_char: u0x1345}],
                [{u_char: u0x1234}]
            ]
     */
    var setVocabularies = function(vocabularies) {
        vocabularies_ = vocabularies;
        index_ = 0;
    };

    var clearVocabularies = function() {
        vocabularies_ = [];
        index_ = 0;
    }

    /*
     * @return [{u_char: 0x1224}, {u_char: 0x2343}]
     */
    var getNextVocabulary = function() {
        var v = [];
        if (vocabularies_.length > 0) 
        {
            v = vocabularies_[index_];
            index_ += 1;
            if (index_ >= vocabularies_.length) {
                index_ = 0;
            }
        }
        return v;
    };

    return {
        init: init,
        setVocabularies: setVocabularies,
        clearVocabularies: clearVocabularies,
        getNextVocabulary: getNextVocabulary
    };
})();
