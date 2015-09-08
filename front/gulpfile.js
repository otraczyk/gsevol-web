'use strict';

var gulp = require('gulp'),
    watch = require('gulp-watch');

var react = require('gulp-react');

gulp.task(
  'watch',
  // 'Watch for any changes in js, scss, html files',
  ['build-react'],
   watchReact //, 'watch-scss', 'watch-bower', 'watch-html']
);

gulp.task('build-react', false, buildReact);
// gulp.task('watch-scss', false, watchScss);
// gulp.task('watch-bower', false, watchBower);
// gulp.task('watch-html', false, watchHtml);

function buildReact(){
    return gulp.src('./app/*.jsx')
        .pipe(react())
        .pipe(gulp.dest('./dist'));
}

function watchReact() {
  return watch('./app/*.jsx', buildReact);
}
