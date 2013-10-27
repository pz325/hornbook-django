//+ Jonas Raoni Soares Silva
//@ http://jsfromhell.com/array/shuffle [v1.0]
function shuffle(o){ //v1.0
    for(var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
    return o;
};

/*
 * Vocabulary list class
 */
function VocabularyList() {
    this.vocabularies_ = [];
    this.index_ = 0;
};

/**
 * @return "0x12340x3456"
 */
VocabularyList.prototype.getNext = function () {
    var v = "";
    if (this.vocabularies_.length > 0) {
        var v = this.vocabularies_[this.index_];
        this.index_ += 1;
        if (this.index_ >= this.vocabularies_.length) {
            this.index_ = 0;
        }    
    }
    return v;
};

/**
 * @param vocabularies ["u0x1234u0x3456", "u0x3456"]
 */
VocabularyList.prototype.set = function(vocabularies) {
    this.vocabularies_ = [];
    for (var i = 0; i < vocabularies.length; ++i) {
        if (vocabularies[i]) {
            this.vocabularies_.push(vocabularies[i]);
        }
    }
    this.vocabularies_ = shuffle(this.vocabularies_);
    this.index_ = 0;
};

VocabularyList.prototype.clear = function() {
    this.vocabularies_ = [];
    this.index_ = 0;
}

/**
 * @return ["u0x1234u0x3456", "u0x3456"]
 */
VocabularyList.prototype.getAll = function() {
    return this.vocabularies_;
}

/**
 * @param vocabulary "u0x3456u0x1122"
*/
VocabularyList.prototype.add = function(vocabulary) {
    this.vocabularies_.push(vocabulary);
};

VocabularyList.prototype.isEmpty = function() {
    if (this.vocabularies_.length === 0) {
        return true;
    }
    else {
        return false;
    }
}

var GradingTestStrategy = (function() {
    var vocabularyList_ = new VocabularyList();

    /**
     * @return a promise object
     */
    var init = function() {
        var deferredObj = $.Deferred();
        if (vocabularyList_.isEmpty())
        {
            HornbookAPI.getAllMostCommonCharacters()
            .done(function(data) {
                vocabularyList_.set(data);
                deferredObj.resolve();
            });
        }
        else {
            deferredObj.resolve();
        }
        return deferredObj.promise();
    };

    return {
        init: init,
        getNextVocabulary: function(){
            return vocabularyList_.getNext();
        },
        vocabularyList: vocabularyList_
    };
})();

var StudyStrategy = (function() {
    var vocabularyList_ = new VocabularyList();

    return {
        setVocabularies: vocabularyList_.set,
        clearVocabularies: vocabularyList_.clear,
        getNextVocabulary: vocabularyList_.getNext,
        getAllVocabularies: vocabularyList_.getAll,
        add: vocabularyList_.add,
    };
})();

var RecapStrategy = (function() {
    var vocabularyList_ = new VocabularyList();

    return {
        init: function() {},
        setVocabularies: vocabularyList_.set,
        clearVocabularies: vocabularyList_.clear,
        getNextVocabulary: vocabularyList_.getNext,
        getAllVocabularies: vocabularyList_.getAll,
        add: vocabularyList_.add,
    };
})();
