//+ Jonas Raoni Soares Silva
//@ http://jsfromhell.com/array/shuffle [v1.0]
function shuffle(o){ //v1.0
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    return o;
};

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
        vocabularies_ = [];
        for (var i = 0; i < vocabularies.length; ++i) {
            if (vocabularies[i]) {
                vocabularies_.push(vocabularies[i]);
            }
        }
        vocabularies_ = shuffle(vocabularies_);
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
                vocabularies_ = shuffle(vocabularies_);
                index_ = 0;
            }    
        }
        return v;
    };

    /**
     * @return ["u0x1234u0x3456", "u0x3456"]
     */
    var getAllVocabularies = function() {
        return vocabularies_;
    }

    return {
        init: init,
        setVocabularies: setVocabularies,
        clearVocabularies: clearVocabularies,
        getNextVocabulary: getNextVocabulary,
        getAllVocabularies: getAllVocabularies
    };
})();

