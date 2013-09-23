function HornbookAPICtrl($scope) {
	$scope.apis = [
		{"name": "api/most_common_character",
	     "request": "some request",
	 	 "response": "some response"},
		{"name": "api/most_common_word",
	     "request": "?ref_character=asdf&last_word=asdf",
	 	 "response": "some response"}
	];
}