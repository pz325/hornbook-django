var API_MOST_COMMON_CHARACTER_URL = "/api/most_common_character";
var API_ALL_MOST_COMMON_CHARACTERS_URL = "/api/all_most_common_characters";
var API_MOST_COMMON_WORD_URL = "/api/most_common_word";

var HornbookAPI = (function() {
    var allMostCommonCharacters = []; 
            // [
            //    [{u_char: u0x1234}, {u_char: u0x1345}],
            //    [{u_char: u0x1234}]
            //]

    /**
     * Call HTTP GET /api/all_most_common_characters
     * an local cache kept
     */
    var getAllMostCommonCharacters = function() {
        var deferredObj = $.Deferred();  
        if (!allMostCommonCharacters) {
            $.ajax({
                type: "GET",
                url: API_ALL_MOST_COMMON_CHARACTERS_URL
            })
            .done(function(resp) {
                allMostCommonCharacters = $.parseJSON(resp);
                deferredObj.resolve(allMostCommonCharacters);
            });
        }
        else {
            deferredObj.resolve(allMostCommonCharacters);
        }
        return deferredObj.promise();
    };

    /**
     * HTTP GET /api/most_common_word
     */
    var getMostCommonWord = function(character, word) {
        return $.ajax({
            type: "GET",
            url: API_MOST_COMMON_WORD_URL,
            data: "ref_character=" + character + "&last_word=" + word
        });
    };

    /**
     * HTTP GET /api/most_common_character
     */
    var getMostCommonCharacter = function() {
        return $.ajax({
            type: "GET",
            url: API_MOST_COMMON_CHARACTER_URL
        });
    }

    // public interface
    return {
        getAllMostCommonCharacters: getAllMostCommonCharacters,
        getMostCommonWord: getMostCommonWord,
        getMostCommonCharacter: getMostCommonCharacter
    };
})();


var GradingTestStrategy = (function() {
    var vocabularies_ = [];
    var index_;

    var init = function() {
        index_ = 0;
        var deferredObj = $.Deferred();
        if (!vocabularies_)
        {
            HornbookAPI.getAllMostCommonCharacters()
            .done(function(data) {

            });
            $.when(HornbookAPI.get_all_most_common_characters())
            .done(function(data) {
                all_most_common_characters_ = data;
                deferred_obj.resolve();        
            });    
        }
        else {
            deferred_obj.resolve();
        }
        return deferred_obj.promise();
    };

    var get_next_char = function() {
        var u_char = all_most_common_characters_[index_]["u_char"];
        index_ += 1;
        if (index_ >= all_most_common_characters_.length) {
            index_ = 0;
        }
        return u_char;
    };

    var get_next_word = function(){
        return "";
    };

    return {
        init: init,
        get_next_char: get_next_char,
        get_next_word: get_next_word
    };
})();