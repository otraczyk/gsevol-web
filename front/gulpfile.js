'use strict';
var plugins = require('gulp-load-plugins')({
  pattern: '*',
  config: process.cwd() + '/package.json',
  lazy: true
});

var gulp  = require('gulp-help')(require('gulp')),
    watch = require('gulp-watch');


var react = require('gulp-react');
var wiredep = require('wiredep').stream;

gulp.task(
    'watch',
    'Watch for any changes in js, scss, html files',
    ['watch-react', 'watch-deps', 'watch-scss'],
    function(){}
);

gulp.task('build-react', false, buildReact);
gulp.task('watch-react', ['build-react'], watchReact);
gulp.task('watch-deps', watchDeps);
gulp.task('inject', injectDeps);
gulp.task('styles', false, compileStyles);
gulp.task('watch-scss', ['styles'], watchScss);


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

function watchScss() {
  plugins.watch(['assets/**/*.scss', 'assets/*.scss'],
    function () {
        gulp.start('styles');
  });
}

function compileStyles() {
    var sassStream = gulp.src('assets/style.scss')
        .pipe(plugins.plumber())
            .pipe(plugins.sass())
        .pipe(gulp.dest('dist/'));

    return sassStream;
}
