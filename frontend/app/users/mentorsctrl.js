planet_app.controller('MentorsCtrl', ['getterFactory', 'setterFactory', '$scope', function(getterFactory, setterFactory, $scope) {
    $scope.mentors = [];

    getterFactory.getItems('mentors', function(data){
        for (i=0;i<data.length;i++){
            $scope.mentors[i] = data[i];
        }
        //console.log($scope.mentors)
    });

    setterFactory.setItem('mentors', function(data){
        console.log(data)
    });
}]);