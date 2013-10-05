var GradingTestStrategy = (function() {
    var vocabularies_ = [];
    var index_;

    /**
     * @return a promise object
     */
    var init = function() {
        index_ = 0;
        var deferredObj = $.Deferred();
        if (vocabularies_.length === 0)
        {
            HornbookAPI.getAllMostCommonCharacters()
            .done(function(data) {
                vocabularies_ = data;
                deferredObj.resolve();
            });
        }
        else {
            deferredObj.resolve();
        }
        return deferredObj.promise();
    };

    /**
     * @return "0x12340x3456"
     */
    var getNextVocabulary = function() {
        var v = "";
        if (vocabularies_.length > 0) {
            var v = vocabularies_[index_];
            index_ += 1;
            if (index_ >= vocabularies_.length) {
                index_ = 0;
            }    
        }
        return v;
    };

    return {
        init: init,
        getNextVocabulary: getNextVocabulary
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
     * @param vocabularies ["u0x1234u0x3456", "u0x3456"]
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
     * @return "0x12240x2343"
     */
    var getNextVocabulary = function() {
        var v = "";
        if (vocabularies_.length > 0) {
            var v = vocabularies_[index_];
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

