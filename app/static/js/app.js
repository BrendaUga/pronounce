var app = angular.module('wordApp', []);

app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

app.controller('WordController', function ($scope, $http) {

    var $self = this;

    $self.page = 'add';
    $self.word = '';
    $self.words = [];

    $scope.upload = function (files) {

        var fd = new FormData();
        fd.append("audio_file", files[0]);
        fd.append("word", this.word);

        $http.post('/', fd, {
            withCredentials: true,
            headers: { 'Content-Type': undefined },
            transformRequest: angular.identity
        }).then(function (data) {
            if (data.data.success) {
                // Show notification that all is good
            }
        })
    };

    $self.save = function () {
        var files = document.getElementById('audio_file').files;

        $scope.upload(files);
    };

    $scope.$watch('wordController.word', function () {

        if ($self.wordExists($self.word)) {

            // Show notification
            console.log('word exists')
        }
    });

    $self.getWords = function () {
        $http.get('/words')
            .then(function (data) {
                $self.words = data.data;
            })
    };

    $self.getWords();

    $self.wordExists = function (word) {
        return typeof $self.words.find(function (w) {
                return w.word == word;
            }) !== 'undefined';
    };
});
