function HornbookAPICtrl($scope, $http) {
	$scope.apis = [
		{
			"name": "Most Common Character",
		 	"url": "/api/most_common_character",
	 	 	"response": {
	 			"data": "",
	 			"status": "",
	 			"headers": "" 	
	 	 	}
	 	},
		{
			"name": "All Most Common Characters",
		 	"url": "/api/all_most_common_characters",
	 	 	"response": {
	 			"data": "",
	 			"status": "",
	 			"headers": "" 	
	 	 	}
	 	},
	 	{
			"name": "Most Common Word",
		 	"url": "/api/most_common_word",
	     	"params": 
	     	{
	     		"ref_character": "一",
	     		"last_word": "一个"
	     	},
	 	 	"response": {
	 			"data": "",
	 			"status": "",
	 			"headers": "" 	
	 	 	}
	 	},
	];

	var prettyJSON = function(obj) {
		return JSON.stringify(obj, null, 4);
	};

	var hornbookAPIService = function(api) {
		$http({
			method: "GET",
			url: api.url,
			params: api.params
		}).success(function(data, status, headers){
			api.response.data = prettyJSON(data);
			api.response.status = prettyJSON(status);
			api.response.headers = prettyJSON(headers());
		});
	};
	
	$scope.requestAPI = function(api) {
		hornbookAPIService(api);
	};

	// request API
	$scope.apis.forEach(function(element, index, array) {
		hornbookAPIService(element);
	});
}