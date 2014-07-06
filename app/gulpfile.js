/*
 * Gulp file for frontend. Due to the nature of gulp there are a few limitations:
 *  - Recompilation of coffeescript/sass will happen on every single file change.
 *    This has the down side of making changing branches a mess.
 *  - Watching tests must be done with karma on the command line as gulp makes
 *    a mess of this:
 *      node_modules/karma/bin/karma start
 *  - Passing --production as an argument will produce production-ready assets
 *
 * Expected usage is:
 *  - gulp code && gulp sass
 *    compiles all the code and sass files into compiled/js and compiled/css
 *  - gulp watch
 *    as above but watches for changes and recompiles in a quicker fashion
 *  - karma run karma.conf.js
 *    not a gulp command but runs the tests. Connect a chrome/firefox window
 *    to the web server it creates
 */

var browserify = require('browserify');
var clean = require('gulp-clean');
var coffeeify = require('coffeeify');
// var compass = require('gulp-compass');
var sass = require('gulp-sass');
var convertSourceMap = require('convert-source-map')
var es = require('event-stream');
var fs = require('fs');
var gulp = require('gulp');
var gutil = require('gulp-util');
var path = require('path');
var reactify = require('reactify');
var rename = require('gulp-rename');
var source = require('vinyl-source-stream')
var sourcemaps = require('gulp-sourcemaps')
var through = require('through2');
var uglify = require('gulp-uglify');
var watchify = require('watchify');
var browserifyShim = require('browserify-shim')

// Get arguments out of the command line
var argv = require('yargs').argv;

/*
 * Cleans out any compiled files
 */
gulp.task('clean', function() {
  return gulp.src(['./compiled/'], {read: false})
    .pipe(clean())
});

/*
 * Creates css files from Sass
 */
gulp.task('sass', function() {
  return gulp.src('sass/app.scss')
    .pipe(sass())
    .pipe(rename('app.css'))
    .pipe(gulp.dest('compiled/css'));
});

/*
 * Watches for changes in the code/sass and recompiles
 */
gulp.task('watch', function() {
  gulp.watch('sass/**/*.scss', ['sass']);
  compile(true);
});

/*
 * Compiles the code
 */
gulp.task('code', function() {
  return compile(false);
});

var stripExtension = function(filename) {
  return filename.substring(0, filename.lastIndexOf("."));
}

/*
 * Creates a file containing require statements for every single spec in
 * the project. Outputs to code/app.bundled/js which should be added to
 * .gitignore)
 */
var prepBundler = function() {
  var requires = []
  
  var write = function(file, enc, cb) {
    var destName = stripExtension(file.relative)
    requires.push('require("./' + destName + '");');
    cb();
  }

  var flush = function(cb) {
    var newFile = new gutil.File({
      base: __dirname,
      cwd: __dirname,
      path: __dirname + '/app.bundled.js',
      contents: new Buffer(requires.join("\n"))
    });
    this.push(newFile);
    cb();
  };

  return through.obj(write, flush);
}

/*
 * Compiles a bundle file that is passed through.
 *  - watch - if set to true will make this task run forever watching for changes
 */
var compileBundle = function(watch) {
  var filenames = []

  var _compileBundle = function(file, callback) {
    var cwd = process.cwd()
    var sourcePath = '.' + file.path.substring(cwd.length)
    var destName = stripExtension(file.relative) + ".js"

    gutil.log('Bundling', sourcePath, 'to', destName);

    var bundler;
    var shimmy = {
        'gridster': {
          path: 'node_modules/gridster/dist/jquery.gridster.js',
          exports: 'gridster',
        }
    }

    browserifyOptions = {
      extensions: ['.coffee', 'jsx'],
    };

    if (watch) {
      browserifyOptions.delay = 300;
      bundler = watchify(sourcePath, browserifyOptions);
    } else {
      bundler = browserify(sourcePath, browserifyOptions);
    }
    bundler.transform(coffeeify);
    bundler.transform(reactify);
    bundler.transform(browserifyShim);

    function rebundle() {
      return bundler.bundle({debug: true})
        .on('error', function(err) {
          gutil.beep();
          gutil.log(gutil.colors.red(err));
        })
        .pipe(source(destName))
        .pipe(gulp.dest('/tmp/js'))
        .on('end', function() {
          gulp.src('/tmp/js/' + destName)
            .pipe(sourcemaps.init())
            //.pipe(uglify())
            .pipe(sourcemaps.write())
            .pipe(gulp.dest('./compiled/js/'))
        })
    }
    bundler.on('update', rebundle);
    bundler.on('log', gutil.log);

    return rebundle()
  }

  return es.map(_compileBundle)
}


/*
 * Compiles all the bundles
 *  - app.coffee - the main app
 *  - app.bundled.js - the tests for karma to run
 */
var compile = function(watch) {
  gulp.src('./code/**/*Spec.coffee', {read: false})
    .pipe(prepBundler())
    .pipe(gulp.dest('./code'))
    .on('end', function() {
      gulp.src(['./code/app.coffee', './code/app.bundled.js'], {read: false})
        .pipe(compileBundle(watch));
    });

  return
}
