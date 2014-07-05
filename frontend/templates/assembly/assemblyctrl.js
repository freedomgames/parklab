planet_app.controller('AssemblyCtrl', ['getterFactory', 'setterFactory', '$scope', function(getterFactory, setterFactory, $scope){
    $scope.msg = "This is the assembly page!";

    $scope.assembly = [];

    getterFactory.getItem('1', function(data){
        for (i=0;i<data.length;i++){
            $scope.assembly[i] = data[i];
        }
        console.log($scope.assembly)
    });
}]);