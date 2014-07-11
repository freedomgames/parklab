planet_app.controller('ProfileCtrl', ['getterFactory', 'setterFactory', '$scope', function(getterFactory, setterFactory, $scope){
    $scope.msg = "This is the profile page!";

    $scope.mentor = [];

    getterFactory.getItem('1', function(data){
        for (i=0;i<data.length;i++){
            $scope.mentor[i] = data[i];
        }
        console.log($scope.mentor)
    });
}]);