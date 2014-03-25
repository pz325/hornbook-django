$(document).ready(function() {

/// Study elements
    var $txtAllStudy_ = $("#all_study");
    var $txtRecapList_ = $("#recap #recap_list");
    
    var studyList_ = [];
    var graspedList_ = [];
    var recapList_ = [];
    
    var clickCallback_ = null;
    var currentMode_ = '';

    var resetUI = function() {
       $txtAllStudy_.text("");
       $txtRecapList_.text("");
       
       studyList_ = [];
       graspedList_ = [];
       recapList_ = [];

       clickCallback_ = null;
       currentMode_ = '';

       Flashcard.displayVocabulary("");
    };

    /**
     *
     */
    var setUI = function() {
        // display all vocabularies
        $txtAllStudy_.text(studyList_.join(" "));
        console.log('Study list: ', studyList_);
        // bind flashcard strategy
        Flashcard.setHanCharacterDivClickCallback(clickCallback_);
        Flashcard.displayVocabulary(studyList_.pop());
    };

/// ======== study new ========

    /*
     * Flashcard click callback in StudyNew mode
     *     save the current vocabulary to graspedList_ (as a holder)
     *     pop one element from studyList_
     *     if studyList_ is empty, swap studyList_ and graspedList_
     *     shuffle studyList_
     */
    var studyNewClickCallback = function() {
        graspedList_.push(Flashcard.getLastWord());
        Flashcard.displayVocabulary(studyList_.pop());
        if (studyList_.length === 0) {
            studyList_ = Util.shuffle(graspedList_);
            graspedList_ = [];    
        }
    };

    /*
     * Init elements for the study new mode
     */ 
    var initStudyNew = function() {
        resetUI();

        // get new studies
        var today_study = $("#input_today_study").val().trim();
        console.log("today study: ", today_study);
        studyList_ = today_study.split(" ");

        clickCallback_ = studyNewClickCallback;        
        currentMode_ = "StudyNew";

        setUI();
    };

    $("#button_add_new").click(function() {
        initStudyNew();
        return false;
    });

    $("#button_save_to_server").click(function() {
        if (currentMode_ === "StudyNew") {
            var newWords = [];
            newWords.push(Flashcard.getLastWord());
            newWords.push.apply(newWords, graspedList_);
            newWords.push.apply(newWords, studyList_);
            console.log(newWords);
            StudyAPI.newStudy(newWords.join(" "))
            .done(function(data, textStatus, jqXHR) {
                Util.notifySuccess("New study saved");
            })
            .fail(function(data, textStatus, jqXHR) {
                Util.notifyError("Failed saving new study");
            });
        }
        return false;
    });


/// ======== revise ========    
    /**
     * call getStudyHistoryIntelligent() or getStudyHistoryBetween()
     * @return $.ajax() deferred object
     */
    var getStudyHistory = function() {
        var history = $('#select_previous_study option:selected').val();
        console.log("history: ", history);
        
        if (history === "intelligent")
            return StudyAPI.getStudyIntelligent();

        if (history === "last_week" || history === "last_month")
            return getStudyHistoryBetween(history);
    };

    /*
     * call StudyAPI.getStudyBetween()
     * @return $.ajax() deferred object
     */
    var getStudyHistoryBetween = function(history) {
        var today = new Date();
        var end_date = new Date();
        var start_date = null;
        if (history === "last_week")
            start_date = Util.getLastWeek();
        if (history === "last_month")
            start_date = Util.getLastMonth();

        console.log('end_date (today):', end_date);
        console.log('start_date: ', start_date);
        return StudyAPI.getStudyBetween(start_date, end_date);
    };

    /**
     * Flashcard click callback in revise mode
     *     remove from studyList_, and save to graspedList_
     *     update progress UI
     *     if studyList_ is to be empty,
     *         save revising history to server
     *     show next vocabulary
     */
    var reviseClickCallback = function() {
        graspedList_.push(Flashcard.getLastWord());

        if (studyList_.length === 0) {
            saveRevise();
            // go to recap mode
            if (recapList_.length > 0)
                initRecap();
            else
                resetUI();
        } else {
            Flashcard.displayVocabulary(studyList_.pop());
        }
    };

    /**
     * Save revise to server
     * Start Revise mode if ncessary
     */
    var saveRevise = function() {
        $.when(
            StudyAPI.reviseStudy(graspedList_.join(" ")),
            StudyAPI.newStudy(recapList_.join(" "))
        ).done(function(r1, r2) {
            Util.notifySuccess("Revise saved");
        })
        .fail(function(r1, r2) {
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
            studyList_ = JSON.parse(data);
            if (studyList_.length > 0) {
                studyList_ = Util.shuffle(studyList_);
                clickCallback_ = reviseClickCallback;
                currentMode_ = "Revise";

                setUI();
            }
            else {
                Util.notifyError("No learning history available");
                $txtAllStudy_.text("No learning history available");
            }
        })
        .fail(function(data, textStatus, jqXHR) {
            Util.notifyError("Failed loading the study history");
        });
    };

    $("#button_load_history").click(function() {
        initRevise();
        return false;
    });

    $("#button_add_to_recap_list").click(function() {
        if (currentMode_ === 'Revise') {
            recapList_.push(Flashcard.getLastWord());
            console.log('recap list: ', recapList_);
            console.log('study list: ', studyList_)
            if (studyList_.length === 0) {
                saveRevise();
                // go to recap mode
                if (recapList_.length > 0)
                    initRecap();
                else
                    resetUI();
            } else {
                Flashcard.displayVocabulary(studyList_.pop());
                $txtRecapList_.text(recapList_);
            }
        }
        return false;
    });

/// ======== recap ========

    var recapClickCallback = function() {
        recapList_.push(Flashcard.getLastWord());
        Flashcard.displayVocabulary(studyList_.pop());
        if (studyList_.length === 0) {
            studyList_ = recapList_;
            recapList_ = [];
        }
    };

    var initRecap = function() {
        studyList_ = recapList_;
        recapList_ = [];
        $txtRecapList_.text("recap mode");
        clickCallback_ = recapClickCallback;
        currentMode_ = "Recap";

        setUI();
        Util.notifySuccess("Switch to Recap mode");
    };

    // initialise
    // bind Flashcard
    Flashcard.init($("#flashcard"));

});