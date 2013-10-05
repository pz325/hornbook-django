var API_MOST_COMMON_CHARACTER_URL = "/api/most_common_character";
var API_ALL_MOST_COMMON_CHARACTERS_URL = "/api/all_most_common_characters";
var API_MOST_COMMON_WORD_URL = "/api/most_common_word";

/**
 * Wrapper of hornbook_api
 * All method return a promised object
 * Callback function can accept (data, textStatus, jqXHR)
 */
var HornbookAPI = (function() {
    var allMostCommonCharacters = [];  // [u0x1234, u0x1345, ...]

    /**
     * Call HTTP GET /api/all_most_common_characters
     * 
     * It is a cacheable request
     * 
     * Data: [u0x1234, u0x1345, ...]
     */
    var getAllMostCommonCharacters = function() {
        var deferredObj = $.Deferred();
        if (allMostCommonCharacters.length === 0) {
            $.ajax({
                type: "GET",
                url: API_ALL_MOST_COMMON_CHARACTERS_URL
            })
            .done(function(resp, textStatus, jqXHR) {
                allMostCommonCharacters = $.parseJSON(resp);
                deferredObj.resolve(allMostCommonCharacters, textStatus, jqXHR);
            });
        }
        else {
            var textStatus = "Cached result";
            deferredObj.resolve(allMostCommonCharacters, textStatus, null);
        }
        return deferredObj.promise();
    };

    /**
     * HTTP GET /api/most_common_word
     * 
     * Data: "0x12340x2334"
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
     * 
     * Data: "0x1234"
     */
    var getMostCommonCharacter = function() {
        return $.ajax({
            type: "GET",
            url: API_MOST_COMMON_CHARACTER_URL
        })
    }

    // public interface
    return {
        getAllMostCommonCharacters: getAllMostCommonCharacters,
        getMostCommonWord: getMostCommonWord,
        getMostCommonCharacter: getMostCommonCharacter
    };
})();
