function HornbookAPICtrl($scope) {
    console.log($scope);
	$scope.apis = [
		{"name": "api/most_common_character",
	     "request": "some request 1111",
	 	 "response": "some response"},
		{"name": "api/most_common_word",
	     "request": "?ref_character=asdf&last_word=asdf",
	 	 "response": "some response"}
	];
}