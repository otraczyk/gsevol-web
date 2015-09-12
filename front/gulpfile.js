'use strict';

var gulp  = require('gulp-help')(require('gulp')),
    watch = require('gulp-watch');

var react = require('gulp-react');
var wiredep = require('wiredep').stream;

gulp.task(
    'watch',
    'Watch for any changes in js, scss, html files',
    ['watch-react', 'watch-deps'],
    function(){}
);

gulp.task('build-react', false, buildReact);
gulp.task('watch-react', ['build-react'], watchReact);
gulp.task('watch-deps', watchDeps);
gulp.task('inject', injectDeps);

function buildReact(){
    return gulp.src('./app/*.jsx')
        .pipe(react())
        .pipe(gulp.dest('./dist'));
}

function watchReact(){
    return watch('./app/*.jsx', function(){
        gulp.start('build-react');
    });
}

function watchDeps(){
    return watch('./bower_components/**/*.*', function(){
        gulp.start('inject');
    });
}

function injectDeps(){
    console.log("Injecting bower dependencies");
    return gulp.src('templates/base.html')
        .pipe(wiredep(
        {
            directory: 'bower_components/',
            exclude: ['bower_components/gumby/*'],
            ignorePath: '../bower_components/',
            fileTypes: {
                html: {
                  replace: {
                    js: '<script src="{% static \'{{filePath}}\' %}"></script>',
                    css: '<link rel="stylesheet" href="{% static \'{{filePath}}\' %}" />'
                  }
                }
              }
        }))
    .pipe(gulp.dest('templates/'));
}
