// Karma configuration
// Generated on Fri Jun 13 2014 13:57:22 GMT+0000 (UTC)

module.exports = function(config) {
  config.set({
    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: '',

    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine'],

    // list of files / patterns to load in the browser
    files: [
      //'test-main.js',
      //{pattern: 'lib/**/*.js', included: false},
      //'compiled/js/app.js',
      './compiled/js/app.bundled.js'
//code/**/*Spec.coffee'}
    ],

    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: {
      './compiled/**/*.js': ['sourcemap']
      //'./code/**/*.coffee': ['browserify']
      //'code/**/*.jsx': ['browserify']
    },

    /*
    browserify: {
      extensions: ['.coffee'],//, '.jsx'],
      transform: ['coffeeify'],//, 'reactify'],
      debug: true,
      watch: true,
    },*/

    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['progress'],

    autoWatch: true,
    port: 9876,
    colors: true,
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_DEBUG,
    browsers: [],
    singleRun: false
  });
};
