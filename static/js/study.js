$(document).ready(function() {

    function getLastWeek() {
        var today = new Date();
        var lastWeek = new Date(today.getTime()-1000*60*60*24*7);
        return lastWeek ;
    }

    function getLastMonth() {
        var today = new Date();
        var lastMonth = new Date(today.getTime()-1000*60*60*24*30);
        return lastMonth ;
    }

    /**
     * call getStudyHistoryIntelligent() or getStudyHistoryBetween()
     * @return $.ajax() deferred object
     */
    var getStudyHistory = function() {
        var history = $('#select_previous_study option:selected').val();
        console.log("history: ", history);

        if (history === "intelligent") {
            return getStudyHistoryIntelligent();
        }

        if (history === "last_week" || history === "last_month") {
            return getStudyHistoryBetween(history);
        }
    };

    /*
     * call StudyAPI.getStudyIntelligent()
     * @return $.ajax() deferred object
     */
    var getStudyHistoryIntelligent = function() {
        return StudyAPI.getStudyIntelligent();
    };

    /*
     * call StudyAPI.getStudyBetween()
     * @return $.ajax() deferred object
     */
    var getStudyHistoryBetween = function(history) {
        var today = new Date();
        var end_date = $.datepicker.formatDate('mm/dd/yy', new Date());
        var start_date = null;
        if (history === "last_week") {
            start_date = $.datepicker.formatDate('mm/dd/yy', getLastWeek());
        }
        if (history === "last_month") {
            start_date = $.datepicker.formatDate('mm/dd/yy', getLastMonth());
        }
        console.log('end_date (today):', end_date);
        console.log('start_date: ', start_date);
        return StudyAPI.getStudyBetween(start_date, end_date);
    };

    var setVocabularies = function(strategy) {
        var vocabularies = strategy.getAllVocabularies();
        console.log('set vocabularies: ', vocabularies);
        // display all vocabularies
        $("#all_study").text(vocabularies);
        // bind flashcard strategy
        Flashcard.setHanCharacterDivClickCallback(function() {
            Flashcard.displayVocabulary(strategy.getNextVocabulary());
        });
        Flashcard.displayVocabulary(strategy.getNextVocabulary());
    };

    var clearRecap = function() {
        RecapStrategy.clearVocabularies();
        $("#recap #recap_list").text("");
    };

    $("#button_add_new").click(function(){
        clearRecap();
        // save today_study
        var today_study = $("#input_today_study").val().trim();
        console.log('today study: ', today_study)
        StudyAPI.saveStudy(today_study)
        .pipe(getStudyHistory)
        .done(function(data, textStatus, jqXHR) {
            Util.notifySuccess("Study history loaded");
            // set vocabularies
            console.log('history data: ', data);
            var v = JSON.parse(data);  // v now includes today's study
            StudyStrategy.setVocabularies(v);
            setVocabularies(StudyStrategy);
        })
        .fail(function(data, textStatus, jqXHR) {
            Util.notifyError("Failed loading the study history");
        });
    });

    $("#button_load_history").click(function() {
        clearRecap();
        getStudyHistory()
        .done(function(data, textStatus, jqXHR) {
            Util.notifySuccess("Study history loaded");
            console.log('history data: ', data);
            var v = JSON.parse(data);
            StudyStrategy.setVocabularies(v);
            setVocabularies(StudyStrategy);
        })
        .fail(function(data, textStatus, jqXHR) {
            Util.notifyError("Failed loading the study history");
        });
    });

    $("#button_add_to_recap_list").click(function() {
        console.log('recap: ', Flashcard.getLastWord());
        RecapStrategy.add(Flashcard.getLastWord());
        $("#recap #recap_list").text(RecapStrategy.getAllVocabularies());
    });

    $("#button_recap").click(function() {
        var vocabularies = RecapStrategy.getAllVocabularies().join(' ');
        console.log(vocabularies);
        StudyAPI.saveStudy(vocabularies)
        .done(function(data, textStatus, jqXHR) {
            Util.notifySuccess("Recap word saved");
            setVocabularies(RecapStrategy);
        })
        .fail(function(data, textStatus, jqXHR) {
            Util.notifyError("Failed saving the recap words");
        });
    });

    // initialise
    // bind Flashcard
    Flashcard.init($("#flashcard"));
    // auto load history
    $("#button_load_history").click();
});