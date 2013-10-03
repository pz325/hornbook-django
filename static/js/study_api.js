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
     * @param vocabularies [{u_char: u0x1234}, {u_char: u0x1345}]
     */
    var set_vocabularies = function(vocabularies) {
        vocabularies_ = vocabularies;
        index_ = 0;
    };

    var clear_vocabularies = function() {
        vocabularies_ = [];
        index_ = 0;
    }

    /*
     * @return u_char
     */
    var get_next_char = function() {
        var u_char = null;
        if (vocabularies_.length > 0) 
        {
            u_char = vocabularies_[index_]["u_char"];
            index_ += 1;
            if (index_ >= vocabularies_.length) {
                index_ = 0;
            }
        }
        return u_char;
    };

    var get_next_word = function(){
        return "";
    };

    return {
        init: init,
        set_vocabularies: set_vocabularies,
        clear_vocabularies: clear_vocabularies,
        get_next_char: get_next_char,
        get_next_word: get_next_word
    };
})();
