'use strict';
var plugins = require('gulp-load-plugins')({
  pattern: '*',
  config: process.cwd() + '/package.json',
  lazy: true
});

var gulp  = require('gulp-help')(require('gulp')),
    watch = require('gulp-watch');


var react = require('gulp-react');
var babel = require('gulp-babel');
var wiredep = require('wiredep').stream;
var useref = require('gulp-useref');
var inject = require('gulp-inject');
var rename = require('gulp-rename');
var runSequence = require('run-sequence'),
    gulpif = require('gulp-if'),
    uglify = require('gulp-uglify'),
    minifyCss = require('gulp-clean-css');

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
gulp.task('apply-static', applyStatic);
gulp.task('minify', minifyCombined);
gulp.task('concat', [
        'build-react',
        'styles',
        'inject'
    ], concat);
gulp.task('build-production',production);


function buildReact(){
    return gulp.src('./app/*.jsx')
        .pipe(react())
        // .pipe(babel({
        //     presets: ["react"]
        // }))
        .pipe(gulp.dest('./build'));
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
    return gulp.src('templates/dependencies-empty.html')
        .pipe(wiredep(
        {
            directory: 'bower_components/',
            // ignorePath: '../bower_components/',
            fileTypes: {
                html: {
                  replace: {
                    js: '<script src="{{filePath}}"></script>',
                    css: '<link rel="stylesheet" href="{{filePath}}" />'
                  }
                }
              }
        }))
        .pipe(inject(gulp.src(['build/*.*', 'assets/**/*.js'], {read: false}),
            {relative: true}, {
        }))
    .pipe(rename('dependencies.html'))
    .pipe(gulp.dest('templates/'));
}

function watchScss() {
  plugins.watch(['assets/**/*.scss', 'assets/*.scss'],
    function () {
        gulp.start('styles');
  });
}

function compileStyles() {
    var sassStream = gulp.src('assets/*.scss')
        .pipe(plugins.plumber())
            .pipe(plugins.sass())
        .pipe(gulp.dest('build/'));

    return sassStream;
}

function concat() {
    return gulp.src('templates/dependencies.html')
                .pipe(useref())
                // .pipe(gulpif('*.js', uglify()))
                // .pipe(gulpif('*.css', minifyCss()))
                .pipe(gulp.dest('templates/'));
}

function applyStatic() {
    var buildStatic = function(content) {
        var re = /\.\.\/dist\/([^"]*)/g;
        var subst = '{% static \'$1\' %}';
        var content = content.replace(re, subst);
        return content;
    }
    return gulp.src('templates/dependencies.html')
            .pipe(useref({buildStatic: buildStatic}))
            .pipe(gulp.dest('templates/'))
}

function minifyCombined() {
    // Minification in useref doesn't work.
    gulp.src('dist/combined.js')
        .pipe(uglify())
        .pipe(gulp.dest('dist/'));
    gulp.src('dist/combined.css')
        .pipe(minifyCss())
        .pipe(gulp.dest('dist/'));
}

function production(done) {
    runSequence('concat', 'apply-static', 'minify', done);
}
