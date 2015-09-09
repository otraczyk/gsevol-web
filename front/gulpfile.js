'use strict';

var gulp  = require('gulp-help')(require('gulp')),
    watch = require('gulp-watch');

var react = require('gulp-react');

gulp.task(
    'watch',
    'Watch for any changes in js, scss, html files',
    ['watch-react'],
    function(){}
);

gulp.task('build-react', false, buildReact);
gulp.task('watch-react', ['build-react'], watchReact);

function buildReact(){
    return gulp.src('./app/*.jsx')
        .pipe(react())
        .pipe(gulp.dest('./dist'));
}

function watchReact(){
    return watch('./app/*.jsx', buildReact);
}
