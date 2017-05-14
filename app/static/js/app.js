var app = angular.module('wordApp', ['ngAnimate', 'angucomplete-alt']);

app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

app.controller('WordController', function ($scope, $http) {

    var $self = this;

    $self.page = 'add';
    $self.word = '';
    $self.words = [];
    $self.error = '';
    $self.searchText = '';

    $self.notification = {
        show: false,
        message: 'Good shit',
        type: 'success',
    };

    $scope.upload = function (files) {

        var fd = new FormData();
        fd.append("audio_file", files[0]);
        if (typeof $self.word.originalObject.word !== 'undefined') {
            fd.append("word", $self.word.originalObject.word);
        } else {
            fd.append("word", $self.word.originalObject);
        }

        $http.post('/', fd, {
            withCredentials: true,
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity,
        }).then(function (data) {
            if (data.data.success) {
                $self.word = '';
                $self.error = '';
                $self.hideNotification();
                $self.showNotification(data.data.message);
            } else {
                $self.error = data.data.message;
            }
        })
    };

    $self.save = function () {
        var files = document.getElementById('audio_file').files;

        $scope.upload(files);
        $self.getWords();
    };

    $self.playAudio = function(filename) {
        var audio = new Audio('files/' + filename);
        audio.play();
    };

    $scope.$watch('wordController.word', function () {
        var checkValue;
        if (typeof $self.word.originalObject.word !== 'undefined') {
            checkValue = $self.word.originalObject.word;
        } else {
            checkValue = $self.word.originalObject
        }
        if ($self.wordExists(checkValue)) {
            $self.showNotification('This word already exists! It will be updated on save.', 'warning', false);
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

    $self.showNotification = function (message, type, leave) {
        $self.notification = {
            show: true,
            message: message,
            type: typeof type === 'undefined' ? 'success' : type,
        };

        leave = typeof leave === 'undefined' ? true : leave;
        if (leave) {
            setTimeout(function () {
                $self.notification = {
                    show: false,
                    message: '',
                    type: type,
                };
            }, 5000)
        }
    };

    $self.hideNotification = function () {
        $self.notification = {
            show: false,
            message: '',
            type: 'success',
        };
    };
});
