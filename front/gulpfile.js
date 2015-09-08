'use strict';

var gulp = require('gulp'),
    watch = require('gulp-watch');

gulp.task(
  'watch',
  'Watch for any changes in js, scss, html files',
  ['watch-react'] //, 'watch-scss', 'watch-bower', 'watch-html']
);

gulp.task('watch-react', false, watchReact);
// gulp.task('watch-scss', false, watchScss);
// gulp.task('watch-bower', false, watchBower);
// gulp.task('watch-html', false, watchHtml);

var react = require('gulp-react');

function watchReact() {
  return watch('app/*.react.js', function (){
        return gulp.src('template.jsx')
            .pipe(react())
            .pipe(gulp.dest('dist'));
            // .on('end', callback);
  });
}
