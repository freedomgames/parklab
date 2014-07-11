planet_app.controller('OrganizationCtrl', ['getterFactory', 'setterFactory', '$scope', function(getterFactory, setterFactory, $scope){
    $scope.msg = "This is the organization page!";

    $scope.organization = [];

    getterFactory.getItem('1', function(data){
        for (i=0;i<data.length;i++){
            $scope.organization[i] = data[i];
        }
        console.log($scope.organization)
    });
}]);