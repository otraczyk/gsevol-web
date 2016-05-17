'use strict';
var plugins = require('gulp-load-plugins')({
  pattern: '*',
  config: process.cwd() + '/package.json',
  lazy: true
});

var gulp  = require('gulp-help')(require('gulp'));


gulp.task('clean', clean);
gulp.task('build-react', buildReact);
gulp.task('build-styles', buildStyles);
gulp.task('watch-react', watchReact);
gulp.task('watch-styles', watchStyles);
gulp.task(
    'inject',
    'Add reference to all bower dependencies and local js files to html.',
    injectDeps
);
gulp.task('watch-deps', watchDeps);
gulp.task(
    'apply-static',
    'Change all dependencies\'s refs for serving static files from django.',
    applyStatic
);
gulp.task('concat', concat);
gulp.task('minify', minifyCombined);
gulp.task('build-production', buildProduction);
gulp.task('build-dev', buildDev);
gulp.task(
    'watch',
    'Rebuild react, styles and dependencies after code changes.',
    ['build-dev', 'watch-react', 'watch-deps', 'watch-styles'],
    function(){}
);
gulp.task('inject-dev', function(done) {
    plugins.runSequence('inject', 'apply-static', done);
});


function clean(done) {
    return plugins.del(['dist/*.*', 'build/*.*'], done);
}

function buildReact(){
    return gulp.src('./app/*.jsx')
        .pipe(plugins.react())
        .pipe(gulp.dest('./build'));
}

function buildStyles() {
    return gulp.src('assets/*.scss')
        .pipe(plugins.plumber())
            .pipe(plugins.sass())
        .pipe(gulp.dest('build/'));
}

function watchReact(){
    return plugins.watch('./app/*.jsx', function(){
        gulp.start('build-react');
    });
}

function watchDeps(){
    return plugins.watch('./bower_components/**/*.*', function(){
        plugins.runSequence('inject', 'apply-static');
    });
}

function watchStyles() {
  return plugins.watch(['assets/**/*.scss', 'assets/*.scss'],
    function () {
        gulp.start('build-styles');
  });
}

function injectDeps(){
    return gulp.src('templates/dependencies-empty.html')
        .pipe(plugins.wiredep.stream(
        {
            directory: 'bower_components/',
            fileTypes: {
                html: {
                  replace: {
                    js: '<script src="{{filePath}}"></script>',
                    css: '<link rel="stylesheet" href="{{filePath}}" />'
                  }
                }
              }
        }))
        .pipe(plugins.inject(gulp.src(['build/*.*', 'assets/**/*.js'], {read: false}),
            {relative: true}, {
        }))
    .pipe(plugins.rename('dependencies.html'))
    .pipe(gulp.dest('templates/'));
}


function concat() {
    return gulp.src('templates/dependencies.html')
                .pipe(plugins.useref())
                .pipe(gulp.dest('templates/'));
}

function applyStatic() {
    var re = /\"\.\.\/(dist|bower_components|build|assets)\/([^"]*)\"/g;
    var subst = '"{% static \'$2\' %}"';

    return gulp.src('templates/dependencies.html')
            .pipe(plugins.replace(re, subst))
            .pipe(gulp.dest('templates/'))
}

function minifyCombined() {
    gulp.src('dist/combined.js')
        .pipe(plugins.uglify({
            compress: {
                 drop_console: true
            }
        }))
        .pipe(gulp.dest('dist/'));
    gulp.src('dist/combined.css')
        .pipe(plugins.cleanCss())
        .pipe(gulp.dest('dist/'));
}

function buildProduction(done) {
    plugins.runSequence('clean', ['build-react', 'build-styles'], 'inject', 'concat',
                'apply-static', 'minify', done);
}

function buildDev(done){
    plugins.runSequence('clean', ['build-react', 'build-styles'], 'inject-dev', done);
}
