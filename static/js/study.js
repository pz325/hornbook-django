$(document).ready(function() {

/// Study elements
    var $txtAllStudy_ = $("#all_study");
    var $txtRecapList_ = $("#recap #recap_list");
    var studyList_ = new VocabularyList();
    var clickCallback_ = null;
    var currentMode_ = '';
    var recapList_ = new VocabularyList();

/// utility methods
    var getLastWeek = function() {
        var today = new Date();
        var lastWeek = new Date(today.getTime()-1000*60*60*24*7);
        return lastWeek ;
    };

    var getLastMonth = function() {
        var today = new Date();
        var lastMonth = new Date(today.getTime()-1000*60*60*24*30);
        return lastMonth ;
    };

    var resetUI = function() {
       $txtAllStudy_.text("");
       $txtRecapList_.text("");
       studyList_.clear();
       clickCallback_ = null;
       currentMode_ = '';
    };

    /**
     *
     */
    var setUI = function() {
        var vocabularies = studyList_.getAll();
        console.log('Study list: ', vocabularies);
        // display all vocabularies
        $txtAllStudy_.text(vocabularies);
        // bind flashcard strategy
        Flashcard.setHanCharacterDivClickCallback(clickCallback_);
        Flashcard.displayVocabulary(studyList_.get());
    };

/// ======== study new ========

    /*
     * Flashcard click callback in study new mode
     *     display the next vocabulary
     */
    var studyNewClickCallback = function() {
        Flashcard.displayVocabulary(studyList_.getNext());
    };

    /*
     * Init elements for the study new mode
     */ 
    var initStudyNew = function() {
        resetUI();

        // get new studies
        var today_study = $("#input_today_study").val().trim();
        console.log("today study: ", today_study);
        studyList_.set(today_study.split(" "));

        clickCallback_ = studyNewClickCallback;
        
        currentMode_ = "StudyNew";

        setUI();
    };

    $("#button_add_new").click(function() {
        initStudyNew();
    });

    $("#button_save_to_server").click(function() {
        if (currentMode_ === "StudyNew") {
            StudyAPI.newStudy(studyList_.getAll().join(" "))
            .done(function(data, textStatus, jqXHR) {
                Util.notifySuccess("New study saved");
            })
            .fail(function(data, textStatus, jqXHR) {
                Util.notifyError("Failed saving new study");
            });
        }
    });

/// ======== revise ========
    
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
        var end_date = new Date();
        var start_date = null;
        if (history === "last_week") {
            start_date = getLastWeek();
        }
        if (history === "last_month") {
            start_date = getLastMonth();
        }
        console.log('end_date (today):', end_date);
        console.log('start_date: ', start_date);
        return StudyAPI.getStudyBetween(start_date, end_date);
    };

    /**
     * Flashcard click callback in revise mode
     *     update study history's revise date
     *     remove the current from studyList_ (update $txtAllStudy_)
     *     show next vocabulary
     */
    var reviseClickCallback = function() {
        StudyAPI.reviseStudy(studyList_.get())
        .done(function(data, textStatus, jqXHR) {
            Util.notifySuccess("Revise saved");
            studyList_.remove();
            $txtAllStudy_.text(studyList_.getAll());
            Flashcard.displayVocabulary(studyList_.get());
        })
        .fail(function(data, textStatus, jqXHR) {
            Util.notifyError("Failed saving revise");
        });
    };

    /*
     * Init elements for the revise mode
     */ 
    var initRevise = function() {
        // get study history
        getStudyHistory()
        .done(function(data, textStatus, jqXHR) {
            resetUI();

            Util.notifySuccess("Study history loaded");
            console.log('history data: ', data);
            var v = JSON.parse(data);
            studyList_.set(v);
            clickCallback_ = reviseClickCallback;
            currentMode_ = "Revise";

            // clear recap list
            recapList_.clear();
            setUI();
        })
        .fail(function(data, textStatus, jqXHR) {
            Util.notifyError("Failed loading the study history");
        });
    };

    $("#button_load_history").click(function() {
        initRevise();
    });

    $("#button_add_to_recap_list").click(function() {
        if (currentMode_ === 'Revise') {
            console.log('recap: ', studyList_.get());
            recapList_.add(studyList_.get());
            studyList_.remove();
            $txtAllStudy_.text(studyList_.getAll());
            Flashcard.displayVocabulary(studyList_.get());
            $txtRecapList_.text(recapList_.getAll());
        }
    });
/// ======== recap ========

    var recapClickCallback = function() {
        Flashcard.displayVocabulary(studyList_.getNext());
    };

    var initRecap = function() {
        // get study history
        resetUI();

        studyList_.set(recapList_.getAll());
        clickCallback_ = recapClickCallback;
        currentMode_ = "Recap";
        // reset recap list
        recapList_.clear();

        setUI();
    };

    $("#button_recap").click(function() {
        var vocabularies = recapList_.getAll().join(' ');
        console.log("Recap: ", vocabularies);
        StudyAPI.newStudy(vocabularies)   // treat recap as new
        .done(function(data, textStatus, jqXHR) {
            Util.notifySuccess("Recap saved");
            initRecap();
        })
        .fail(function(data, textStatus, jqXHR) {
            Util.notifyError("Failed saving the recap");
        });
    });




    // initialise
    // bind Flashcard
    Flashcard.init($("#flashcard"));
});